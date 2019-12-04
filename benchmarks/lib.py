import logging
import time
import datetime
import torch
import os
import argparse
import gc

from typing import Dict, Any

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logging.root.setLevel(logging.DEBUG)


parser = argparse.ArgumentParser(description="Run TorchScript benchmarks")
parser.add_argument("--out", help="Directory to write CSVs to", required=False)
parser.add_argument("--time", help="Time of current commit", required=False)
parser.add_argument("--pr", help="PR of current commit", required=False)
parser.add_argument("--hash", help="Hash of current commit", required=False)
parser.add_argument("--runs", help="Number of times to run benchmarks", default=10)

args = parser.parse_args()


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


class Commit(object):
    def __init__(self, time, pr, hash):
        self.time = time
        self.pr = pr
        self.hash = hash


class Benchmark(object):
    out_dir = None
    commit = None
    num_runs = None

    def name(self):
        return type(self).__name__.lower()

    def output_filename(self):
        csv_name = "{}.csv".format(self.name())
        return os.path.join(self.out_dir, csv_name)

    def init(self):
        self.out_dir = args.out
        if args.time:
            commit_time = datetime.datetime.strptime(args.time, "%Y-%m-%dT%H:%M:%S%z")
        else:
            commit_time = ''
        self.num_runs = int(args.runs)
        self.commit = (commit_time, args.pr, args.hash)

    def clear_cache(self):
        mb_of_data = 3
        output = [i for i in range(mb_of_data * 1024 * 1024)]
        return list(map(lambda x: x + 1, output))

    def cleanup(self):
        self.clear_cache()
        gc.collect()
        time.sleep(1)

    def run(self) -> Dict[str, Any]:
        self.init()
        runs = self.num_runs
        warmup_runs = 1

        logging.info("Benchmarking '{name}', best of {runs} runs".format(name=self.name(), runs=runs))
        logging.info("Commit {}".format(self.commit))
        if self.out_dir is None:
            logging.warning("'--out' is not set, printing result to stdout")
        else:
            logging.info("Saving results to {out_dir}".format(out_dir=self.out_dir))

        # Save the minimum results to the output file
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        for i in range(warmup_runs):
            self.benchmark()

        # Gather the results
        field_names = None
        results = {}
        self.cleanup()
        for i in range(runs):
            result = self.benchmark()
            if len(results) == 0:
                results = {key: [] for key in result.keys()}

            for key in result:
                results[key].append(result[key])
        self.cleanup()

        if self.out_dir is None:
            # TODO: calculate statistics
            import pprint
            pprint.pprint(results)
        else:
            self.save_results(results, self.commit)

    def save_results(self, results, commit):
        # Open the file, check if the headers are present. If not, add them.
        # Then re-open the file, add the relevant data line
        logging.info(
            "Saving results for {name} to {filename}".format(name=self.name(), filename=self.output_filename()))

        if os.path.exists(self.output_filename()):
            existing_data = json.loads(open(self.output_filename(), 'r'))


    def benchmark(self):
        raise NotImplementedError()
