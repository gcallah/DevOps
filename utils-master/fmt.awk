#!/usr/bin/awk -f

# fmt.awk: format into 60 character lines.
# From Kernighan and Pike.

/./  {
        for (i = 1; i <= NF; i++) addword($i) 
        print  # preserve existing lines!
}

/^$/ { printline(); print "" }
END  { printline() }

function addword(w)
{
    if (length(line) + 1 + length(w) > 60)
        printline()
    if (length(line) == 0)
        line = w
    else
        line = line " " w
}

function printline()
{
    if (length(line) > 0)
    {
        print line
        line = ""
    }
}
