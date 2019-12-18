# 1. Checkout Pytorch nightly
# 2. Run the benchmark scripts (each should output to its own file)
# 3. Push result files (all files ending in ".csv") to the site repo
import argparse
import os

from torchscript_benchmarks import run_shell_command

dir_path = os.path.dirname(os.path.realpath(__file__))


def local_file(*args):
    return os.path.join(dir_path, *args)


BUILDER_SCRIPT = local_file('builder.sh')
PIP = 'pip'
PYTHON = 'python'


class Commit(object):
    def __init__(self, time, pr, hash):
        self.time = time
        self.pr = pr
        self.hash = hash

    def __repr__(self):
        parts = [str((key, str(self.__dict__[key]))) for key in self.__dict__]
        return '({})'.format(", ".join(parts))

    @staticmethod
    def get_test():
        return Commit('2019-11-07T17:16:50-08:00', '12345',
                      '8f917abed18833ac00577844fe13375ac8fce168')


def clean_environment():
    """
    Uninstall torchvision and torch
    """
    YES = 'y\n' * 10
    YES = YES.encode('utf-8')

    # Cleanup environment
    run_shell_command([PIP, 'uninstall', 'torchvision'],
                      input=YES,
                      note='(use a clean environment for running tests)')
    run_shell_command([PIP, 'uninstall', 'torch'], input=YES)
    run_shell_command([PIP, 'uninstall', 'torch'], input=YES)

    try:
        run_shell_command([PYTHON, '-c', '"import torch"'],
                          note='(check that torch was uninstalled)')
        failed = False
    except RuntimeError as e:
        failed = True

    if not failed:
        raise RuntimeError("Cleanup went wrong, torch was not uninstalled")


def get_current_commit():
    """
    Query git for the hash from the current commit, grab the pull request number if possible
    """
    commit_info = run_shell_command(
        ['git', 'show', commit_hash, '--format="%aI%n%b"', '--no-patch'],
        silence_output=True,
        cwd='pytorch',
        note='(getting commit PR and timestamp)')
    commit_info = commit_info.split('\n')
    time = commit_info[0]
    pr = None
    for line in commit_info[1:]:
        if 'Pull Request resolved: ' in line:
            pr = line.split('/pull/')[1]
            break

    return Commit(time, pr, commit_hash)


def build_benchmark_command(benchmark_file, destination_dir, commit):
    """
    Create the shell command to run to execute a benchmark
    """

    command = [PYTHON, benchmark_file]
    if destination_dir is not None:
        command.extend(['--out', destination_dir])
    if commit is not None:
        command.extend(['--time', '"{}"'.format(commit.time)])
        command.extend(['--pr', '"{}"'.format(commit.pr)])
        command.extend(['--hash', '"{}"'.format(commit.hash)])

    return command


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run TorchScript benchmarks")
    parser.add_argument(
        "--benchmarks",
        help=  # noqa
        "Python file containing that will run the benchmark (can have multiple values)",
        required=True,
        nargs='+')
    parser.add_argument("--skip-checkout",
                        help="Don't remove existing PyTorch/Torchvision",
                        action='store_true',
                        required=False)
    parser.add_argument("--skip-conda-check",
                        help="Don't print the current conda environment",
                        action='store_true',
                        required=False)
    parser.add_argument("--out",
                        help="Destination git repo to write JSONs to",
                        required=False)
    parser.add_argument("--hash", help="PyTorch hash to use", required=False)

    args = parser.parse_args()

    # This is only set if a specific hash is provided and a PR can be found in the
    # commit message
    commit = None

    if not args.skip_conda_check:
        run_shell_command(['conda', 'info'],
                          note='(are you on the right conda environment?)')

    if not args.skip_checkout:
        # Remove any existing torch/torchvision installs
        clean_environment()

        # Build PyTorch from a specific hash (use master if one isn't provided)
        commit_hash = args.hash if args.hash else 'master'
        run_shell_command([BUILDER_SCRIPT, commit_hash],
                          note='(building pytorch)')

        # Get information about the currently checkout out commit
        commit = get_current_commit()
    else:
        assert args.hash is None, "Cannot --skip-checkout if a hash is set"

    for benchmark in args.benchmarks:
        run_shell_command(build_benchmark_command(benchmark, args.out, commit))
