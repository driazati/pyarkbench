# 1. Checkout Pytorch nightly
# 2. Run the benchmark scripts (each should output to its own file)
# 3. Push result files (all files ending in ".csv") to the site repo
import subprocess
import sys
import glob
import os
import textwrap

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


def run_command(command, cwd=".", silence_output=False, raise_on_fail=True, input=None, note="", **kwargs):
    note = "{}{}{}".format(col.BLUE, note, col.RESET)
    command_str = " ".join(command)
    log(color(col.YELLOW, command_str), note)

    encoding = None
    call_input = None
    if input is not None:
        encoding = 'utf-8'
        call_input = input.decode(encoding)

    if kwargs.get('shell', False):
        command = " ".join(command)
        kwargs['executable'] = '/bin/fish'

    if config['quiet']:
        ret = 0
        msg = ''
        try:
            subprocess.check_output(command, stderr=subprocess.PIPE, cwd=cwd, **kwargs)
        except subprocess.CalledProcessError as err:
            ret = err.returncode
            msg = err.stderr.decode(sys.getfilesystemencoding())
    else:
        result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=call_input, encoding=encoding, **kwargs)
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


YES = 'y\n' * 10
YES = YES.encode('utf-8')

# Use the "benchmark" conda environment
# run_command(['conda', 'activate', 'benchmark'], input=YES, shell=True)

# # Cleanup environment
# run_command(['pip', 'uninstall', 'torchvision'], input=YES, shell=True)
# run_command(['pip', 'uninstall', 'numpy'], input=YES, shell=True)
# run_command(['pip', 'uninstall', 'torch'], input=YES, shell=True)
# run_command(['pip', 'uninstall', 'torch'], input=YES, shell=True)

run_command(['python', 'test.py'])

files = glob.glob(os.getcwd() + '/*.csv')
out_dir = sys.argv[1]
print(out_dir)
print(files)

