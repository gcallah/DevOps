#!/bin/sh
#This script should be called from test_html.sh with both arguments supplied
#Runs spell checker ,commits the custom dictionary and returns
#the exit code

python3 $2/html_spell.py $1 ../utils/data/English.txt data/custom_dict.txt -e
echo $?
git add data/custom_dict.txt
git commit -m "Updated Custom dictionary"