from sys import argv
from functools import reduce
import re

dig_pattern = '\d+'
char_pattern = '[^\d\.\n]'

p1total = 0
prev_chars = []
prev_nums = []
gears = {}
for l, line in enumerate(open(argv[1])):
    # store tuples of numbers and their index spans
    nums = [(m[0], m.span()) for m in re.finditer(dig_pattern, line)]
    # store a list of the indices of characters
    chars = [m.start() for m in re.finditer(char_pattern, line)]
    # make a dictionary item for the index of any potential gears
    for m in re.finditer('\*', line):
        gears[f'{l} {m.start()}'] = []

    # Check previous line's nums against characters from this line
    for numstr, (i0, i1) in prev_nums:
        adj = [(c >= i0-1) and (c <= i1) for c in chars]
        if any(adj):
            p1total += int(numstr)
            # check if the match is with a *; if so, add it to the gear's nums
            for i, x in enumerate(adj):
                c = chars[i]
                if x:
                    try:
                        gears[f'{l} {c}'].append(int(numstr))
                    except: pass

    # reset prev numbers for next iteration
    prev_nums = []
    # Check this lines nums against this line's and last line's characters
    for numstr, (i0, i1) in nums:
        # adjacency to chars in previous line
        adj = [(pc >= i0-1) and (pc <= i1) for pc in prev_chars]

        if (i0 - 1) in chars or i1 in chars:
            # if it's adjacent, add to total
            p1total += int(numstr)
            # add it to a gear's nums if need be. if these indices aren't gears
            # then nothing will happen
            try:
                gears[f'{l} {i0 - 1}'].append(int(numstr))
            except: pass
            try:
                gears[f'{l} {i1}'].append(int(numstr))
            except: pass

        elif any(adj):
            # it's below or diagonal from prev line character, add to total
            p1total += int(numstr)
            # check if the match is with a *; if so, add it to the gear's nums
            for i, x in enumerate(adj):
                pc = prev_chars[i]
                if x:
                    try:
                        gears[f'{l-1} {pc}'].append(int(numstr))
                    except: pass

        else:
            # it's not a part # yet, store to check against next line's characters
            prev_nums.append((numstr, (i0, i1)))

    prev_chars = chars

p2total = sum([reduce(lambda x,y: x*y, g) for g in gears.values() if len(g) > 1])

print(f'Part 1: {p1total}')
print(f'Part 2: {p2total}')
