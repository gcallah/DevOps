#!/usr/bin/env python3 
# program to process SJC CVS file for faculty.

import csv

NAME = 0
CAMPUS = 1
DEPT = 2
RANK = 3
URL = 4

with open("/home/gcallah/utils/faculty.csv","r") as f_in:
    freader = csv.reader(f_in)
    with open("/home/gcallah/utils/out.csv","w") as f_out:
        for row in freader:
           # nms = "Judy A. Cardoza"
            nms = row[NAME].split()
            no_mi = [cln for cln in nms if "." not in cln]
            if len(no_mi) < 2:
                print(no_mi)
                continue
            # print("No mi:" + str(no_mi))
            no_titles = no_mi
            if len(no_mi) >= 2:
                no_titles = no_mi[0:2]
            # print("No titles:" + str(no_titles))
            fwriter = csv.writer(f_out)
            fwriter.writerow([no_titles[0], no_titles[1], row[CAMPUS],
                    row[DEPT], row[RANK], row[URL]])
    

