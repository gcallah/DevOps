#!/usr/bin/env python3 
ints = []

n = 20

def init(n):
    for i in range(2, n + 1):
        ints.append(True)

def sieve(n):
    stop = n**(1/2)
    stop = int(stop)
    print("stop = " + str(stop))
    for i in range(2, stop + 1):
        print(i)
        if ints[i - 2] == True:
            j = (i * 2) - 2
            while j < len(ints):
                print("j = " + str(j))
                ints[j] = False
                j = j + i

init(n)
sieve(n)
print(ints)
