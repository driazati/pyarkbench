# TorchScript Benchmarks

This repo consists of a series of benchmarks on common models used in TorchScript and
a runner that handles gathering and pushing results. For details, see the [website readme](https://github.com/driazati/driazati.github.io/tree/master/torchscript).


# Benchmarks

See the example in `benchmarks/basic/run.py` for a quick start. To run it, do any of the following

```bash
python benchmarks/basic/run.py
python benchmarks/basic/run.py --stats
python benchmarks/basic/run.py --stats mean
python benchmarks/basic/run.py --runs 100 --stats
python benchmarks/basic/run.py --out .
```

# Benchmark Runner

The runner will handle building a specific version of PyTorch and running your benchmark with that version. It is useful for things like backtesting performance on a model, but if you are just looking to try out a change, you shouldn't need to use it.

For a quick example, see [`examples/backtest.sh`](examples/backtest.sh).
