from typing import Optional
import os
import sys
import subprocess
import shlex
import re

from .types import Command, Arg, OStream, EStream

__all__ = ["parse_input", "fprint", "locate_executable", "run_executable"]


def parse_input(
    user_input: list[str],
) -> Optional[tuple[Command, list[Arg], list[OStream], list[EStream]]]:
    command, *rest = shlex.split(user_input)

    args = []
    ostreams = []
    estreams = []

    i = 0
    while i < len(rest):
        if m := re.search(r"(\d)?>>?", rest[i]):
            if i + 1 >= len(rest):
                print("pysh: parse error near '\\n'")
                return None
            mode = "w" if len(re.findall(r">", rest[i])) == 1 else "a"
            if m.group(1) in {None, "1"}:
                ostreams.append((rest[i + 1], mode))
            elif m.group(1) == "2":
                estreams.append((rest[i + 1], mode))
            else:
                print(f"pysh: file descriptor {m.group(1)} not specified")
                return None
            i += 1
        # TODO: what about parse errors?
        else:
            args.append(rest[i])
        i += 1

    if len(ostreams) == 0:
        ostreams = [("<stdout>", "w")]
    if len(estreams) == 0:
        estreams = [("<stderr>", "w")]

    for stream, _ in ostreams + estreams:
        if stream in {"<stdout>", "<stderr>"}:
            continue
        if not os.path.exists(os.path.dirname(os.path.abspath(stream))):
            print(f"pysh: no such file or directory: {stream}")
            return None

    return command, args, ostreams, estreams


def fprint(
    content: str = "",
    ostreams: list[tuple[str, str]] = None,
    error: str = "",
    estreams: list[tuple[str, str]] = None,
    end: str | None = "\n",
) -> None:
    if ostreams is None:
        ostreams = [("<stdout>", "w")]
    if estreams is None:
        estreams = [("<stderr>", "w")]

    for estream, mode in estreams:
        try:
            ep = sys.stderr if estream == "<stderr>" else open(estream, mode)
        except Exception as e:
            print(f"pysh: no such file or directory: {estream}")
            return

        if error != "":
            print(error, file=ep)
        if estream != "<stderr>":
            ep.close()

    for ostream, mode in ostreams:
        try:
            op = sys.stdout if ostream == "<stdout>" else open(ostream, mode)
        except Exception as e:
            print(f"pysh: no such file or directory: {ostream}")
            return

        if content != "":
            print(content, file=op, end=end)
        if ostream != "<stdout>":
            op.close()


def locate_executable(command: str) -> Optional[str]:
    PATH = os.environ.get("PATH", "")

    for directory in PATH.split(":"):
        command_path = os.path.join(directory, command)
        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
            return command_path


def run_executable(
    command: Command, args: list[Arg], ostreams: list[OStream], estreams: list[EStream]
) -> None:
    for ostream, omode in ostreams:
        op = sys.stdout if ostream == "<stdout>" else open(ostream, mode=omode)
        for estream, emode in estreams:
            ep = sys.stderr if estream == "<stderr>" else open(estream, mode=emode)
            subprocess.run([command, *args], stdout=op, stderr=ep)
            if estream != "<stderr>":
                ep.close()
        if ostream != "<stdout>":
            op.close()
