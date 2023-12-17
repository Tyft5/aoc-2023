from sys import argv
import numpy as np

puzzle = []
for line in open(argv[1]):
    if line.strip():
        # Line is not blank, construct puzzle
        puzzle.append(line)
    else:
        # Line is blank, process puzzle and start the next one
        puzzle = np.array(puzzle)


        puzzle = []