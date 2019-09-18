from typing import Any, Dict

import torch
# import torchvision
import resnet
from lib import Benchmark, Timer

import sys


class Resnet50(Benchmark):
    def benchmark(self) -> Dict[str, Any]:
        eager_resnet = resnet.resnet50(pretrained=False)
        sample_inputs = torch.randn(1, 3, 224, 224)

        with Timer() as eager_time:
            eager_resnet(sample_inputs)
            pass

        with Timer() as compilation_time:
            script_resnet = torch.jit.script(eager_resnet)
            pass

        with Timer() as script_exec_time:
            script_resnet(sample_inputs)
            pass

        return {
            "eager_time": eager_time.duration,
            "compilation_time": compilation_time.duration,
            "script_exec_time": script_exec_time.duration,
        }


if __name__ == '__main__':
    if sys.version_info < (3, 7):
        raise RuntimeError("Python 3.7 or greater required")
    out_dir = sys.argv[1]
    Resnet50().run()
