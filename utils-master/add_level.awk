#!/usr/bin/awk -f

/<a href/ { print "<" tag ">\n    " $0 }

/<\/a>/   { print "    " $0 "\n<\/" tag ">" }

!/</      { print "    " $0 }
