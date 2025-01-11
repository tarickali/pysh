from typing import Optional
import os
import sys

__all__ = ["locate_executable", "fprint"]


def locate_executable(command: str) -> Optional[str]:
    PATH = os.environ.get("PATH", "")

    for directory in PATH.split(":"):
        command_path = os.path.join(directory, command)
        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
            return command_path


def fprint(content: str, files: list[str], end: str | None = "\n") -> bool:
    for file in files:
        fp = sys.stdout if file == "<stdout>" else open(file, "w")
        print(content, file=fp, end=end)
        if file != "<stdout>":
            fp.close()
