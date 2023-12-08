from sys import argv
from re import findall
from itertools import cycle

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
# nodes = starts.copy()
# cur_instr = [0 for _ in nodes]
# sni = 0
# n_instr = len(instr)

# idea: find period of each start
# next start reaches Z after x periods of prev
# find when next start reaches Z on a factor of the 
#   least common multiple of prev, cause they'll be Z
# eliminates redoing same cycles of prev ones
periods = [0 for _ in starts]

for sni, sn in enumerate(starts):
    nd = sn
    cnt = 0
    zcnt = False

    for dir in cycle(instr):
        nd = themap[nd][dir]
        cnt += 1

        if nd[-1] == 'Z':
            if not sni or cnt % periods[sni-1] == 0:
                if zcnt:
                    periods[sni] = cnt - pref
                    break
                else:
                    pref = cnt
                    zcnt = True
    print(periods)
p2steps = cnt            

# while sni < len(nodes):
#     nd = nodes[sni]

#     for dir in cycle(instr):
#         if sni:
#             if cur_instr[sni] < cur_instr[0]:
#                 nd = themap[nd][dir]
#                 cur_instr[sni] += 1
#             elif nd[-1] == 'Z':
#                 nodes[sni] = nd
#                 sni += 1
#                 print(nodes)
#                 print(cur_instr)
#                 break
#             else:
#                 nodes[sni] = nd
#                 sni = 0
#                 break
#         else:
#             nd = themap[nd][dir]
#             cur_instr[sni] += 1
#             if nd[-1] == 'Z':
#                 nodes[sni] = nd
#                 sni += 1
#                 break

print(f'Part 2: {p2steps}')