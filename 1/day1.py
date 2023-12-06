import re
from sys import argv

dwords = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', '1', '2', '3', '4', '5', '6', '7', '8', '9']

max_chars = max([len(w) for w in dwords])
p1total, p2total = 0, 0

for line in open(argv[1]):
    # shove the digits together
    digits = ''.join([c for c in line if c.isdigit()])
    # concat the first and last and add to the sum
    p1total += int(digits[0] + digits[-1])

    # get pairs of digits and the index where they start in the line
    # this will grab both words and numbers
    inds = [(mtch.start(), str((ind%9)+1)) for ind, word in enumerate(dwords) for mtch in re.finditer(word, line)]

    # sort by index in the line, then grab just the digits
    digits = [pair[1] for pair in sorted(inds, key=lambda p: p[0])]   
    p2total += int(digits[0] + digits[-1])


print(f'Part 1: {p1total}')
print(f'Part 2: {p2total}')

