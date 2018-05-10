#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3 -u
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

PRINTDELAY = 0.09 #0.09
#Delay in seconds between the printing of every line


L1 = ["A","C","G","T"]
L2 = ["T","G","C","A"]
def randTable(n):
    l = []
    for i in range(n):
        l.append(randint(0,3))
    return l
 
def DNAstring(n,line, dna):
    global WIDTH, HEIGHT, OFFSET, ATCOUNT, GCCOUNT, L1, L2
    C = int(WIDTH*(sin((n/HEIGHT)+OFFSET) + 1)/2)
    S = int(WIDTH*(sin(n/HEIGHT) + 1)/2)
    i_start = min(C, S)
    i_end = max(C, S)
    rs1 = []
    rs2 = []
    lx = []
    colorcode = 0
    if C < S:
        lx = [L1, L2]
        colorcode = dna[line] 
    else:
        lx = [L2, L1]
        colorcode = 3 - dna[line] 
    for i in range(i_start+(40-WIDTH//2)):
        rs1.append(" ")
    rs1.append(lx[0][dna[line]])
    x = i_end-i_start-1
    y = x//2
    x = x-y
    for i in range(x):
        rs1.append("—")
    for i in range(y):
        rs2.append("—")
    rs2.append(lx[1][dna[line]])
    for i in range(WIDTH-i_end):
        rs2.append(" ")
    return([colorcode, "".join(rs1), "".join(rs2),C<S])

def tickinit(tick,dnatable):
    dnalist = []
    for i in range(24):
        dnalist.append(DNAstring(i+tick,i,dnatable))
    return dnalist

class Person:
    def __init__(self,sex,age,height,eyecolor,haircolor,condition):
        self.sex = sex
        self.age = age
        self.height = height
        self.eyecolor = eyecolor
        self.haircolor = haircolor
        self.condition = condition

def main(stdscr):
    global PEOPLE
    stdscr.clear()
    curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4,curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    C1 = [curses.color_pair(1),\
            curses.color_pair(4),\
            curses.color_pair(3),\
            curses.color_pair(2)]
    C2 = [curses.color_pair(2),\
            curses.color_pair(3),\
            curses.color_pair(4),\
            curses.color_pair(1)]
    curses.curs_set(False)
    tick = 0
    dnatable = randTable(24)
    dnalist = []
    loadinglines = ["INITIALIZING DNA SEQUENCER","-- Loading sample",\
            "-- Calculating resistivity quotient", "-- Running variable voltage array",\
            "-- Resistance mapping nucleotides","","SAMPLE SUCCESSFULLY LOADED!"]
    loadinglines2 = ["GENOME SUCCESSFULLY SEQUENCED","-- Locating dominant alleles",\
            "-- Reading genetic traits","-- Formatting output","",\
            "PRESS ANY KEY TO VIEW RESULTS"]
    stage = 1
    while True:
        stdscr.clear()
        try:
            if stage == 0:
                for i in range((tick//10)+1):
                    if i == len(loadinglines):
                        stage = 1
                        break
                    s = loadinglines[i]
                    stdscr.addstr(i+1,10,s,curses.A_BOLD)
            elif stage == 1:
                dnalist = tickinit(tick,dnatable)
                stage = 2
                temptick = tick
            elif stage == 2:
                for i in range(24):
                    if i > 1 and i < 22:
                        dna = dnalist[i]
                        model = curses.A_BOLD
                        mod = []
                        if dna[3]:
                            mod = [0,model]
                        else:
                            mod = [model,0]
                        stdscr.addstr(i,0,dna[1],C1[dna[0]]+mod[0])
                        stdscr.addstr(i,len(dna[1]),dna[2],C2[dna[0]]+mod[1])
                        dnalist[i] = DNAstring(i+tick,i,dnatable)
                    elif i > 0 and i < 23:
                        stdscr.addstr(i,40-WIDTH//2,"="*WIDTH,curses.A_BOLD)
                    else:
                        s = " Reading DNA " + ". " * ((tick//4)%4)
                        if len(s) % 2:
                            s = s + " "
                        w = (WIDTH - len(s))//2
                        ws = "=" * w
                        stdscr.addstr(i,40-WIDTH//2,ws+s+ws,curses.A_BOLD)
            tick += 1
            stdscr.refresh()
            sleep(PRINTDELAY)
        except KeyboardInterrupt:
            break
curses.wrapper(main)

