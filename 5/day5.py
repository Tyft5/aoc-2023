from sys import argv
import re

def dest_from_src(mapping, the_id):
    for (dest, src, span) in mapping:  # for each line/range
        if src <= the_id < (src + span):
            # the id is in range, get the dest id
            return dest + (the_id - src)

    # id wasn't in any ranges, so it's 1 to 1
    return the_id


def get_location(maps, the_id):
    for m in maps:  # for each mapping
        the_id = dest_from_src(m, the_id)
    return the_id

data = []
with open(argv[1]) as f:
    # grab seeds from first line
    seeds = [int(s) for s in f.readline().split(':')[1].split()]

    for line in f:
        # skip empty lines
        if not line.strip(): continue

        # build data structure:
        # [ #map [ #range ( destination, source, span ), ... ], ... ]
        
        mappings = re.findall('\d+', line)
        if mappings:  # line has numbers
            data[-1].append([int(n) for n in mappings])
        else:         # line has no numbers, new map
            # note that this also runs for the first map, necessary bc it
            # has to run once for the -1 index above to work
            data.append([])

p1closest = min([get_location(data, s) for s in seeds])
p2closest = min([get_location(data, s) for (s0, span) in zip(*[iter(seeds)]*2) for s in range(s0, s0+span)])

print(f'Part 1: {p1closest}')
print(f'Part 2: {p2closest}')
