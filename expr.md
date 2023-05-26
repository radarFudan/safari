Get stuck in building wheels for collected packages: dropout-layer-norm - use CUDA 11.7 runtime, resolved

`python evals/lambada.py --ckpt_path ./checkpoint/hyena_small_150b_tok.ckpt --data_dir ./data`

move the code into the parent folder
`python3 runtime_hyena_flashmha.py > results.txt`

Summarize:
listops, multiclass_classification
imdb, multiclass_classification
cifar, multiclass_classification
aan, multiclass_classification
pathfinder, multiclass_classification
pathx, multiclass_classification

da2:
`python -m train experiment=lra/long-conv-lra-listops`
olive-puddle-24
Benchmark

da:
`python -m train experiment=lra/long-conv-lra-imdb`
clean-hill-26
Benchmark

da3:
`python -m train experiment=lra/long-conv-lra-cifar`
fallen-frost-27
Benchmark

da2
`python -m train experiment=lra/long-conv-lra-aan`
faithful-sponge-29
Benchmark

da3
`python -m train experiment=lra/long-conv-lra-pathfinder`
charmed-dragon-32
Benchmark, size 6G

da
`python -m train experiment=lra/long-conv-lra-pathx`
lyric-mountain-31
Benchmark, size 24G
Val Accuracy, 97.57%
Interesting thing is the val accuracy is monotonic increasing but the val loss is not monotonic

da2
`DATA_PATH=./data python -m train experiment=wt103/base`
unique-bush-49
Benchmark, which model, seems to be SSM+attention size 40G
Val perplexity, 1.006

da2
`DATA_PATH=./data python -m train experiment=wt103/hyena`
icy-fog-55, morning-river-60
Benchmark, use the model from evaluation on wt103 setting,

dagen2 - card 0
`CUDA_VISIBLE_DEVICES=0 DATA_PATH=./data python -m train experiment=wt103/hyenassm`
brisk-wave-58, atomic-breeze-61
Constant in $h$

`CUDA_VISIBLE_DEVICES=1 DATA_PATH=./data python -m train experiment=wt103/hyenassm_debug`
deft-spaceship-59, dazzling-leaf-62
SSM in $h$

`CUDA_VISIBLE_DEVICES=0 DATA_PATH=./data python -m train experiment=wt103/hyena_reproduce wandb=null`
devoted-totem-63
with 125M version Hyena
