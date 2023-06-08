## Environment required:

CUDA11.7, driver 450.172(+) or 470.82(+)

## Evaluation with hyena

`python evals/lambada.py --ckpt_path ./checkpoint/hyena_small_150b_tok.ckpt --data_dir ./data`

move the code into the parent folder
`python3 runtime_hyena_flashmha.py > results.txt`

## Long range arena

Summarize:
listops, multiclass_classification
imdb, multiclass_classification
cifar, multiclass_classification
aan, multiclass_classification
pathfinder, multiclass_classification
pathx, multiclass_classification

`python -m train experiment=lra/long-conv-lra-listops`

olive-puddle-24
Benchmark

`python -m train experiment=lra/long-conv-lra-imdb`

clean-hill-26
Benchmark

`python -m train experiment=lra/long-conv-lra-cifar`

fallen-frost-27
Benchmark

`python -m train experiment=lra/long-conv-lra-aan`

faithful-sponge-29
Benchmark

`python -m train experiment=lra/long-conv-lra-pathfinder`
charmed-dragon-32
Benchmark, size 6G

`python -m train experiment=lra/long-conv-lra-pathx`
lyric-mountain-31
Benchmark, size 24G
Val Accuracy, 97.57%
Interesting thing is the val accuracy is monotonic increasing but the val loss is not monotonic

## Wikitext103

`DATA_PATH=./data python -m train experiment=wt103/base`
unique-bush-49
Benchmark, which model, seems to be SSM+attention size 40G
Val perplexity, 1.006

`DATA_PATH=./data python -m train experiment=wt103/hyena`
icy-fog-55, morning-river-60
Benchmark, use the model from evaluation on wt103 setting,

`CUDA_VISIBLE_DEVICES=0 DATA_PATH=./data python -m train experiment=wt103/hyenassm`
brisk-wave-58, atomic-breeze-61
Constant in $h$, killed by timeout

`CUDA_VISIBLE_DEVICES=1 DATA_PATH=./data python -m train experiment=wt103/hyenassm_debug`
deft-spaceship-59, dazzling-leaf-62
SSM in $h$, killed by timeout

`CUDA_VISIBLE_DEVICES=0 DATA_PATH=./data python -m train experiment=wt103/hyena_reproduce`
devoted-totem-63
with 125M version Hyena

`CUDA_VISIBLE_DEVICES=0 DATA_PATH=./data python -m train experiment=wt103/hyena_reproduce trainer.max_epochs=200 train.ckpt="/home/aiops/wangsd/github/safari-Hazy/outputs/2023-05-24/10-23-01-537515/checkpoints/last.ckpt" optimizer.lr=0.0001 optimizer.weight_decay=0`
restful-plant-64
5 epochs, smaller learning rate(0.0001), no effects, stopped

`CUDA_VISIBLE_DEVICES=0 DATA_PATH=./data python -m train experiment=wt103/hyena_reproduce trainer.max_epochs=200 train.ckpt="/home/aiops/wangsd/github/safari-Hazy/outputs/2023-05-24/10-23-01-537515/checkpoints/last.ckpt" optimizer.lr=0.0006 optimizer.weight_decay=0.1 optimizer.betas=[0.9,0.98]`
eager-yogurt 66, same weight decay

`CUDA_VISIBLE_DEVICES=0 DATA_PATH=./data python -m train experiment=wt103/hyena_reproduce trainer.max_epochs=200 train.ckpt="/home/aiops/wangsd/github/safari-Hazy/outputs/2023-05-24/09-26-37-278987/checkpoints/last.ckpt" optimizer.lr=0.0006 optimizer.weight_decay=0.1 optimizer.betas=[0.9,0.98]`
67?

Current schedule: reproduce the hyena:

1. Check the base transformer dataset
   `CUDA_VISIBLE_DEVICES=0,1 DATA_PATH=./data python -m train experiment=wt103/base`
   Check with the transformer-xl, the data is correct
   unique-oath-70, long-conv

`DATA_PATH=./data python -m train experiment=synthetics/induction_head/transformer`
87

`DATA_PATH=./data python -m train experiment=wt103/transformer`
dainty-deluge-88, ethereal-sun-93
train loss 2.88, preplexity 17.851, test loss 3.23, perplexity 25
train loss 2.84, preplexity 17.15008, test loss 3.25, perplexity 25.98

`DATA_PATH=./data python -m train experiment=wt103/transformer`

Consider add layers from 2 to 12, attention layers still [0, 1]
rural-brook-91, overfitted
train loss, perplexity, test loss, perplexity

`DATA_PATH=./data python -m train experiment=wt103/transformer`

layers 12, attention at [1, 8]
worthy-jazz-92, overfitted
train loss, perplexity, test loss, perplexity

`DATA_PATH=./data python -m train experiment=wt103/transformer`

layers 12, attention at [1, 8]
manually add causal constraints
radiant-thunder-104
