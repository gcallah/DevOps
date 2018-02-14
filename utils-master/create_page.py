#!/usr/bin/env python3 

import sys

indent = "            "

if len(sys.argv) < 2:
    print("Must supply a page name.")
    exit(1)

page_nm = sys.argv[1]
for line in sys.stdin:
    sys.stdout.write(line)
    if "<title>" in line:
        sys.stdout.write(indent + page_nm + "\n")
    if "<h1>" in line:
        sys.stdout.write(indent + page_nm + "\n")

