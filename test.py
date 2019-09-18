
from contextlib import contextmanager
from typing import List, Optional
from collections import OrderedDict
from typing import List, Any, Dict

import time
import functools
import datetime
import math
import sys
import os
import logging


import torch
import torch.nn as nn
# import torchvision
import resnet


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logging.root.setLevel(logging.DEBUG)

out_dir = None

class Timer(object):
    def __enter__(self):
        self.start = time.perf_counter_ns()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter_ns()
        self.duration = (self.end - self.start) / 1000 / 1000


class Benchmark(object):
    def name(self):
        return type(self).__name__.lower()

    def output_filename(self):
        csv_name = "{}.csv".format(self.name())
        return os.path.join(out_dir, csv_name)

    def run(self) -> Dict[str, Any]:
        runs = 3

        logging.info("Benchmarking {name}, best of {runs} runs".format(name=self.name(), runs=runs))

        # Gather the results
        field_names = None
        results = []
        for _ in range(runs):
            result = self.benchmark()
            if field_names is None:
                field_names = result.keys()
            else:
                assert field_names == result.keys()
            results.append(result.values())
        field_names = tuple(field_names)

        # Find the minimum of all runs
        min_results = results[0]
        for index, result in enumerate(results[1:]):
            if not isinstance(result, (int, float)):
                continue
            if min_results[index] > result:
                min_results[index] = result
        min_results = tuple(min_results)

        # Save the minimum results to the output file
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        metadata = (now, torch.version.git_version)
        self.save_results(("time", "git_hash") + field_names, metadata + min_results)

    def save_results(self, field_names, results):
        # Open the file, check if the headers are present. If not, add them.
        # Then re-open the file, add the relevant data line
        logging.info("Saving results for {name}".format(name=self.name()))
        add_headers = False
        if not os.path.exists(self.output_filename()):
            add_headers = True
        else:
            with open(self.output_filename(), 'r') as f:
                line = f.readline()
                if line == '':
                    # No headers present
                    add_headers = True

        results = map(lambda x: str(x), results)
        with open(self.output_filename(), 'a+') as f:
            if add_headers:
                f.write(",".join(field_names) + "\n")
            f.write(",".join(results) + "\n")

    def benchmark(self):
        raise NotImplementedError()


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
