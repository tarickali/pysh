import os

from .utils import locate_executable, fprint

__all__ = ["builtins"]


def handle_exit(args: list[str], ostreams: list[str], estreams: list[str]) -> None:
    if len(args) > 1:
        fprint(error="exit: too many arguments", estreams=estreams)
        return

    if len(args) == 1 and not args[0].isnumeric():
        fprint(error="exit: invalid usage", estreams=estreams)
        return

    status = int(args[0]) if len(args) != 0 else 0
    exit(status)


def handle_echo(args: list[str], ostreams: list[str], estreams: list[str]) -> None:
    content = " ".join(args)
    fprint(content=content, ostreams=ostreams, estreams=estreams)


def handle_type(args: list[str], ostreams: list[str], estreams: list[str]) -> None:
    content = ""
    for command in args:
        if command in builtins:
            content += f"{command} is a shell builtin"
        elif executable := locate_executable(command):
            content += f"{command} is {executable}"
        else:
            content += f"{command}: not found"

    fprint(content=content, ostreams=ostreams)


def handle_pwd(args: list[str], ostreams: list[str], estreams: list[str]) -> None:
    errors = ""
    if len(args) != 0:
        errors += "pwd: too many arguments"

    fprint(content=os.getcwd(), ostreams=ostreams, error=errors, estreams=estreams)


def handle_cd(args: list[str], ostreams: list[str], estreams: list[str]) -> None:
    if len(args) > 1:
        fprint(error="cd: too many arguments", estreams=estreams)
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
        fprint(error=f"cd: {path}: No such file or directory", estreams=estreams)


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
    # "cat": handle_cat,
}
