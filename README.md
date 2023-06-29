# Reproducing Hyena

## How to reproduce hyena?

### Environment

This repository requires Python 3.9 and Pytorch 1.13.
Other packages are listed in [requirements.txt](./requirements.txt).

### Configs

Notice that the wikitext-103 [base configuration](./configs/experiment/wt103/base.yaml) cannot be directly used as it only set the attention to be the first and 8th layer, while the rest layer might be empty layers (not sure).

## Acknowledgements

This repo was forked from Albert Gu's [state spaces](https://github.com/HazyResearch/state-spaces) repo and borrows its structure.
It also contains code from the [FlashAttention](https://github.com/HazyResearch/flash-attention) training scripts.
