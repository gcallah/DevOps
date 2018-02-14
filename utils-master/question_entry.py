"""
A little script to get and properly format questions for quizzes, homework,
etc.
"""

import sys
import random

DELIM = '#'
CORR_MARK = '^'


def ask(msg):
    print(msg, end='')
    ans = input()
    return ans.strip()

def ask_int(msg):
    ans = "NAN"
    while not ans.isdigit():
        ans = ask(msg)
    return ans

def add_item(item):
    return item + DELIM

if len(sys.argv) < 2:
    print("Must enter a directory for quizzes.")
    exit(1)

quiz_dir = sys.argv[1]

chap = ask_int("Enter chapter # for question: ")
section = ask_int("Enter section # for question: ")
file_nm = quiz_dir + "/quiz" + chap + "." + section + ".txt"
f = open(file_nm, "a")

while True:
    answers = []

    question = ask("Enter question (blank to stop entering): ")
    if len(question) < 1:
        break

    correct = ask("Enter correct answer (we will randomize for you!): ")
    correct = CORR_MARK + correct
    answers.append(correct)
    
    new_bad = ""
    while True:
        new_bad = ask("Enter a wrong answer (blank to stop entering): ")
        if len(new_bad) < 1:
            break
        else:
            answers.append(new_bad)
    
    s = ""
    s += add_item(question)
    random.shuffle(answers)
    for answer in answers:
        s += add_item(answer)

    s = s[0:-1]
    f.write(s + "\n")

