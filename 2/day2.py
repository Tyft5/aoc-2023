from sys import argv
from functools import reduce

cubes = {'red': 12, 'green': 13, 'blue': 14}

def get_cube_dicts(line: str):
    gdicts = []
    game, info = line.split(':')
    for draw in info.split(';'):
        d = {}
        for pull in draw.split(','):
            n, color = pull.split()
            d[color] = int(n)
        gdicts.append(d)
    
    return gdicts

def is_possible(line: str):
    for batch in get_cube_dicts(line):
        for color, n in batch.items():
            if n > cubes[color]:
                return False
    
    return True

def get_power(line: str):
    gdicts = get_cube_dicts(line)
    colormins = [max(filter(None, [batch.get(color) for batch in gdicts])) for color in cubes]
    
    return reduce(lambda x, y: x*y, colormins)

p1total, p2total = 0, 0
for line in open(argv[1]):
    if is_possible(line):
        p1total += int(line.split(':')[0].split()[-1])

    p2total += get_power(line)

print(f'Part 1: {p1total}')
print(f'Part 2: {p2total}')
