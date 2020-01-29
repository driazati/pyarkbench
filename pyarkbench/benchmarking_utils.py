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


DEFAULT_ARGS = {
    'num_runs': 10,
    'warmup_runs': 1,
}


class default_args():
    """
    Adds a bunch of default command line arguments to make orchestrating
    benchmark runs more convenient. To see all the options, call
    `default_args.init()` and run the script with the `--help` option.
    """
    parser = None

    def init():
        default_args.parser = argparse.ArgumentParser(description="Run benchmarks")
        default_args.parser.add_argument("--num_runs",
                            help="Number of times to run benchmarks",
                            default=DEFAULT_ARGS['num_runs'],
                            type=int)
        default_args.parser.add_argument("--warmup_runs",
                            help="Number of times to warm up benchmarks (run without recording times)",
                            default=DEFAULT_ARGS['warmup_runs'],
                            type=int)

        default_args.parser.add_argument("--out",
                            help="Directory to write JSON output (filename is `YourClassName.json`)",
                            required=False)
        default_args.parser.add_argument("--stats",
                            nargs='*',
                            metavar='method',
                            help="Call functions from Python's `statistics` package instead of showing raw numbers (if no methods are provided, mean, median, and variance are computed)")

        default_args.parser.add_argument("--time",
                            help="Time of current commit (used by runner script)",
                            required=False)
        default_args.parser.add_argument("--pr", help="PR of current commit (used by runner script)", required=False)
        default_args.parser.add_argument("--hash",
                            help="Hash of current commit (used by runner script)",
                            required=False)
        default_args.parser.add_argument("--quiet",
                            help="Disable logging",
                            required=False,
                            action='store_true')
        return default_args.parser.parse_args()

    @staticmethod
    def bench():
        """
        Default arguments to be passed to a `Benchmark` object
        """
        args = default_args.init()
        commit = None
        if args.time and args.pr and args.hash:
            commit = Commit(args.time, args.pr, args.hash)
        return [args.num_runs, args.warmup_runs, args.quiet, commit]
    
    @staticmethod
    def stats():
        """
        Default arguments to be passed to the `Benchmark.print_stats` method
        """
        args = default_args.init()
        if args.stats is None or len(args.stats) == 0:
            return ('mean', 'median', 'variance')
        return args.stats

    @staticmethod
    def save():
        """
        Default arguments to be passed to the `Benchmark.save_results` method
        """
        args = default_args.init()
        if args.out is None:
            return os.getcwd()
        return args.out


class Timer(object):
    """
    Context manager object that will time the execution of the statements it
    manages.
        `self.start` - start time
        `self.end` - end time
        `self.ms_duration` - end - start / 1000 / 1000
    """
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
    """
    Churn through a bunch of data, run the garbage collector, and sleep for a
    second to "reset" the Python interpreter.
    """
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
    """
    Wrapper around a git commit
    """
    def __init__(self, time, pr, hash):
        if isinstance(time, str):
            time = datetime.datetime.strptime(args.time, "%Y-%m-%dT%H:%M:%S%z")
        self.time = time
        self.pr = pr
        self.hash = hash

    def __repr__(self):
        parts = [str((key, str(self.__dict__[key]))) for key in self.__dict__]
        return '({})'.format(", ".join(parts))


class Benchmark(object):
    """
    Benchmarks should extend this class and implement the `benchmark` method.
    """
    def __init__(self, num_runs: int=DEFAULT_ARGS['num_runs'], warmup_runs: int=DEFAULT_ARGS['warmup_runs'], quiet: bool=False, commit: Commit=None):
        # Parse arguments
        if quiet:
            logging.getLogger().disabled = True
        assert isinstance(num_runs, int), "Expected num_runs to be an int but got {}".format(type(num_runs))
        assert isinstance(warmup_runs, int), "Expected warmup_runs to be an int but got {}".format(type(warmup_runs))

        self.num_runs = num_runs
        self.warmup_runs = warmup_runs
        self.commit = commit

        # Get the output name for this test
        self.name = type(self).__name__.lower()

    def benchmark(self) -> Dict[str, float]:
        """
        This method must be implemented in your subclass and returns a dictionary
        of metric name to the time captured for that metric.
        """
        raise NotImplementedError()

    def run(self) -> Dict[str, Any]:
        """
        This is the entry point into your benchmark. It will first run `benchmark()`
        `self.warmup_runs` times without using the resulting timings, then it will
        run `benchmark()` `self.num_runs` times and return the resulting timings.
        """
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

        return results
        
    def print_results(self, results):
        """
        Pretty print the raw results by JSON dumping them.
        """
        print(json.dumps(results, indent=2))
        
    def print_stats(self, results, stats=('mean', 'median', 'variance')):
        """
        Collects and prints statistics over the results.
        """
        stat_values = {}
        for name in results:
            entry = results[name]
            if isinstance(entry, list):
                stat_values[name] = {}
                for stat in stats:
                    stat_values[name][stat] = getattr(statistics, stat)(entry)
            else:
                stat_values[name] = results[name]
        print(json.dumps(stat_values, indent=2))

    def save_results(self, results, out_dir, filename=None):
        """
        Save the results gathered from benchmarking and metadata about the commit
        to a JSON file named after the type of `self`.
        """
        json_name = "{}.json".format(self.name)
        if filename is None:
            output_filename = os.path.join(out_dir, json_name)
        else:
            output_filename = filename

        logging.info("Saving results for {name} to {filename}".format(
            name=self.name, filename=output_filename))

        data = []
        spot = 0
        make_new_entry = True
        if os.path.exists(output_filename):
            with open(output_filename, 'r') as in_file:
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
                print(self.commit)
                entry["commit"] = {
                    "pr": self.commit.pr,
                    "hash": self.commit.hash,
                    "time": self.commit.time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                }

            entry["runs"] = [results]
            data.insert(spot, entry)
        else:
            data[spot]["runs"].append(results)

        with open(output_filename, 'w') as out:
            json.dump(data, out, indent=2)
