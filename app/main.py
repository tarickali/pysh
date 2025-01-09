import subprocess

from .builtins import builtins
from .utils import locate_executable


def main():
    while True:
        command, *args = input("$ ").split(" ")
        if command in builtins:
            builtins[command](args)
        elif locate_executable(command) is not None:
            subprocess.run([command, *args])
        else:
            print(f"{command}: command not found.")


if __name__ == "__main__":
    main()
