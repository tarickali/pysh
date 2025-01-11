from typing import Optional
import sys
import subprocess
import shlex
import re

from .builtins import builtins
from .utils import locate_executable


def parse_args(args: list[str]) -> Optional[tuple[list[str], list[str]]]:
    value_args = []
    file_args = []

    i = 0
    while i < len(args):
        if m := re.search(r"(\d)?>", args[i]):
            n = 1 if m.group(1) is None else int(m.group(1))
            if i + 1 >= len(args):
                print("pysh: parse error near '\\n'")
                return None
            file_args.append(args[i + 1])
            i += 1
        else:
            value_args.append(args[i])
        i += 1

    return value_args, file_args


def main():
    while True:
        command, *raw_args = shlex.split(input("$ "))
        parsed_args = parse_args(raw_args)

        # Error parsing args, continue
        if parsed_args is None:
            continue

        args, files = parsed_args
        if len(files) == 0:
            files = ["<stdout>"]

        if command in builtins:
            builtins[command](args, files)
        elif locate_executable(command) is not None:
            for file in files:
                fp = sys.stdout if file == "<stdout>" else open(file, "w")
                subprocess.run([command, *args], stdout=fp)
                if file != "<stdout>":
                    fp.close()
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
