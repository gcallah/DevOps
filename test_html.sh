#!/bin/sh
#  This file should include all tests run on our web pages.

# exit on any error with that error status:
set -e

#In case someone does not set up submodule properly, we use try catch block to
#ensure submodule has been added properly.
{
    cd ../; git submodule add https://github.com/gcallah/utils.git; cd -
} || {}
cd $2; git pull; cd -
python3 $2/html_checker.py $1
python3 $2/url_checker.py $1 https://gcallah.github.io/DevOps/
#if python3 $2/html_spell.py $1 ../utils/English.txt ../utils/custom_dict.txt; 
#then
#    echo "Spell checker produced an error"
#    exit 0
#fi
