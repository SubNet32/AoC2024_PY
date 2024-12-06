import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

sequence = ["X","M","A","S"]
directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
field = []

for line in file:
    field.append([c for c in line])


def checkSequence(seq: list, direction: tuple, x: int, y: int):
    x += direction[0]
    y += direction[1]
    if(x < 0 or x >= len(field[0]) or y < 0 or y >= len(field)):
        return False
    expected = seq.pop(0)
    if(field[y][x] != expected):
        return False
    if(len(seq) > 0):
        return checkSequence(seq, direction, x, y)
    return True

sum = 0
for y in range(len(field)):
    for x in range(len(field[y])):
        if(field[y][x] != sequence[0]): continue
        for direction in directions:
            if(checkSequence(sequence[1::], direction, x, y)):
                sum += 1



print("--- %s seconds ---" % (time.time() - start_time))
print("result", sum)