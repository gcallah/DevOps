#!/bin/sh
#  This file should include all tests run on our web pages.

python3 $2/html_checker.py $1
python3 $2/url_checker.py $1 -u https://gcallah.github.io/DevOps/
# spell checker should be run here.
# python3 $2/html_spell.py $1 # main_dict custom_dict
