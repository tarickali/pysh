from .builtins import builtins
from .utils import parse_input, locate_executable, run_executable


def main():
    while True:
        parsed_input = parse_input(input("$ "))

        # Error parsing input, continue
        if parsed_input is None:
            continue

        command, args, ostreams, estreams = parsed_input

        if command in builtins:
            builtins[command](args, ostreams, estreams)
        elif locate_executable(command) is not None:
            run_executable(command, args, ostreams, estreams)
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
