from sys import argv

def opposite(d1, d2):
    diff1 = abs(d1[0] - d2[0])
    diff2 = abs(d1[1] - d2[1])
    if diff1 and diff1 == 2:
        return True
    elif diff2 and diff2 == 2:
        return True
    else:
        return False

def take_step(pipes, at, dirs, valids, lastdir):
    for d in dirs:
        # Keep it from going back and forth forever
        if opposite(dirs[d], lastdir): continue

        # Prevent moves that are invalid based on current position
        if pipes[at[0]][at[1]] not in valids[0][d]: continue

        step = [a + dr for a, dr in zip(at, dirs[d])]
        try:
            if pipes[step[0]][step[1]] in valids[1][d]:
                return step, dirs[d]
        except IndexError:
            continue

pipes = []
for li, line in enumerate(open(argv[1])):
    if 'S' in line:
        srow = li
        scol = line.find('S')
    pipes.append(line.replace('\n',''))

dirs = {'down': (1, 0), 'up': (-1, 0), 'left': (0, -1), 'right': (0, 1)}
valid_next = {'down': 'S|LJ', 'up': 'S|F7', 'left': 'S-FL', 'right': 'S-J7'}
valid_this = {'down': 'S|F7', 'up': 'S|LJ', 'left': 'S-J7', 'right': 'S-FL'}
valids = [valid_this, valid_next]
pos = [srow, scol]

# first step. does python have do while?
at, lastdir = take_step(pipes, pos, dirs, valids, (0, 0))
step = 1

while at != pos:
    at, lastdir= take_step(pipes, at, dirs, valids, lastdir)
    step += 1

p1max = int(step // 2)
print(f'Part 1: {p1max}')