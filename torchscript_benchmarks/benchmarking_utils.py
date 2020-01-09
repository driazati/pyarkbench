import logging
import time
import datetime
import os
import argparse
import json
import gc
import statistics

from typing import Dict, Any

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.root.setLevel(logging.DEBUG)

args = None


def setup_args():
    global args
    parser = argparse.ArgumentParser(description="Run TorchScript benchmarks")
    parser.add_argument("--runs",
                        help="Number of times to run benchmarks",
                        default=10)

    parser.add_argument("--out",
                        help="Directory to write JSON output (filename is `YourClassName.json`)",
                        required=False)
    parser.add_argument("--stats",
                        nargs='*',
                        metavar='method',
                        help="Call functions from Python's `statistics` package instead of showing raw numbers (if no methods are provided, mean, median, and variance are computed)")

    parser.add_argument("--time",
                        help="Time of current commit (used by runner script)",
                        required=False)
    parser.add_argument("--pr", help="PR of current commit (used by runner script)", required=False)
    parser.add_argument("--hash",
                        help="Hash of current commit (used by runner script)",
                        required=False)

    args = parser.parse_args()
    return args


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


def clear_cache():
    mb_of_data = 3
    output = [i for i in range(mb_of_data * 1024 * 1024)]
    return list(map(lambda x: x + 1, output))


def cleanup():
    clear_cache()
    gc.collect()
    time.sleep(1)


def find_spot(data, commit):
    # Find the index in data where commit should be inserted, assuming data
    # is ordered by commit time
    # TODO: Make this a binary search
    if commit is None:
        return 0, True
    index = 0
    for d in data:
        entry_time = d["commit"]["time"]
        entry_time = datetime.datetime.strptime(entry_time,
                                                "%Y-%m-%dT%H:%M:%S%z")

        if d["commit"]["hash"] == commit.hash:
            return index, False

        if commit.time < entry_time:
            break

        index += 1

    return index, True


class Commit(object):
    def __init__(self, time, pr, hash):
        self.time = time
        self.pr = pr
        self.hash = hash

    def __repr__(self):
        parts = [str((key, str(self.__dict__[key]))) for key in self.__dict__]
        return '({})'.format(", ".join(parts))


class Benchmark(object):
    def __init__(self):
        # Parse arguments
        self.out_dir = args.out
        if args.stats is None:
            self.stats = None
        else:
            if len(args.stats) == 0:
                self.stats = ['mean', 'median', 'variance']
            else:
                self.stats = args.stats
            for stat in self.stats:
                assert getattr(statistics, stat) is not None
        if self.out_dir is None:
            if self.stats is not None:
                logging.warning("'--out' is not set, printing statistics to stdout")
            else:
                logging.warning("'--out' is not set, printing raw results to stdout")
        msg = "Cannot compute stats and save JSON to file, don't combine --out and --stats args"
        assert not (self.out_dir is not None and self.stats is not None), msg
        self.num_runs = int(args.runs)
        self.warmup_runs = 1

        # If provided on the command line, make a commit object for the results
        if not args.time or not args.hash or not args.pr:
            logging.info(
                "--time, --hash, or --pr not provided, commit is unknown")
            self.commit = None
        else:
            if args.time:
                time = datetime.datetime.strptime(args.time, "%Y-%m-%dT%H:%M:%S%z")
            else:
                time = ''
            commit = Commit(time, args.pr, args.hash)
            logging.info("Commit {}".format(commit))
            self.commit = commit

        # Get the output name for this test
        self.name = type(self).__name__.lower()

        if self.out_dir:
            json_name = "{}.json".format(self.name)
            self.output_filename = os.path.join(self.out_dir, json_name)
        else:
            self.output_filename = None

    def run(self) -> Dict[str, Any]:
        if not hasattr(self, 'num_runs'):
            raise RuntimeError("Call Benchmark.__init__() before run()")

        logging.info("Benchmarking '{name}', best of {runs} runs (with {warmup_runs} warmup runs)".format(
            name=self.name, runs=self.num_runs, warmup_runs=self.warmup_runs))

        now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S%z")

        for i in range(self.warmup_runs):
            self.benchmark()

        # Gather the results
        field_names = None
        results = {}
        cleanup()
        for i in range(self.num_runs):
            result = self.benchmark()
            if len(results) == 0:
                results = {key: [] for key in result.keys()}

            for key in result:
                results[key].append(result[key])
        cleanup()

        # Add the time the test was run to the results
        results["benchmark_run_at"] = str(now)

        if self.out_dir is None:
            # TODO: calculate statistics
            if self.stats is not None:
                stats = {}
                for name in results:
                    entry = results[name]
                    if isinstance(entry, list):
                        stats[name] = {}
                        for stat in self.stats:
                            stats[name][stat] = getattr(statistics, stat)(entry)
                    else:
                        stats[name] = results[name]
                print(json.dumps(stats, indent=2))
            else:
                print(json.dumps(results, indent=2))
        else:
            self.save_results(results)

    def save_results(self, results):
        """
        Save the results gathered from benchmarking and metadata about the commit
        to a JSON file named after the type of `self`.
        """
        logging.info("Saving results for {name} to {filename}".format(
            name=self.name, filename=self.output_filename))

        data = []
        spot = 0
        make_new_entry = True
        if os.path.exists(self.output_filename):
            with open(self.output_filename, 'r') as in_file:
                try:
                    data = json.load(in_file)
                    spot, make_new_entry = find_spot(data, self.commit)
                except json.decoder.JSONDecodeError as e:
                    logging.warning(
                        "Error decoding JSON, deleting existing content {}".
                        format(str(e)))

        if make_new_entry:
            entry = {}
            if self.commit:
                entry["commit"] = {
                    "pr": self.commit.pr,
                    "hash": self.commit.hash,
                    "time": self.commit.time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                }

            entry["runs"] = [results]
            data.insert(spot, entry)
        else:
            data[spot]["runs"].append(results)

        with open(self.output_filename, 'w') as out:
            json.dump(data, out, indent=2)

    def benchmark(self):
        raise NotImplementedError()
