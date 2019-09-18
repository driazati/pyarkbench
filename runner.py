# 1. Checkout Pytorch nightly
# 2. Run the benchmark scripts (each should output to its own file)
# 3. Push result files (all files ending in ".csv") to the site repo
import subprocess
from subprocess import PIPE
import sys
import glob
import os
import textwrap
import argparse
import pty


class col:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


config = {
    'quiet': False
}

def log(*args, **kwargs):
    if not config['quiet']:
        print(*args, **kwargs)


def color(color, text):
    return col.BOLD + color + str(text) + col.RESET


def run_shell_command(command, cwd=None, silence_output=False, raise_on_fail=True, input=None, note=""):
    note = "{}{}{}".format(col.BLUE, note, col.RESET)
    command_str = " ".join(command)
    log(color(col.YELLOW, command_str), note)

    encoding = None
    call_input = None
    if input is not None:
        encoding = 'utf-8'
        call_input = input.decode(encoding)

    command = " ".join(command) + "\n"

    kwargs = {
        "stdout": PIPE,
        "stderr": PIPE,
        # "encoding": encoding,
        "shell": True
    }

    if input is not None:
        kwargs['input'] = input
    if cwd is not None:
        kwargs['cwd'] = cwd

    result = subprocess.run(command, **kwargs)
    msg = "(process returned {})".format(result.returncode)

    def get_output(stream):
        if isinstance(stream, str):
            return stream.strip()
        return stream.decode('utf-8').strip()

    if not silence_output:
        out = get_output(result.stdout)
        if out != '':
            log(color(col.RED, "stdout"))
            log(textwrap.indent(out, '    '))
        out = get_output(result.stderr)
        if out != '':
            log(color(col.RED, "stderr"))
            log(textwrap.indent(out, '    '))

    if result.returncode != 0:
        if raise_on_fail:
            raise RuntimeError(msg)
        else:
            log(msg)
    return get_output(result.stdout)


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

if not args.skip_checkout:
    YES = 'y\n' * 10
    YES = YES.encode('utf-8')

    # Cleanup environment
    run_shell_command([PIP, 'uninstall', 'torchvision'], input=YES, note='(use a clean environment for running tests)')
    run_shell_command([PIP, 'uninstall', 'numpy'], input=YES)
    run_shell_command([PIP, 'uninstall', 'torch'], input=YES)
    run_shell_command([PIP, 'uninstall', 'torch'], input=YES)

    try:
        run_shell_command([PYTHON, '-c', '"import torch"'], note='(check that torch was uninstalled)')
        # print("ran")
        failed = False
    except RuntimeError as e:
        failed = True

    if not failed:
        raise RuntimeError("Setup went wrong, torch was not uninstalled")


    # Build PyTorch
    # TODO: checkout, build
    if args.hash:
        # Build pytorch
        run_shell_command(['./builder.sh', args.hash], note='(building pytorch)')
    else:
        # Using nightly build
        install = [PIP, 'install', '--pre', 'torch', 'torchvision', '-f', 'https://download.pytorch.org/whl/nightly/cu92/torch_nightly.html']
        run_shell_command(install, note='(no hash provided, using nightly build)')

run_shell_command([PYTHON, 'test.py', args.out])


run_shell_command(['git', 'add', '*.csv'], cwd=args.out)
run_shell_command(['git', 'c', '-m"Update benchmarks"'], cwd=args.out)
run_shell_command(['git', 'push'], cwd=args.out)


