#!/usr/bin/python

import sys
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import re
import numpy as np

COLORS = {
    'Y' : 'yellow',
    'P' : '#FF00FF',
    'B' : '#5050FF',
    'G' : 'green',
}

plt.figure(figsize=(10,15))

days = []
wallet = []
traffic = []
memb = []
macro = None
day = None

f = open('data.txt')
while True:
    line = f.readline()
    if not line:
        break
    match = re.match('^- day (\d+); Account: \$([^ ]+) .*traffic:([^)s]+)', line)
    if match:
        day = int(match.group(1))
        days.append(day)
        wallet.append(float(match.group(2)))
        traffic.append(int(match.group(3)) / 1000)
    match = re.match('buying a monthly membership', line)
    if match and day != None:
        memb.append(day)
    match = re.match('^Macro: (\d+ \d+ \d+ \d+ \d+ \d+)', line)
    if match:
        line = [float(m) for m in match.group(1).split()]
        if macro is None:
            macro = np.matrix(line)
        else:
            macro = np.vstack([macro, line])
f.close()


#plt.show()

#sys.exit(0)

weeks = range(0,day,28)

#sys.exit(0)

plt.subplot(411)

start = 325

plt.ylabel('wallet ($)')
plt.xlim(0,float(days[-1]))
plt.plot(days,wallet)
plt.plot([0],[start],'s', markersize=8)
plt.plot([0,float(days[-1])], [start,start], 'g')
plt.annotate('START', xy=(0, start), xytext=(10,start), horizontalalignment='left')
plt.plot(memb,[0] * len(memb), 'or', markersize=15)
plt.xlabel('time (days)')
plt.xticks(weeks)
plt.grid()

plt.subplot(412)
macro[:,0] /= 5000
macro[:,1] /= 15000
macro[:,2] /= 45000
macro[:,3] /= 135000
plt.plot(days, macro[:,0], COLORS['Y'], label='yellow', marker='o', linewidth=5, markevery=7)
plt.plot(days, macro[:,1], COLORS['P'], label='purple', marker='x', linewidth=3, markevery=7, markersize=7)
plt.plot(days, macro[:,2], COLORS['B'], label='blue', linewidth=3)
plt.plot(days, macro[:,3], COLORS['G'], label='green', linewidth=3)
plt.ylim(0, macro[:,:3].max() + 1)
plt.ylabel('macro (normalized)')
plt.xlim(0,float(days[-1]))
plt.xlabel('time (days)')
plt.xticks(weeks)
plt.legend()
plt.grid(True)

plt.subplot(413)
plt.ylabel('traffic (K)')
plt.xlim(0,float(days[-1]))
plt.plot(days,traffic)
plt.plot(memb,[0] * len(memb), 'or', markersize=15)
plt.xlabel('time (days)')
plt.xticks(weeks)
plt.grid()

plt.grid(True)

plt.subplot(414)
plt.ylabel('panels')



LENGTHS = {
    'Y' : 4,
    'P' : 6,
    'B' : 7,
    'G' : 8,
}

f = open('data.txt')
yaxis = 0
while True:
    line = f.readline()
    if not line:
        break
    match = re.match('^- day (\d+); Account: \$([^ ]+) .*traffic:([^)s]+)', line)
    if match:
        print line,
        day = int(match.group(1))
    match = re.match('^Qualifying the panel (.)\((.)', line)
    if match:
        print line,
        type = match.group(2)
        rect = Rectangle((day,yaxis), LENGTHS[match.group(1)]*7, 1, fc = COLORS[match.group(1)],
            alpha = (1,0.4)[type == 'C'])
        yaxis += 1
        plt.gca().add_patch(rect)
#        days.append(int(match.group(1)))
#        wallet.append(float(match.group(2)))
#        traffic.append(int(match.group(3)))
#        print match.group(3)
f.close()
# (days,yaxis), 4, 1

#rect = Rectangle((0,2), 4, 1, fc = 'yellow')
#plt.gca().add_patch(rect)
#rect = Rectangle((2,3), 4, 1, fc = 'yellow')
#plt.gca().add_patch(rect)


plt.xlim(0,day + 4)
plt.ylim(0,yaxis + 1)
plt.plot(memb,[0] * len(memb), 'or', markersize=15)
#plt.plot([1,2,3,4])

plt.xlabel('time (days)')
plt.xticks(weeks)
plt.yticks([])
plt.grid()

plt.savefig('/tmp/bb.pdf', bbox_inches = 'tight')
