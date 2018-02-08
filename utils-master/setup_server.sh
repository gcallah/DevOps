#!/bin/sh

echo "Getting $1 code from GitHub."
git clone https://github.com/gcallah/$1.git
mv $1 mysite


echo "The following must be run interactively: once you run them, run mysite/db.sh."
echo "mkvirtualenv --python=/usr/bin/python3.5 django19"
echo "workon django19"
