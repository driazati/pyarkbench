This library is intended to make it easy to write small benchmarks and view the results.

# Usage

See [examples/basic.py](examples/basic.py) for a full working example.

```python
from pybench import Benchmark, Timer, default_args

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

## `Timer`

## `default_args`