from math import *
from time import sleep
from random import randint
ac = "\033[91m"
tc = "\033[96m"
gc = "\033[92m"
cc = "\033[94m"
ec = "\033[0m"
WIDTH = 20 
#Width of the DNA. No larger than 80, 30 looks good 20

OFFSET = 2.2 
#Offset of two bands in radians (phase shift of two sines) 2.2

HEIGHT = 3
#Vertical stretch. Lower value makes it more compressed 3

PRINTDELAY = 0.05
#Delay in seconds between the printing of every line

ATCOUNT = 0
GCCOUNT = 0

L1 = ["A","T","G","C"]
L2 = ["T","A","C","G"]
C1 = [ac,tc,gc,cc]
C2 = [tc,ac,cc,gc]
def DNAstring(n):
    global WIDTH, HEIGHT, OFFSET, ATCOUNT, GCCOUNT
    C = int(WIDTH*(sin((n/HEIGHT)+OFFSET) + 1)/2)
    S = int(WIDTH*(sin(n/HEIGHT) + 1)/2)
    i_start = min(C, S)
    i_end = max(C, S)
    rs = []
    r = randint(0,3)
    if r < 2:
        ATCOUNT += 1
    else:
        GCCOUNT += 1
    for i in range(i_start):
        rs.append(" ")
    rs.append(C1[r])
    rs.append(L1[r])
    X = i_end - i_start - 1
    Y = X//2
    X = X - Y
    for i in range(X):
        rs.append("—")
    rs.append(C2[r])
    for i in range(Y):
        rs.append("—")
    rs.append(L2[r])
    rs.append(ec)
    return "".join(rs)

i = 0
while True:
    try:
        print(DNAstring(i))
        i += 1
        sleep(PRINTDELAY)
    except KeyboardInterrupt:
        print()
        print("Lines Printed: {}".format(i))
        print("A-T Pairs:     {}".format(ATCOUNT))
        print("G-C Pairs:     {}".format(GCCOUNT))
        break


