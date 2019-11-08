import logging
import time
import datetime
import torch
import os
import argparse
import json

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

    def __repr__(self):
        parts = [str((key, str(self.__dict__[key]))) for key in self.__dict__]
        return '({})'.format(", ".join(parts))


class Benchmark(object):
    out_dir = None
    commit = None
    num_runs = None

    def name(self):
        return type(self).__name__.lower()

    def output_filename(self):
        csv_name = "{}.json".format(self.name())
        return os.path.join(self.out_dir, csv_name)

    def init(self):
        self.out_dir = args.out
        if args.time:
            time = datetime.datetime.strptime(args.time, "%Y-%m-%dT%H:%M:%S%z")
        else:
            time = ''
        return Commit(time, args.pr, args.hash)

    def run(self) -> Dict[str, Any]:
        commit = self.init()
        runs = int(args.runs)

        logging.info("Benchmarking '{name}', best of {runs} runs".format(name=self.name(), runs=runs))
        logging.info("Commit {}".format(commit))
        if self.out_dir is None:
            logging.warning("'--out' is not set, printing result to stdout")


        now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S%z")

        # Gather the results
        field_names = None
        results = {}
        for i in range(runs):
            result = self.benchmark()
            if len(results) == 0:
                results = {key: [] for key in result.keys()}

            for key in result:
                results[key].append(result[key])

        # Add the time the test was run to the results
        results["benchmark_run_at"] = str(now)


        if self.out_dir is None:
            # TODO: calculate statistics
            import pprint
            pprint.pprint(results)
        else:
            self.save_results(results, commit)

    def find_spot(self, data, commit):
        # Find the index in data where commit should be inserted, assuming data
        # is ordered by commit time
        # TODO: Make this a binary search
        index = 0
        for d in data:
            entry_time = d["commit"]["time"]
            entry_time = datetime.datetime.strptime(entry_time, "%Y-%m-%dT%H:%M:%S%z")

            if d["commit"]["hash"] == commit.hash:
                return index, False

            if commit.time < entry_time:
                break

            index += 1

        return index, True


    def save_results(self, results, commit):
        # Open the file, check if the headers are present. If not, add them.
        # Then re-open the file, add the relevant data line
        assert commit is not None
        logging.info(
            "Saving results for {name} to {filename}".format(name=self.name(), filename=self.output_filename()))

        data = []
        spot = 0
        make_new_entry = True
        if os.path.exists(self.output_filename()):
            with open(self.output_filename(), 'r') as in_file:
                try:
                    data = json.load(in_file)
                    spot, make_new_entry = self.find_spot(data, commit)
                except json.decoder.JSONDecodeError as e:
                    logging.warning("Error decoding JSON, deleting existing content {}".format(str(e)))

        if make_new_entry:
            entry = {
                "commit": {
                    "pr": commit.pr,
                    "hash": commit.hash,
                    "time": commit.time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                },
                "runs": [results]
            }
            data.insert(spot, entry)
        else:
            data[spot]["runs"].append(results)


        with open(self.output_filename(), 'w') as out:
            json.dump(data, out, indent=2)


    def benchmark(self):
        raise NotImplementedError()
