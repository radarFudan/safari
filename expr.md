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


`python -m train experiment=lra/long-conv-lra-pathfinder`

Benchmark


`python -m train experiment=lra/long-conv-lra-pathx`

Benchmark

