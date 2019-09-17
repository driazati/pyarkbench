# TorchScript Benchmarks

This repo consists of a series of benchmarks on common models used in TorchScript and
a runner that handles gathering and pushing results.

## Benchmarks

????

## Runner

This is a short script to run the benchmarks. At 3 AM PDT each night, the runner builds PyTorch and runs the benchmarks. It assumes the benchmarks write their outputs to CSV files located where the script is run. The runner will copy these CSV files to the submodule repo
and push them. The webpage in the submodule repo pulls the CSV files each time, so as soon as GitHub pages
updates the website the new results should be viewable at [driazati.github.io/torchscript](driazati.github.io/torchscript).

The runner should be started via [Anacron](https://en.wikipedia.org/wiki/Anacron) like so

```bash
anacron -t 0 3 * * * ./runner.sh
```
