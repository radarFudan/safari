Get stuck in building wheels for collected packages: dropout-layer-norm - use CUDA 11.7 runtime, resolved

`python evals/lambada.py --ckpt_path ./checkpoint/hyena_small_150b_tok.ckpt --data_dir ./data`

move the code into the parent folder
`python3 runtime_hyena_flashmha.py > results.txt`

Summarize:
listops,    multiclass_classification
imdb,       multiclass_classification
cifar,      multiclass_classification
aan,        multiclass_classification
pathfinder, multiclass_classification
pathx,      multiclass_classification

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

da2
`DATA_PATH=./data python -m train experiment=wt103/base`
unique-bush-49
Benchmark, TODO which model? size 40G

da3
`DATA_PATH=./data python -m train experiment=wt103/hyena`