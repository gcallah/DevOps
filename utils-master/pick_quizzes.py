#!/usr/bin/env python3 

"""
    File to select "quiz of the day" (or minute, or year, depending on how
    often we run this!) for include in course web pages.
"""

import os
import random
import re

for file in os.listdir('.'):
    if re.match(r'^quiz[0-9]+.[0-9]+.txt$', file):
        print(file)
