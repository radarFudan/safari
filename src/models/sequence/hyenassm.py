import math

from re import U
import torch
import torch.nn as nn
import torch.nn.functional as F
from functools import partial

from einops import rearrange, repeat

try:
    from src.ops.fftconv import fftconv_ref, fftconv_func
except ImportError:
    fftconv_func = None

try:
    from flash_attn.ops.fused_dense import FusedDense
except ImportError:
    FusedDense = None

import src.utils.registry as registry
from src.utils.train import OptimModule
from src.utils.config import instantiate, auto_assign_attrs
from src.models.nn import Activation


# reference convolution with residual connection
def fftconv_ref(u, k, D, dropout_mask, gelu=True, k_rev=None):
    seqlen = u.shape[-1]
    fft_size = 2 * seqlen
    k_f = torch.fft.rfft(k, n=fft_size) / fft_size
    if k_rev is not None:
        k_rev_f = torch.fft.rfft(k_rev, n=fft_size) / fft_size
        k_f = k_f + k_rev_f.conj()
    u_f = torch.fft.rfft(u.to(dtype=k.dtype), n=fft_size)

    if len(u.shape) > 3:
        k_f = k_f.unsqueeze(1)

    y = torch.fft.irfft(u_f * k_f, n=fft_size, norm="forward")[..., :seqlen]

    out = y + u * D.unsqueeze(-1)
    if gelu:
        out = F.gelu(out)
    if dropout_mask is not None:
        return (out * rearrange(dropout_mask, "b H -> b H 1")).to(dtype=u.dtype)
    else:
        return out.to(dtype=u.dtype)


@torch.jit.script
def mul_sum(q, y):
    return (q * y).sum(dim=1)


class HyenaSSMFilter(OptimModule):
    def __init__(
        self,
        d_model,
        d,
        order,
        seq_len,
        hidden_dim,
        constant_one=True,
    ):
        super().__init__()
        self.d_model = d_model
        self.d = d
        self.order = order
        self.seq_len = seq_len
        self.hidden_dim = hidden_dim
        self.constant_one = constant_one

        # c, (d*order, m)
        # W, (m, m)
        # U, (m, d*order)
        # m shall be >= d * order
        # TODO, construct the c, W, U as parameters
        if not self.constant_one:
            pass
            assert hidden_dim >= d * order
            self.c = nn.Parameter(torch.randn(d * order, hidden_dim))
            self.W = nn.Parameter(torch.randn(hidden_dim, hidden_dim))
            self.U = nn.Parameter(torch.randn(hidden_dim, 1))
            self.dt = nn.Parameter(torch.rand(1) * 0.1)  # dt <= 0.1

    def filter(self, L):
        # shape(1, L, d * (order - 1))
        assert L <= self.seq_len

        # TODO, parameterizes the filter based on c, W, U

        if self.constant_one:
            return torch.ones(1, L, self.d * (self.order - 1))
        else:
            return (
                self.c
                @ torch.matrix_exp(
                    self.W.unsqueeze(0)
                    * (torch.linspace(0, L, L).unsqueeze(-1).unsqueeze(-1))
                    * self.dt
                )
                @ self.U
            )

    def forward(self, x, L, k=None, bias=None, *args, **kwargs):
        if k is None:
            k = self.filter(L)

        # Ensure compatibility with filters that return a tuple
        k = k[0] if type(k) is tuple else k
        if bias is None:
            bias = self.bias
        bias = bias if self.use_bias else 0 * bias

        if self.fused_fft_conv:
            bias = bias.to(dtype=torch.float32)
            y = fftconv_func(
                x,
                k,
                bias,
                dropout_mask=None,
                gelu=False,
                force_fp16_output=torch.is_autocast_enabled(),
            )
        else:
            y = fftconv_ref(x, k, bias, dropout_mask=None, gelu=False)

        return y


class HyenaSSMOperator(nn.Module):
    def __init__(
        self,
        d_model,
        l_max,
        order=2,
        filter_order=64,
        num_heads=1,
        inner_factor=1,
        num_blocks=1,
        fused_bias_fc=False,
        outer_mixing=False,
        dropout=0.0,
        filter_dropout=0.0,
        filter_cls="hyena-filter",
        post_order_ffn=False,
        jit_filter=False,
        short_filter_order=3,
        activation="id",
        return_state=False,
        **filter_args,
    ):
        r"""
        Hyena operator described in the paper https://arxiv.org/pdf/2302.10866.pdf

        Args:
            d_model (int): Dimension of the input and output embeddings (width of the layer)
            l_max: (int): Maximum input sequence length. Defaults to None
            order: (int): Depth of the Hyena recurrence. Defaults to 2
            filter_order: (int): Width of the FFN parametrizing the implicit filter. Defaults to 64
            num_heads: (int): Number of heads. Defaults to 1
            inner_factor: (int): Width multiplier. Defaults to 1
            num_blocks: (int): Number of blocks in sequence length. Defaults to 1
            fused_bias_fc: (bool): Whether to use fused bias FC. Defaults to False
            dropout: (float): Dropout probability. Defaults to 0.0
            filter_dropout: (float): Dropout probability for the filter. Defaults to 0.0
            post_order_ffn: (bool): Apply a dense layer between steps of the recurrence. Defaults to False
            jit_filter: (bool): Whether JIT the implicit filter function. Defaults to False
            short_filter_order: (int): Length of the explicit input convolutional filter. Defaults to 3
            activation: (str): type of act between kernel output and FF (default identity)
            return_state: (bool): whether to return a state
        """
        super().__init__()
        assert (
            d_model % num_heads == 0
        ), f"Model dimension {d_model} must be divisible by num heads {num_heads}"
        assert (
            l_max % num_blocks == 0
        ), f"Maximum signal length {l_max} must be divisible by block dimension {num_blocks}"
        block_dim = l_max // num_blocks
        head_dim = d_model // num_heads

        auto_assign_attrs(
            self,
            d_model=d_model,
            order=order,
            l_max=l_max,
            num_heads=num_heads,
            inner_factor=inner_factor,
            block_dim=block_dim,
            head_dim=head_dim,
            filter_order=filter_order,
            post_order_ffn=post_order_ffn,
            short_filter_order=short_filter_order,
            num_blocks=num_blocks,
            filter_dropout=filter_dropout,
            jit_filter=jit_filter,
            outer_mixing=outer_mixing,
            activation=activation,
            return_state=return_state,
        )
        self.activation = Activation(activation)
        self.dropout = nn.Dropout(dropout)
        self.setup_projections(fused_bias_fc, inner_factor)
        self.setup_filters(filter_cls, filter_args)

    def setup_projections(self, fused_bias_fc, inner_factor):
        "Initializes input and output projections (over the width dimension)"
        if fused_bias_fc and FusedDense is None:
            raise ImportError("fused_dense is not installed")
        linear_cls = nn.Linear if not fused_bias_fc else FusedDense
        self.out_proj = linear_cls(self.d_model * inner_factor, self.d_model)
        self.in_proj = linear_cls(self.d_model, (self.order + 1) * self.d_model)
        if self.post_order_ffn:
            self.ord_proj_w = nn.Parameter(
                torch.randn(self.order, self.num_heads, self.num_heads)
                / math.sqrt(self.head_dim)
            )

    def setup_filters(self, filter_cls, filter_args):
        "Initializes the explicit and implicit filters"
        assert self.order >= 2, f"Order must be at least 2, (got {self.order})"
        total_width = self.d_model * self.inner_factor * (self.order + 1)

        self.short_filter = nn.Conv1d(
            in_channels=total_width,
            out_channels=total_width,
            kernel_size=self.short_filter_order,
            groups=total_width,
            padding=self.short_filter_order - 1,
        )

        filter_cls = instantiate(registry.layer, filter_cls, partial=True)

        self.filter_fn = filter_cls(
            self.head_dim * self.inner_factor * (self.order - 1),
            d=self.head_dim,
            order=(self.order - 1),
            seq_len=self.l_max,
            **filter_args,
        )
        if self.jit_filter:
            self.filter_fn = torch.jit.script(self.filter_fn, self.L)

    def recurrence(self, u, state):
        "Fast inference mode via distilled recurrence"
        raise NotImplementedError("Working on it!")

    def forward(self, u, *args, **kwargs):
        l = u.size(-2)
        l_filter = min(l, self.l_max)
        u = self.in_proj(u)
        u = rearrange(u, "b l d -> b d l")

        uc = self.short_filter(u)[..., :l_filter]

        # head_dim = d_model // num_heads
        # (ho v) = (num_heads head_dim * (order + 1))
        # Default z = 1
        uc = rearrange(
            uc,
            "b (ho v) (z l) -> b ho v z l",
            z=self.num_blocks,
            ho=self.num_heads,
            v=self.head_dim * (self.order + 1),
        )

        *x, v = uc.split(self.d_model, dim=2)
        k = self.filter_fn.filter(
            l_filter
        )  # make the kernel real, more over, it's of shape (1, L, d * (order - 1))

        # `c` is always 1 by default
        k = rearrange(k, "c l (v o) -> c o v l", v=self.head_dim, o=self.order - 1)[0]

        bias = rearrange(
            self.filter_fn.bias, "(v o) -> o v", v=self.head_dim, o=self.order - 1
        )

        for o, x_i in enumerate(reversed(x[1:])):
            if self.outer_mixing:
                v = rearrange(v, "b h v z l -> b h 1 v z l")
                v = self.dropout(v * rearrange(x_i, "b h v z l -> b h v 1 z l"))
                v = v.sum(dim=2)
            else:
                v = self.dropout(v * x_i)

            # the bias term is broadcasted. Last dimension (l) is handled by fftconv
            v = self.filter_fn(v, l_filter, k=k[o], bias=bias[o, None, :, None])

            if self.post_order_ffn:
                w = self.ord_proj_w[o]
                v = mul_sum(
                    rearrange(w, "h1 h2 -> 1 h1 h2 1 1 1"),
                    rearrange(v, "b h v z l -> b h 1 v z l"),
                )

        y = self.activation(
            rearrange(
                v * x[0],
                "b h v z l -> b (z l) (h v)",
                z=self.num_blocks,
                h=self.num_heads,
            )
        )
        y = self.out_proj(y)

        if self.return_state:
            return y, None
        return y

    @property
    def d_output(self):
        return self.d_model