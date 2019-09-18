import logging
import time
import datetime
import torch
import os

from typing import Dict, Any

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
