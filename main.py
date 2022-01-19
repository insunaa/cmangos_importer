#!/usr/bin/python3
from string import Template
import sys
import os.path
from src.parser import parse_file


if len(sys.argv) == 2:
    filepath = sys.argv[1]
elif len(sys.argv) == 1:
    print("Usage: ./main.py path_to_the_file")
    sys.exit(0)
else:
    sys.exit(1)

if os.path.isfile(filepath):
    with open(filepath) as file:
        parse_file(file.readlines())
