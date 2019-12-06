from typing import Any, Dict

import torch
# import torchvision
import resnet
from lib import Benchmark, Timer

import sys
import argparse
import datetime


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

        return {
            "Eager Runtime (ms)": eager_time.ms_duration,
            "Compilation Time (ms)": compilation_time.ms_duration,
            "Script Runtime (ms)": script_exec_time.ms_duration,
            "10th Script Runtime (ms)": tenth_script_exec_time.ms_duration,
        }

if __name__ == '__main__':
    # Basic().run()
    Resnet50().run()
