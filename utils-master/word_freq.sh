#!/bin/sh

cat $1 | tr -cs A-Za-z '\012' | tr A-Z a-z | sort | uniq -c | sort -r -n
