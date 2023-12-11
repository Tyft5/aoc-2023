from sys import argv

data = [[int(i) for i in l.split()] for l in open(argv[1])]

def predict(hist, ind):
    if any(hist):
        diffs = [hist[i] - hist[i-1] for i in range(1, len(hist))]
        extended = predict(diffs, ind)
        if ind:
            return hist + [hist[ind] + extended[ind]]
        else:
            return [hist[ind] - extended[ind]] + hist
    elif ind:
        return hist + [0]
    else:
        return [0] + hist

p1total = sum([predict(d, -1)[-1] for d in data])
print(f'Part 1: {p1total}')

p2total = sum([predict(d, 0)[0] for d in data])
print(f'Part 2: {p2total}')