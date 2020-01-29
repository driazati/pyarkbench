import subprocess
from subprocess import PIPE
import textwrap
import os


class col:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


config = {'quiet': False}


def log(*args, **kwargs):
    if not config['quiet']:
        print(*args, **kwargs)


def color(color, text):
    return col.BOLD + color + str(text) + col.RESET


def run_shell_command(command,
                      cwd=None,
                      silence_output=False,
                      raise_on_fail=True,
                      input=None,
                      note=""):
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
