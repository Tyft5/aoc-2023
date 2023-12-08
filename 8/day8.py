from sys import argv
from re import findall
from itertools import cycle
from math import lcm

themap = {}
with open(argv[1]) as f:
    instr = [int(c == 'R') for c in f.readline().strip('\n')]
    f.readline() # blank
    
    for line in f:
        at, cnct = line.split('=')
        themap[at.strip()] = findall('[A-Z0-9]+', cnct)

# Part 1
node = 'AAA'; p1steps = 0
for dir in cycle(instr):
    node = themap[node][dir]
    p1steps += 1
    if node == 'ZZZ': break

print(f'Part 1: {p1steps}')

# Part 2
starts = [k for k in themap if k[-1] == 'A']
periods = [0 for _ in starts]

for sni, sn in enumerate(starts):
    nd = sn
    cnt = 0
    zcnt = False

    for dir in cycle(instr):
        nd = themap[nd][dir]
        cnt += 1

        if nd[-1] == 'Z':
            if zcnt:
                periods[sni] = cnt - pref
                break
            else:
                pref = cnt
                zcnt = True

p2steps = lcm(*periods)

print(f'Part 2: {p2steps}')