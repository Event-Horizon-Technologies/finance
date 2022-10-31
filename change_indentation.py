#!/usr/bin/env python3

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
EXCLUDED_FOLDERS_LIST = ["venv"]
EXCLUDED_FOLDERS = set(ROOT.joinpath(folder) for folder in EXCLUDED_FOLDERS_LIST)
USAGE = (
    "Usage: change_indentation.py [OPTION]\n"
    "Change indentation for all python files in the project\n"
    "	-t		  Indent with tabs\n"
    "	-s <spaces> Indent with <spaces> number of spaces\n"
)

def get_new_indent(argv):
    if len(argv) < 1:
        exit(USAGE)
    if argv[0] == "-t":
        return "\t"
    if argv[0] == "-s":
        if len(argv) < 2:
            exit(USAGE)
        try:
            return int(argv[1]) * " "
        except ValueError:
            exit(USAGE)
    else:
        exit(USAGE)

def starts_code_block(line):
    return re.search(":\s*$", line)

def get_leading_space(line):
    if match := re.search("^(\s+)\S+", line):
        return match.group(1)
    return ""

def get_old_indent(file):
    last_line = ""
    with open(file, "r") as f:
        for line in f.readlines():
            if starts_code_block(last_line):
                return get_leading_space(line)
            last_line = line
    return ""

def is_long_indent(leading_space, last_leading_space, old_indent):
    return leading_space > last_leading_space + old_indent

def change_indentation(file, new_indent):
    old_indent = get_old_indent(file)
    last_leading_space = ""

    if old_indent == "": return

    with open(file, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            leading_space = get_leading_space(line)
            indents = leading_space.count(old_indent)
            if indents:
                if not is_long_indent(leading_space, last_leading_space, old_indent):
                    lines[i] = line.replace(leading_space, indents * new_indent, 1)
                last_leading_space = leading_space

    if lines:
        with open(file, "w") as f:
            f.write(''.join(lines))

def is_included(file):
    return EXCLUDED_FOLDERS.isdisjoint(file.parents)

def main(argv):
    new_indent = get_new_indent(argv)
    for file in filter(is_included, ROOT.rglob("*.py")):
        change_indentation(file, new_indent)


if __name__ == "__main__":
    main(sys.argv[1:])
