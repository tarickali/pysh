__all__ = ["builtins"]


def handle_exit(args: list[str]) -> None:
    if len(args) > 1:
        print(f"exit: too many arguments")
        return

    if len(args) == 1 and not args[0].isnumeric():
        print(f"exit: invalid usage")
        return

    status = int(args[0]) if len(args) != 0 else 0
    exit(status)


def handle_echo(args: list[str]) -> None:
    print(" ".join(args))


builtins = {
    "exit": handle_exit,
    "echo": handle_echo,
}
