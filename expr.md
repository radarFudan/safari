0. Copy the lra dataset from state space
1. Try `python -m train experiment=lra/long-conv-lra-listops` - 15-00-08-397497
    Get the listops running
    **TODO** Implement the weighted loss for cross entropy
    **TODO** Implement the memory evaluation for listops task
    However, the listops does not output a sequence. 
    The good news is that it has an accuracy. 

2. Next I try to get the imdb running `python -m train experiment=lra/long-conv-lra-imdb`
    Just discovered the imdb is **multiclass-classification task**.
    It seems I should focus on the task with different loss and metric.
    sunny-lake-1 finished.
    Same as listops, need memory evaluation. 

3. Implement the weighted loss for mse
4. Running `python -m train experiment=lra/long-conv-lra-cifar`
    good-flower-2
    val loss 0.5045, val accuracy 87.58%
    Same as listops, need memory evaluation. 
    crashed - why

5. curious-serenity-3 `python -m train experiment=lra/long-conv-lra-aan`
    val loss 0.3485, val accuracy 84.96$%
    crashed
    Is the output sequential? 

6. easy-dew-4 `python -m train experiment=lra/long-conv-lra-pathfinder`
    Stopped as there is no pathfinder 32...
    (Failed)
    **TODO** Find the pathfinder 32, check silicon

7. Rerun for the trashing debug
    balmy-durian-5
    Currently no crash
    **running**

8. `python -m train experiment=synthetics/associative_recall/base.yaml`
    This is a base class

9. Should run 
    `python -m train experiment=synthetics/associative_recall/transformer`
    24
    `python -m train experiment=synthetics/associative_recall/transformer_wl0`
    25, 31
    `python -m train experiment=synthetics/associative_recall/transformer_wl2`
    26
    
    `python -m train experiment=synthetics/associative_recall/s4d`
    ethereal-serenity-27
    `python -m train experiment=synthetics/associative_recall/s4d_wl0`
    ruby-disco-28, 32
    `python -m train experiment=synthetics/associative_recall/s4d_wl2`
    vibrant-voice-29

    This task does not return sequence output...

    `python -m train experiment=synthetics/associative_recall/h3`
    *TODO*, bugged, jit.so bug
    30

10 `python -m train experiment=synthetics/associative_recall/hyena-131k-30vs.yaml`
    33, 34
    I tried two machines, but it's strange that the utilization of GPU is 0 and the experiment is running very slow. 
    What's next?
