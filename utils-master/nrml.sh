#!/bin/sh

sed 's/<p class="normal">\(.*\)/~<p>~\1/' | tr "~" "\n"
