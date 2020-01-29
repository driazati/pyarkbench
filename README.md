This library is intended to make it easy to write small benchmarks and view the results.

- [Usage](#usage)
- [API](#api)
  * [`Benchmark`](#benchmark)
    + [`benchmark`](#benchmark)
    + [`run`](#run)
    + [`print_results`](#print-results)
    + [`print_stats`](#print-stats)
    + [`save_results`](#save-results)
  * [`cleanup`](#cleanup)
  * [`default_args`](#default-args)
    + [`bench`](#bench)
    + [`stats`](#stats)
    + [`save`](#save)
  * [`Timer`](#timer)
  * [`Commit`](#commit)
- [Developer Notes](#developer-notes)

# Usage

See [examples/basic.py](examples/basic.py) for a full working example.

```python
from pyarkbench import Benchmark, Timer, default_args

class Basic(Benchmark):
    def benchmark(self):
        with Timer() as m1:
            # Do some stuff
            pass

        with Timer() as m2:
            # Do some other stuff
            pass

        return {
            "Metric 1 (ms)": m1.ms_duration,
            "Metric 2 (ms)": m2.ms_duration,
        }

if __name__ == '__main__':
    # Initialize the benchmark and use the default command line args
    bench = Basic(*default_args.bench())

    # Run the benchmark (will run your code in `benchmark` many times, some to warm up and then some where the timer results are save)
    results = bench.run()

    # View the raw results
    bench.print_results(results)

    # See aggregate statistics about the results
    bench.print_stats(results, stats=default_args.stats())

    # Save the results to a JSON file named based on the benchmark class
    bench.save_results(results, out_dir=default_args.save())
```

# API

## `Benchmark`
```python
Benchmark(self, num_runs: int = 10, warmup_runs: int = 1, quiet: bool = False, commit: pybench.benchmarking_utils.Commit = None)
```

Benchmarks should extend this class and implement the `benchmark` method.

### `benchmark`
```python
Benchmark.benchmark(self) -> Dict[str, float]
```

This method must be implemented in your subclass and returns a dictionary
of metric name to the time captured for that metric.

### `run`
```python
Benchmark.run(self) -> Dict[str, Any]
```

This is the entry point into your benchmark. It will first run `benchmark()`
`self.warmup_runs` times without using the resulting timings, then it will
run `benchmark()` `self.num_runs` times and return the resulting timings.

### `print_results`
```python
Benchmark.print_results(self, results)
```

Pretty print the raw results by JSON dumping them.

### `print_stats`
```python
Benchmark.print_stats(self, results, stats=('mean', 'median', 'variance'))
```

Collects and prints statistics over the results.

### `save_results`
```python
Benchmark.save_results(self, results, out_dir, filename=None)
```

Save the results gathered from benchmarking and metadata about the commit
to a JSON file named after the type of `self`.

## `cleanup`
```python
cleanup()
```

Churn through a bunch of data, run the garbage collector, and sleep for a
second to "reset" the Python interpreter.

## `default_args`
```python
default_args(self, /, *args, **kwargs)
```

Adds a bunch of default command line arguments to make orchestrating
benchmark runs more convenient. To see all the options, call
`default_args.init()` and run the script with the `--help` option.

### `bench`
```python
default_args.bench()
```

Default arguments to be passed to a `Benchmark` object

### `stats`
```python
default_args.stats()
```

Default arguments to be passed to the `Benchmark.print_stats` method

### `save`
```python
default_args.save()
```

Default arguments to be passed to the `Benchmark.save_results` method

## `Timer`
```python
Timer(self, /, *args, **kwargs)
```

Context manager object that will time the execution of the statements it
manages.
    `self.start` - start time
    `self.end` - end time
    `self.ms_duration` - end - start / 1000 / 1000

## `Commit`
```python
Commit(self, time, pr, hash)
```

Wrapper around a git commit

# Developer Notes

To build this package locally, check it out and run

```bash
python setup.py develop
```

To rebuild these docs, run

```bash
pip install pydoc-markdown
pydocmd simple pybench.Benchmark+ pybench.cleanup pybench.default_args+ pybench.Timer pybench.Commit
```