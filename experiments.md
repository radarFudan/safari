Adding `wandb=null` to any command line turns off logging.

Some of these datasets may require downloading and preparing data, documented in the [src/dataloaders](./src/dataloaders/) subdirectory.

## Long Range Arena (LRA)

You can use these configs to reproduce the best results on LRA using a random initialization.

```
python -m train experiment=lra/long-conv-lra-listops
python -m train experiment=lra/long-conv-lra-imdb
python -m train experiment=lra/long-conv-lra-cifar
python -m train experiment=lra/long-conv-lra-aan
python -m train experiment=lra/long-conv-lra-pathfinder
python -m train experiment=lra/long-conv-lra-pathx
```

## Language Modeling Synthetics

You can use these commands to run synthetics from the H3 paper:
```
python -m train experiment=synthetics/associative_recall/transformer
python -m train experiment=synthetics/associative_recall/s4d
python -m train experiment=synthetics/associative_recall/h3

python -m train experiment=synthetics/induction_head/transformer
python -m train experiment=synthetics/induction_head/s4d
python -m train experiment=synthetics/induction_head/h3
```

You should get scores >97 for Transformer and H3 for both tasks, and worse scores for S4D.

Note that the train accuracy is being computed over the entire sequence.
If you swap it out with another layer and train accuracy goes to 100, that probably means that your layer is non-causal. 
This is a common failure mode of models tested on these synthetics, consider testing causality numerically (e.g. checking whether gradients
only flow "backwards in time" i.e. 
$$\forall j > i: \frac{\partial y_i}{\partial x_j} \approx 0$$

To run the synthetics from the Hyena paper, you can use these commands:
```
python -m train experiment=synthetics/associative_recall/hyena-131k-30vs.yaml 
```
You can also customize sequence length and vocabulary sizes directly through the command line (or by creating a custom config).
We recommend a quick run with vocabulary size 10 and sequence length 256 to verify the pipeline is working correctly
```
python -m train experiment=synthetics/associative_recall/ dataset.input_seq_len=$SEQ_LEN dataset.vocab_size=$VOCAB_SIZE dataset.data_idr=$DATA_DIR
```
Note that dataset generation for >100k sequence lengths can take a while. If you pass a DATA_DIR to the script, the dataset will be saved after generation, and loaded for any other run with the same sequence length and vocabulary size.

Hyena (2 layers) should reach >90 accuracy on the 30 vocabulary size, 131k sequence length associative recall task ([here:](https://api.wandb.ai/links/zymrael/pnw1nckm) for an example wandb log). Other models should get worse scores (Transformers will be a pain to train on 131k, good luck!).


## Downstream Evaluations

Hyena small checkpoint is available at `https://huggingface.co/Zymrael/hyena-small-150b-tok`.
Download directly and move to CKPT_PATH.

To evaluate your language model on LAMBADA (OpenAI preprocessing with full last word accuracy, see: https://github.com/EleutherAI/lm-evaluation-harness/issues/356 and https://github.com/openai/gpt-2/issues/131#issuecomment-497136199 for differences between LAMBADA versions).

```
CUDA_VISIBLE_DEVICES=$ID python evals/lambada.py --ckpt_path $CKPT_PATH --data_dir $DATA_DIR
```
Dataset should first be downloaded from `https://openaipublic.blob.core.windows.net/gpt-2/data/lambada_test.jsonl` and saved to `$DATA_DIR/lambada/lambada_openai/lambada_test.jsonl`.

To evaluate additional models, write a custom `eval` config in `src/configs/evals/`. 

For Hyena small (153M, trained for 150B tokens), you should see `32.95` accuracy without stop word filter and `44.30` with stop word filter.  
