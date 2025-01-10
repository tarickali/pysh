import os
from pathlib import Path

from .utils import locate_executable

__all__ = ["builtins"]


def handle_exit(args: list[str]) -> None:
    if len(args) > 1:
        print("exit: too many arguments")
        return

    if len(args) == 1 and not args[0].isnumeric():
        print("exit: invalid usage")
        return

    status = int(args[0]) if len(args) != 0 else 0
    exit(status)


def handle_echo(args: list[str]) -> None:
    print(" ".join(args))


def handle_type(args: list[str]) -> None:
    for command in args:
        if command in builtins:
            print(f"{command} is a shell builtin")
        elif executable := locate_executable(command):
            print(f"{command} is {executable}")
        else:
            print(f"{command}: not found")


def handle_pwd(args: list[str]) -> None:
    if len(args) != 0:
        print("pwd: too many arguments")
        return

    print(os.getcwd())


def handle_cd(args: list[str]) -> None:
    if len(args) == 0:
        return
    if len(args) > 1:
        print("cd: too many arguments")
        return

    path = args[0]  # assume absolute path
    if path[0] == "~":  # home directory
        HOME = os.environ.get("HOME", "/")
        path = HOME if len(path) == 1 else HOME + path[1:]
        path = os.path.abspath(path)
    elif not os.path.isabs(path):  # relative path
        path = os.path.abspath(path)

    if os.path.exists(path):
        os.chdir(path)
    else:
        print(f"cd: No such file or directory: {path}")


def handle_cat(args: list[str]) -> None:
    content = ""
    for arg in args:
        try:
            content += open(arg).read()
        except:
            content = f"cat: {arg}: No such file or directory\n"
    print(content, end="")


builtins = {
    "exit": handle_exit,
    "echo": handle_echo,
    "type": handle_type,
    "pwd": handle_pwd,
    "cd": handle_cd,
    "cat": handle_cat,
}
