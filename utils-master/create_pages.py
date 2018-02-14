#!/usr/bin/env python3 

import sys
import csv
from subprocess import call

HTML_PG = 0
TITLE = 1
PAGE_SCRIPT = "../utils/create_page.py"


if len(sys.argv) < 3:
    print("Must supply a file of pages to create and a page template.")
    exit(1)

page_templ = sys.argv[2]

with open(sys.argv[1], "r") as f_in:
    freader = csv.reader(f_in)
    for row in freader:
        print("<a href=\"" + row[HTML_PG] + "\">\n    "
              + row[TITLE] + "\n</a>\n")
        call(PAGE_SCRIPT + " \"" + row[TITLE] +
             "\" <" + page_templ +
             " >" + row[HTML_PG],
             shell=True)
