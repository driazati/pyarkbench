# TorchScript Benchmarks

This repo consists of a series of benchmarks on common models used in TorchScript and
a runner that handles gathering and pushing results.

## Benchmarks

Write a benchmark like in [`benchmarks/test.py`](benchmarks/test.py), add a call to it in `main`.

## Runner

This is a script to build PyTorch (`./builder.sh`) and run the benchmarks.

The runner should be started via [Anacron](https://en.wikipedia.org/wiki/Anacron) like so

```bash
anacron -t 0 3 * * * ./runner.sh
```
