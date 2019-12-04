from typing import Any, Dict

import torch
# import torchvision
import resnet
from lib import Benchmark, Timer

import sys
import argparse
import datetime

class Basic(Benchmark):
    def benchmark(self) -> Dict[str, Any]:
        with Timer() as eager_time:
            pass

        with Timer() as compilation_time:
            pass

        with Timer() as script_exec_time:
            pass

        return {
            "Eager Runtime (ms)": eager_time.ms_duration,
            "Compilation Time (ms)": compilation_time.ms_duration,
            "Script Runtime (ms)": script_exec_time.ms_duration,
        }

class Resnet50(Benchmark):
    def benchmark(self) -> Dict[str, Any]:
        eager_resnet = resnet.resnet50(pretrained=False)
        sample_inputs = torch.randn(1, 3, 224, 224)

        with Timer() as eager_time:
            eager_resnet(sample_inputs)

        with Timer() as compilation_time:
            script_resnet = torch.jit.script(eager_resnet)

        with Timer() as script_exec_time:
            script_resnet(sample_inputs)

        for _ in range(10):
            script_resnet(sample_inputs)

        with Timer() as tenth_script_exec_time:
            script_resnet(sample_inputs)

        # with Timer() as script_exec_time:
        #     script_resnet.to('cuda')(sample_inputs)

        return {
            "Eager Runtime (ms)": eager_time.ms_duration,
            "Compilation Time (ms)": compilation_time.ms_duration,
            "Script Runtime (ms)": script_exec_time.ms_duration,
            "10th Script Runtime (ms)": tenth_script_exec_time.ms_duration,
        }


parser = argparse.ArgumentParser(description="Run TorchScript benchmarks")
parser.add_argument("--out", help="Directory to write CSVs to", required=False)
parser.add_argument("--time", help="Time of current commit", required=False)
parser.add_argument("--pr", help="PR of current commit", required=False)
parser.add_argument("--runs", help="Number of times to run benchmarks", default=10)

args = parser.parse_args()

if __name__ == '__main__':
    if sys.version_info < (3, 7):
        raise RuntimeError("Python 3.7 or greater required")

    #Basic().run()
    Resnet50().run()
