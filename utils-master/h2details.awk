#!/usr/bin/awk -f
# this file processes HTML files to change hX tags (<h1> etc.
# to the <details> <summary> style we now use.

BEGIN {
    INDENT1 = "    "
    INDENT2 = INDENT1 INDENT1
    INDENT3 = INDENT2 INDENT1
    INDENT4 = INDENT2 INDENT2
    INDENT5 = INDENT4 INDENT1
}

/ *<h2>/ {
   print INDENT2 "<details>"
   print INDENT3 "<summary class=\"sum1\">"
   next
}

/ *<\/h2>/ {
   print INDENT3 "</summary>"
   # this next tag will need to be moved by hand to the proper place
   # but at least we can output it at the correct indent level and
   # indicate its necessity
   print INDENT2 "</details>"
   next
}

/ *<h3>/ {
   print INDENT3 "<details>"
   print INDENT4 "<summary class=\"sum2\">"
   next
}

/ *<\/h3>/ {
   print INDENT4 "</summary>"
   # this next tag will need to be moved by hand to the proper place
   # but at least we can output it at the correct indent level and
   # indicate its necessity
   print INDENT3 "</details>"
   next
}

/ *<h4>/ {
   print INDENT4 "<details>"
   print INDENT5 "<summary class=\"sum3\">"
   next
}

/ *<\/h4>/ {
   print INDENT5 "</summary>"
   # this next tag will need to be moved by hand to the proper place
   # but at least we can output it at the correct indent level and
   # indicate its necessity
   print INDENT4 "</details>"
   next
}

{ print }
