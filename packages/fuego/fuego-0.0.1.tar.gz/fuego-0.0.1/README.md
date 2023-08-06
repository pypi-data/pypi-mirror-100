# Fuego

## Getting Started

- clone the repo, `cd ` into it.
- start new virtual environment
- Install in dev mode `pip install -e .` (dont forget the `.` at the end)
- `cd examples`


```
fuego run \
    --gpu-type k80 \
    --num-gpus 1 \
example_autoencoder/run.py \
    --gpus 1 \
    --max_epochs 11 \
    --default_root_dir ./logs
```