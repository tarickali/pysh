import os

from .utils import locate_executable, fprint

__all__ = ["builtins"]


def handle_exit(args: list[str], files: list[str]) -> None:
    if len(args) > 1 or len(files) != 1:
        print("exit: too many arguments")
        return

    if len(args) == 1 and not args[0].isnumeric():
        print("exit: invalid usage")
        return

    status = int(args[0]) if len(args) != 0 else 0
    exit(status)


def handle_echo(args: list[str], files: list[str]) -> None:
    content = " ".join(args)
    fprint(content, files)


def handle_type(args: list[str], files: list[str]) -> None:
    content = ""
    for command in args:
        if command in builtins:
            content += f"{command} is a shell builtin"
        elif executable := locate_executable(command):
            content += f"{command} is {executable}"
        else:
            content += f"{command}: not found"

    fprint(content, files)


def handle_pwd(args: list[str], files: list[str]) -> None:
    content = ""
    if len(args) != 0:
        content += "pwd: too many arguments"

    fprint(os.getcwd(), files)


def handle_cd(args: list[str], files: list[str]) -> None:
    if len(args) > 1:
        print("cd: too many arguments")
        return

    if len(args) == 0:
        args = ["~"]

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


def handle_cat(args: list[str], files: list[str]) -> None:
    content = ""
    for arg in args:
        try:
            content += open(arg).read()
        except:
            print(f"cat: {arg}: No such file or directory")

    fprint(content, files, end="")


def handle_ls(args: list[str], files: list[str]) -> None:
    pass


builtins = {
    "exit": handle_exit,
    "echo": handle_echo,
    "type": handle_type,
    "pwd": handle_pwd,
    "cd": handle_cd,
    "cat": handle_cat,
}
