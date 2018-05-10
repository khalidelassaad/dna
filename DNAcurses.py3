from math import *
from time import sleep
from random import randint
import curses
WIDTH = 30 
#Width of the DNA. No larger than 80, 30 looks good 20

OFFSET = 1.7 
#Offset of two bands in radians (phase shift of two sines) 2.2

HEIGHT = 3.5
#Vertical stretch. Lower value makes it more compressed 3

PRINTDELAY = 0.07
#Delay in seconds between the printing of every line


L1 = ["A","T","G","C"]
L2 = ["T","A","C","G"]
def DNAstring(n):
    global WIDTH, HEIGHT, OFFSET, ATCOUNT, GCCOUNT
    C = int(WIDTH*(sin((n/HEIGHT)+OFFSET) + 1)/2)
    S = int(WIDTH*(sin(n/HEIGHT) + 1)/2)
    i_start = min(C, S)
    i_end = max(C, S)
    rs1 = []
    rs2 = []
    r = randint(0,3)
    for i in range(i_start+(40-WIDTH//2)):
        rs1.append(" ")
    rs1.append(L1[r])
    x = i_end-i_start-1
    y = x//2
    x = x-y
    for i in range(x):
        rs1.append("—")
    for i in range(y):
        rs2.append("—")
    rs2.append(L2[r])
    for i in range(WIDTH-i_end):
        rs2.append(" ")
    return([r, "".join(rs1), "".join(rs2)])

def main(stdscr):
    stdscr.clear()
    curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4,curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    C1 = [curses.color_pair(1),\
            curses.color_pair(2),\
            curses.color_pair(3),\
            curses.color_pair(4)]
    C2 = [curses.color_pair(2),\
            curses.color_pair(1),\
            curses.color_pair(4),\
            curses.color_pair(3)]
    curses.curs_set(False)
    x = 0
    dnadict = dict()
    for i in range(25):
        dnadict[i] = DNAstring(i)
    while True:
        try:
            for i in range(24):
                dna = dnadict[i]
                stdscr.addstr(i,0,dna[1],C1[dna[0]])
                stdscr.addstr(i,len(dna[1]),dna[2],C2[dna[0]])
                dnadict[i] = dnadict[i+1]
            x += 1
            dnadict[24] = DNAstring(i+x)
            stdscr.refresh()
            sleep(PRINTDELAY)
        except KeyboardInterrupt:
            break
curses.wrapper(main)

