from sys import argv

data = [[int(i) for i in l.split()] for l in open(argv[1])]

def predict(hist):
    if any(hist):
        diffs = [hist[i] - hist[i-1] for i in range(1, len(hist))]
        extended = predict(diffs)
        return hist + [hist[-1] + extended[-1]]
    else:
        return hist + [0]

p1total = sum([predict(d)[-1] for d in data])
print(f'Part 1: {p1total}')