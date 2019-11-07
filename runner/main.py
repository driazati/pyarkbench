# 1. Checkout Pytorch nightly
# 2. Run the benchmark scripts (each should output to its own file)
# 3. Push result files (all files ending in ".csv") to the site repo
import subprocess
from subprocess import PIPE
import textwrap
import argparse


from lib import run_shell_command, color, log


parser = argparse.ArgumentParser(description="Run TorchScript benchmarks")
parser.add_argument("--skip-checkout", help="Don't remove PyTorch/Torchvision", action='store_true', required=False)
parser.add_argument("--out", help="Destination to write CSVs to", required=True)
parser.add_argument("--hash", help="PyTorch hash to use", required=False)

args = parser.parse_args()


PIP = 'pip'
PYTHON = 'python'

run_shell_command(['conda', 'info'], note='(are you on the right conda environment?)')

def checkout_and_build_pytorch(hash):
    run_shell_command(['./builder.sh'])

# These are only set if a specific hash is provided and a PR can be found in the
# commit message
time = None
pr = None

if not args.skip_checkout:
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
        raise RuntimeError("Setup went wrong, torch was not uninstalled")

    # Build PyTorch
    commit_hash = args.hash if args.hash else 'master'
    run_shell_command(['./builder.sh', commit_hash], note='(building pytorch)')
    commit_info = run_shell_command(['git', 'show', commit_hash, '--format="%aI%n%b"', '--no-patch'], silence_output=True, cwd='pytorch', note='(getting commit PR and timestamp)')
    commit_info = commit_info.split('\n')
    time = commit_info[0]
    for line in commit_info[1:]:
        if 'Pull Request resolved: ' in line:
            pr = line.split('/pull/')[1]
            break

command = [PYTHON, 'test.py', '--out', args.out]
if args.hash:
    assert time is not None
    command.append('--time')
    command.append('"{}"'.format(time))
    if pr is not None:
        command.append('--pr')
        command.append(pr)
run_shell_command(command)


run_shell_command(['git', 'add', '*.csv'], cwd=args.out)
run_shell_command(['git', 'c', '-m"Update benchmarks"'], cwd=args.out)
run_shell_command(['git', 'push'], cwd=args.out)
