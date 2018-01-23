# import shutil
# shutil.copy2('C:/Users/VivekPC/Desktop/New folder/about.html', 'C:/Users/VivekPC/Desktop/about.html')
#
#

import sys

if len(sys.argv) < 2:
    print("Must supply a HTML file.")
    exit(1)

html_file = sys.argv[1]

# [Prof] - the file name has to come from command line
# f = open('C:/Users/VivekPC/Desktop/about.html',"r")
f = open(html_file, "r")
input = f.readlines()
f.close()

# Testing
print input
print '-'*60


# remove list items from <!DOCTYPE html> to next 22 lines (inclusive)
# [Prof] - we need to go until we start seeing text that wil appeR ON SCREEN
# [Prof] - These tags could include: <hn> - where n can be 1 - 5 or <p> or <figure> or <img>
pos1 = 0
for i in range(len(input)):
    if "<!DOCTYPE html>" in input[i]:
        pos1 = i

pos2 = 0
for i in range(len(input)):
    if "<h1>" in input[i] or "<p>" in input[i] or "<h2>" in input[i] \
        or "<h3>" in input[i] or "<h4>" in input[i] or "<h5>" in input[i]\
            or "<figure>" in input[i]:#or "<img" in input[i]:
        pos2 = i
        break

# del input[0:22+1]

del input[pos1:pos2]

# Removing tag </html>
# [Prof] - remove from </body> onwards
pos3 = 0
for line in range(len(input)):
  if  "</body>" in input[line]:
    pos3 = line

print pos3
del input[pos3:]


output = []
output.append("""{% extends "base.html" %}""""\n")
output.append("""{% block content %}""""\n")
output.append("""<div class="module">""""\n")
for i in range(len(input)):
    output.append(input[i])

output.append("""{% endblock content %}""")
print output

