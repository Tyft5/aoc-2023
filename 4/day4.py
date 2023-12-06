from sys import argv
import re

p1total = 0
mtchs = []
for line in open(argv[1]):
    # split into two sets of numbers and parse into arrays
    winning, mine = (re.findall('\d+', p) for p in line.split(':')[1].split('|'))
    
    # number of matches
    matches = len([n for n in mine if n in winning])

    # casting to int eliminates scores < 1, i.e., no matches
    p1total += int(2**(matches-1))

    # store the # of matches for part 2
    mtchs.append(matches)

# array with number of cards, start with 1 OG
cards = [1] * len(mtchs)
# for each card
for i in range(len(cards)):
    # for each following card, based on # of matches
    for j in range(1, mtchs[i] +1):
        # bounds check        we get (# this card) additional later cards
        if i+j < len(cards): cards[i+j] += cards[i]

# total number of cards
p2total = sum(cards)

print(f'Part 1: {p1total}')
print(f'Part 2: {p2total}')
