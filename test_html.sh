#!/bin/sh
#  This file should include all tests run on our web pages.

# exit on any error with that error status:
set -e

python3 $2/html_checker.py $1
python3 $2/url_checker.py $1 https://gcallah.github.io/DevOps/

if [[ "$USER" == "pravarsingh" || "$USER" == "kdugar" ]]; then
	devops_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
	echo "Checking word spellings..."
	sh $devops_dir/spell_checker.sh $1 $2 $devops_dir
fi
