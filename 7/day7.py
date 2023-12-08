from sys import argv
from collections import defaultdict
import bisect

# Helper function to find the type of a hand
def get_type(hand: str, p: bool):
    cards = defaultdict(lambda: 0)
    for c in hand: cards[c] += 1

    weird = not p and 'J' in cards.keys()
    num_c = len(cards)

    if not weird:
        if num_c == 1:                              return 6 # 5oaK
        elif num_c == 2:
            if list(cards.values())[0] in (1, 4):   return 5 # 4oaK
            else:                                   return 4 # FH
        elif num_c == 3:
            if max(list(cards.values())) == 3:      return 3 # 3oaK
            else:                                   return 2 # 2P
        elif num_c == 4:                            return 1 # 1P
        else:                                       return 0 # HC
    else:
        num_J = cards['J']
        if num_c <= 2:                              return 6 # 5oaK
        elif num_c == 3:
            if num_J > 1:                           return 5 # 4oaK
            elif max(list(cards.values())) == 3:    return 5 # 4oaK
            else:                                   return 4 # FJ
        elif num_c == 4:                            return 3 #3oaK
        else:                                       return 1 # 1P

# Helper function to convert a hand string to a hex int
def hex_convert(hand: str, p: bool):
    h = '0x'
    for d in hand:
        if d == 'T':            h += 'a'
        elif d == 'J' and p:    h += 'b'
        elif d == 'J':          h += '1'
        elif d == 'Q':          h += 'c'
        elif d == 'K':          h += 'd'
        elif d == 'A':          h += 'e'
        else:                   h += d

    return int(h, 16)

# Read input into list
p1hands = [[] for _ in range(7)]
p2hands = [[] for _ in range(7)]

for line in open(argv[1]):
    hand, bid = line.split()

    p1hexhand = hex_convert(hand, True)
    p2hexhand = hex_convert(hand, False)

    p1type = get_type(hand, True)
    p2type = get_type(hand, False)
    
    # insort keeps the sublists sorted
    bisect.insort(p1hands[get_type(hand, True)], (p1hexhand, int(bid)), key=lambda x: x[0])
    bisect.insort(p2hands[get_type(hand, False)], (p2hexhand, int(bid)), key=lambda x: x[0])

# find winnings
# sum flattens into one sorted list
p1total = sum([bid*(i+1) for i, (hand, bid) in enumerate(sum(p1hands, []))])
p2total = sum([bid*(i+1) for i, (hand, bid) in enumerate(sum(p2hands, []))])

print(f'Part 1: {p1total}')
print(f'Part 2: {p2total}')
