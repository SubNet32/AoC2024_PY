import time
from collections import deque
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

field = []
directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
sequence = ["M","M", "S", "S"]

for line in file:
    field.append([c for c in line])


def getEdges(x: int, y: int):
    edges = []
    for direction in directions:
        dx = x + direction[0]
        dy = y + direction[1]
        if(dx < 0 or dx >= len(field[0]) or dy < 0 or dy >= len(field)):
            continue
        edges.append(field[dy][dx])
    return edges

sum = 0
for y in range(len(field)):
    for x in range(len(field[y])):
        if(field[y][x] != "A"): continue
        edges = getEdges(x, y)
        if(len(edges) != 4): continue
        d = deque(edges)
        for i in range(4):
            d.rotate(1)
            if((list(d) == sequence)):
                sum += 1
                break





print("--- %s seconds ---" % (time.time() - start_time))
print("result", sum)