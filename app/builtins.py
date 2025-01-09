import os

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


builtins = {
    "exit": handle_exit,
    "echo": handle_echo,
    "type": handle_type,
    "pwd": handle_pwd,
}
