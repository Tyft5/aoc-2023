from sys import argv
import numpy as np

# expansion factor
factor = 10**6

def dist(d1, d2, cols, expanded, fac):
    # number of rows traversed + col difference
    d1row = d1 // cols; d1col = d1 % cols
    d2row = d2 // cols; d2col = d2 % cols

    # add $factor steps for each expansion between the rows and cols
    expand = 0
    for rtoexp in expanded[0]:
        if (d1row > rtoexp > d2row):
            expand += fac
    for ctoexp in expanded[1]:
        if (d1col > ctoexp > d2col) or (d2col > ctoexp > d1col):
            expand += fac

    return abs((d2row - d1row)) + abs(d2col - d1col) + expand

im = []
for line in open(argv[1]):
    im.append([c == '#' for c in line.strip('\n')])
im = np.array(im, dtype=bool)
cols = im.shape[1]

# Find rows and columns that have no galaxies
exp_cols = ~np.any(im, axis=0)
exp_rows = ~np.any(im, axis=1)
exp = (np.where(exp_rows)[0], np.where(exp_cols)[0])

# Flatten and find indices of galaxies
galax = np.where(im.ravel())[0]

# Find distances between pairs
p1total = 0; p2total = 0
for gi in range(len(galax)-1, 0, -1):
    for gj in range(gi):
        # Find dist between each galaxy and the ones before it
        # Sum up dists from each pair
        p1total += dist(galax[gi], galax[gj], cols, exp, 1)
        p2total += dist(galax[gi], galax[gj], cols, exp, factor-1)

print(f'Part 1: {p1total}')
print(f'Part 2: {p2total}')

