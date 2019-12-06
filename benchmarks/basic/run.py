from typing import Any, Dict

import torch
from lib import Benchmark, Timer

import sys
import argparse
import datetime


class Basic(Benchmark):
    def benchmark(self) -> Dict[str, Any]:
        with Timer() as m1:
            pass

        with Timer() as m2:
            pass

        return {
            "Metric 1 (ms)": m1.ms_duration,
            "Metric 2 (ms)": m2.ms_duration,
        }

if __name__ == '__main__':
    Basic().run()
