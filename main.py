#!/usr/bin/python3
from string import Template
import sys
import os.path
from src.parser import parse_file

expansion = 1

if sys.stdin and sys.stdin.isatty():
    # check if ran from cli
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
    elif len(sys.argv) == 3:
        filepath = sys.argv[1]
        if sys.argv[2].isdecimal():
            expansion = int(sys.argv[2])
    elif len(sys.argv) == 1:
        print("Usage: ./main.py path_to_the_file")
        sys.exit(0)
    else:
        sys.exit(1)
else:
    filepath = "./exported.txt"


if os.path.isfile(filepath):
    with open(filepath) as file:
        parse_file(file.readlines(), expansion)
