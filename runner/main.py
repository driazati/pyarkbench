# 1. Checkout Pytorch nightly
# 2. Run the benchmark scripts (each should output to its own file)
# 3. Push result files (all files ending in ".csv") to the site repo
import subprocess
from subprocess import PIPE
import textwrap
import argparse


from lib import run_shell_command, color, log

BUILDER_SCRIPT = './builder.sh'
BENCHMARK_TEST = './benchmarks/test.py'
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



def clean_environment():
    YES = 'y\n' * 10
    YES = YES.encode('utf-8')

    # Cleanup environment
    run_shell_command([PIP, 'uninstall', 'torchvision'], input=YES, note='(use a clean environment for running tests)')
    run_shell_command([PIP, 'uninstall', 'torch'], input=YES)
    run_shell_command([PIP, 'uninstall', 'torch'], input=YES)

    try:
        run_shell_command([PYTHON, '-c', '"import torch"'], note='(check that torch was uninstalled)')
        failed = False
    except RuntimeError as e:
        failed = True

    if not failed:
        raise RuntimeError("Cleanup went wrong, torch was not uninstalled")


def get_current_commit():
    commit_info = run_shell_command(['git', 'show', commit_hash, '--format="%aI%n%b"', '--no-patch'], silence_output=True, cwd='pytorch', note='(getting commit PR and timestamp)')
    commit_info = commit_info.split('\n')
    time = commit_info[0]
    pr = None
    for line in commit_info[1:]:
        if 'Pull Request resolved: ' in line:
            pr = line.split('/pull/')[1]
            break

    return Commit(time, pr, hash)


def build_test_command(commit):
    command = [PYTHON, BENCHMARK_TEST, '--out', args.out]
    if commit is not None:
        command.extend(['--time', '"{}"'.format(commit.time)])
        command.extend(['--pr', '"{}"'.format(commit.pr)])
        command.extend(['--hash', '"{}"'.format(commit.hash)])

    return command


parser = argparse.ArgumentParser(description="Run TorchScript benchmarks")
parser.add_argument("--skip-checkout", help="Don't remove existing PyTorch/Torchvision", action='store_true', required=False)
parser.add_argument("--skip-conda-check", help="Don't print the current conda environment", action='store_true', required=False)
parser.add_argument("--out", help="Destination git repo to write JSONs to", required=True)
parser.add_argument("--hash", help="PyTorch hash to use", required=False)

args = parser.parse_args()


# These are only set if a specific hash is provided and a PR can be found in the
# commit message
commit = None


if not args.skip_conda_check:
    run_shell_command(['conda', 'info'], note='(are you on the right conda environment?)')

if not args.skip_checkout:
    # Remove any existing torch/torchvision installs
    clean_environment()

    # Build PyTorch
    commit_hash = args.hash if args.hash else 'master'
    run_shell_command([BUILDER_SCRIPT, commit_hash], note='(building pytorch)')

    # Get information about the currently checkout out commit
    time, pr = get_current_commit()

# Testing only
commit = Commit('2019-11-07T17:16:50-08:00', '12345', '8f917abed18833ac00577844fe13375ac8fce168')


run_shell_command(build_test_command(commit))


# Move results to the out directory and update it
# run_shell_command(['git', 'add', '*.json'], cwd=args.out)
# run_shell_command(['git', 'c', '-m"Update benchmarks"'], cwd=args.out)
# run_shell_command(['git', 'push'], cwd=args.out)
