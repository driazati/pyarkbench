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


class Timer(object):
    def __enter__(self):
        self.start = time.perf_counter_ns()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter_ns()
        self.ms_duration = (self.end - self.start) / 1000 / 1000


def print_table(data):
    if len(data) == 0:
        return
    widths = [0 for word in data[0]]
    for row in data:
        for index, word in enumerate(row):
            word = str(word)
            if widths[index] < len(word):
                widths[index] = len(word)
    formats = ["{{: <{}}}".format(width) for width in widths]
    format_string = " ".join(formats)
    for row in data:
        print(format_string.format(*row))


class Benchmark(object):
    out_dir = None
    commit_time = None
    commit_pr = None
    num_runs = None

    def name(self):
        return type(self).__name__.lower()

    def output_filename(self):
        csv_name = "{}.csv".format(self.name())
        return os.path.join(self.out_dir, csv_name)

    def run(self) -> Dict[str, Any]:
        runs = self.num_runs

        logging.info("Benchmarking {name}, best of {runs} runs".format(name=self.name(), runs=runs))
        if self.out_dir is None:
            logging.warning("out_dir is not set, printing result to stdout")
        else:
            logging.info("Saving results to {out_dir}".format(out_dir=self.out_dir))

        # Save the minimum results to the output file
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        commit_time = self.commit_time if self.commit_time else ''
        commit_pr = self.commit_pr if self.commit_pr else ''
        metadata = (now, commit_time, commit_pr, torch.version.git_version)
        metadata_names = ("benchmark_time", "commit_time", "commit_pr", "git_hash")

        # Gather the results
        field_names = None
        results = []
        for i in range(runs):
            result = self.benchmark()
            if field_names is None:
                field_names = result.keys()
            else:
                assert field_names == result.keys()
            results.append([i] + list(result.values()))
        field_names = ['run_number'] + list(field_names)

        if self.out_dir is None:
            # TODO: calculate statistics
            results.insert(0, field_names)
            print_table(results)
        else:
            metadata_and_results = list(map(lambda x: metadata + tuple(x), results))
            self.save_results(metadata_names + tuple(field_names), metadata_and_results)

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

        # results = list(map(lambda x: str(x), results))
        with open(self.output_filename(), 'a+') as f:
            if add_headers:
                f.write(",".join(field_names) + "\n")
            for result in results:
                result = list(map(lambda x: str(x), result))
                f.write(",".join(result) + "\n")

    def benchmark(self):
        raise NotImplementedError()
