# -*- coding: utf-8 -*-
import Tkinter as tk
import time
import threading
import subprocess
import sys
from vowpalwabbit import pyvw
vw = pyvw.vw(quiet=True)
root = tk.Tk()
p = 0
curr = None

def example(v, s):
    return str(v)+" |pos x: "+str(s[0][0])+ \
        " y: "+str(s[0][1])+ \
        " |dv dx: "+str(s[1][0])+ \
        " dy: "+str(s[1][1])

width = 1920
coeff = 1000000.0

def value(c):
    return (c[0]+c[1]*width)/coeff

def coord(v):
    n = v*coeff
    x = n % width
    return (int(x), int((n-x)/width))

def read_button():
    while True:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            sys.exit()
        if not line or line == "\n":
            sys.exit()
        if line == "1\n":
            for i in range(p, p+size):
                s = buffer[i % size]
                ex = example(value(curr), s)
                print ex
                for j in range(0,25):
                    vw.example(ex).learn()

t = threading.Thread(target=read_button)
t.start()

dv = None
size = 5
buffer = size*[((0,0),(0,0))]
while True:
    time.sleep(0.1)
    new = root.winfo_pointerxy()
    if curr:
        dv = (new[0]-curr[0], new[1]-curr[1])
    curr = new
    if(dv and (dv[0]**2 + dv[1]**2) > 160):
        buffer[p] = (curr, dv)
        p = (p+1) % size
        ex = example(0, (curr, dv))
        pred = vw.predict(ex)
        c = coord(pred)
        subprocess.Popen(u'echo "⬤" | osd_cat -c red  -O 1 -u black -d 2 -i '+str(c[0]-width)+' -o '+str(c[1]), shell=True)
        print coord(value(curr)), c
