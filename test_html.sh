#!/bin/sh
#  This file should include all tests run on our web pages.

# exit on any error with that error status:
set -e

python3 $2/html_checker.py $1
python3 $2/url_checker.py $1 -u https://gcallah.github.io/DevOps/
# spell checker should be run here.
python3 $2/html_spell.py $1 ../utils/English.txt ../utils/custom_dict.txt
