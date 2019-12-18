from typing import Any, Dict

import torch
from torchscript_benchmarks import Benchmark, Timer, setup_args


import torchvision


class MaskRCNN(Benchmark):
    def benchmark(self) -> Dict[str, Any]:
        print("Starting")
        eager_model = torchvision.models.detection.maskrcnn_resnet50_fpn(num_classes=50, pretrained=False)
        eager_model.eval()
        sample_inputs = torch.randn(1, 3, 300, 300)

        with Timer() as eager_time:
            eager_model(sample_inputs)

        with Timer() as compilation_time:
            script_model = torch.jit.script(eager_model)

        with Timer() as script_exec_time:
            script_model(sample_inputs)

        for _ in range(10):
            script_model(sample_inputs)

        with Timer() as tenth_script_exec_time:
            script_model(sample_inputs)

        return {
            "Eager Runtime (ms)": eager_time.ms_duration,
            "Compilation Time (ms)": compilation_time.ms_duration,
            "Script Runtime (ms)": script_exec_time.ms_duration,
            "10th Script Runtime (ms)": tenth_script_exec_time.ms_duration,
        }

if __name__ == '__main__':
    setup_args()
    MaskRCNN().run()
