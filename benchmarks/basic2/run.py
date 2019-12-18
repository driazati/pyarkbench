from typing import Any, Dict

from torchscript_benchmarks import Benchmark, Timer, setup_args


class Basic2(Benchmark):
    def benchmark(self) -> Dict[str, Any]:
        with Timer() as m1:
            pass

        with Timer() as m2:
            pass

        return {
            "Another Metric 1 (ms)": m1.ms_duration,
            "Another Metric 2 (ms)": m2.ms_duration,
        }

if __name__ == '__main__':
    setup_args()
    Basic2().run()
