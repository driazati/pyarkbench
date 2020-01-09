from torchscript_benchmarks import Benchmark, Timer, setup_args


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
    # Setup command line args for this script
    setup_args()
    Basic().run()
