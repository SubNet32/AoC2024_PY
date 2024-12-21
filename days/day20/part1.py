import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

def move(pos: tuple[int], direction: tuple[int]):
    return (pos[0] + direction[0], pos[1] + direction[1])

directions =[(1, 0), (0, 1), (-1, 0), (0, -1)]
positions = set[tuple[int]]()
start = (0, 0)
end = (0,0)
for y, line in enumerate(file):
    for x, char in enumerate(line):
        if char == "." or char == "S" or char == "E":
            positions.add((x, y))
        if char == "S":
            start = (x, y)
        if char == "E":
            end = (x, y)

path = dict[tuple[int], int]()
pos = start
t = 0
path[pos] = t

while pos != end:
    t += 1
    for d in directions:
        p1 = move(pos,d)
        if p1 in positions and p1 not in path:
            pos = p1
            path[pos] = t
            break

saved = dict[int, int]()
total = 0
for pos in path:
    for d in directions:
        p1 = move(pos,d)
        if p1 in path:
            continue
        for d in directions:
            p2 = move(p1,d)
            if p2 in path:
                save = path[p2] - path[pos] - 2
                if(save >= 100):
                    total += 1
                    if(save not in saved):
                        saved[save] = 1
                    else:
                        saved[save] += 1


print("--- %s seconds ---" % (time.time() - start_time))
print("result", total)