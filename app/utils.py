from typing import Optional
import os

__all__ = ["locate_executable"]


def locate_executable(command: str) -> Optional[str]:
    PATH = os.environ.get("PATH", "")

    for directory in PATH.split(":"):
        command_path = os.path.join(directory, command)
        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
            return command_path
