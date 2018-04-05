#!/bin/sh
# This code is NOT getting us the container we need yet!
#  Still experimenting to get the right mix of utils.
if [ -z "$1" ]
  then
    echo "You must provide the location of your DevOps repo."
    exit 1
fi
docker pull python
docker run -it -p 8000:8000 -v $1:/home/DevOps --name alpine bash
