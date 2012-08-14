#!/usr/bin/python

import sys
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import re

plt.figure(figsize=(10,15))

days = []
wallet = []
traffic = []
memb = []
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
#        print match.group(3)
f.close()

weeks = range(0,day,28)

#sys.exit(0)

plt.subplot(311)
plt.ylabel('wallet ($)')
plt.xlim(0,float(days[-1]))
plt.plot(days,wallet)
plt.plot([0],[225],'s', markersize=8)
plt.plot([0,float(days[-1])], [225,225], 'g')
plt.annotate('START', xy=(0, 225), xytext=(10,225), horizontalalignment='left')
plt.plot(memb,[0] * len(memb), 'or', markersize=15)
plt.xlabel('time (days)')
plt.xticks(weeks)
plt.grid()

plt.grid(True)

plt.subplot(312)
plt.ylabel('traffic (K)')
plt.xlim(0,float(days[-1]))
plt.plot(days,traffic)
plt.plot(memb,[0] * len(memb), 'or', markersize=15)
plt.xlabel('time (days)')
plt.xticks(weeks)
plt.grid()

plt.grid(True)

plt.subplot(313)
plt.ylabel('panels')


COLORS = {
    'Y' : 'yellow',
    'P' : '#FF00FF',
    'B' : '#5050FF'
}
LENGTHS = {
    'Y' : 4,
    'P' : 6,
    'B' : 7,
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