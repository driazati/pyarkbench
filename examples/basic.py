from pyarkbench import Benchmark, Timer, default_args


class Basic(Benchmark):
    def benchmark(self):
        with Timer() as m1:
            pass

        with Timer() as m2:
            pass

        return {
            "Metric 1 (ms)": m1.ms_duration,
            "Metric 2 (ms)": m2.ms_duration,
        }

if __name__ == '__main__':
    bench = Basic(*default_args.bench())
    results = bench.run()
    bench.print_results(results)
    bench.print_stats(results, stats=default_args.stats())
    bench.save_results(results, out_dir=default_args.save())
