from sys import argv

def num_winning_ways(time, dist):
    race_total = 0
    for charge in range(1, time):  # for each charge time
        if charge*(time - charge) > dist:  # breaks the record
            race_total += 1
        elif race_total: break  # short-circuit once we're charging too long
    
    return race_total

with open(argv[1]) as f:
    times = [int(t) for t in f.readline().split(':')[1].split()]
    dists = [int(d) for d in f.readline().split(':')[1].split()]

# Part 1
p1total = 1
for t, d in zip(times, dists):  # for each race
    p1total *= num_winning_ways(t, d)

# Part 2
time = int(''.join(map(str, times)))
distance = int(''.join(map(str, dists)))

p2total = num_winning_ways(time, distance)

print(f'Part 1: {p1total}')
print(f'Part 2: {p2total}')
