#!/bin/sh

cp cloud/*.html $1
git add $1/*.html
git commit $1/*.html -m "Initial commit."
git push origin master
