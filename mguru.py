# -*- coding: utf-8 -*-
import Tkinter as tk
import time
import threading
import subprocess
import sys
from vowpalwabbit import pyvw

width = 1920
height = 1080
size = 30
w = width/size
n = int((width*height)/size**2)

vw = pyvw.vw(log_multi=n, power_t=1, learning_rate=0.7, nn=100, holdout_off=True)
root = tk.Tk()
p = 0
curr = None

examples = []

def example(v, s):
    return str(v)+" |pos x: "+str(1.0*s[0][0]/width)+ \
        " y: "+str(1.0*s[0][1]/height)+ \
        " |old x: "+str(1.0*s[1][0]/width)+ \
        " y: "+str(1.0*s[1][1]/width)


def value(c):
    return int(c[0]/size+c[1]/size*w)

def coord(v):
    x = v % w
    return (int(size*x), int(size*(v-x)/w))

def read_button():
    while True:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            sys.exit()
        if not line or line == "\n":
            sys.exit()
        if line == "1\n":
            for i in range(p, p+length):
                s = buffer[i % length]
                ex = example(value(curr)+1, s)
                print ex
                examples.append(ex)
                for j in range(0,25):
                    for e in examples:
                        vw.learn(e)

t = threading.Thread(target=read_button)
t.start()

prev = None
length = 1
buffer = length*[((0,0),(0,0))]
while True:
    time.sleep(0.2)
    new = root.winfo_pointerxy()
    if curr:
        prev = (curr[0], curr[1])
    curr = new
    if(prev and ((curr[0]-prev[0])**2 + (curr[1]-prev[1])**2) > 160):
        buffer[p] = (curr, prev)
        p = (p+1) % length
        ex = example(1, (curr, prev))
        pred = vw.predict(ex)
        c = coord(pred-1)
        if(pred>0):
            subprocess.Popen(u'echo "⬤" | osd_cat -c red  -O 1 -u black -d 1 -i '+str(c[0])+' -o '+str(c[1]), shell=True)
        print curr, value(curr), coord(value(curr)), pred-1, c
