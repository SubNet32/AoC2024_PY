import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

stones = {}

def addStones(newNumbers: set, number: int, stoneCount: int):
    if number in newNumbers:
        newNumbers[number] += stoneCount
    else:
        newNumbers[number] = stoneCount

for s in file[0].split():
    addStones(stones, int(s), 1)


for step in range(75):
    newStones = { }
    for stone in stones:
        if(stone == 0):
            addStones(newStones, 1, stones[stone])
            continue
        stoneLen = len(str(stone))
        if(stoneLen  % 2 == 0):
            halfStoneLen = int(stoneLen / 2)
            first = int(str(stone)[:halfStoneLen])
            second = int(str(stone)[halfStoneLen:])
            addStones(newStones, first, stones[stone])
            addStones(newStones, second, stones[stone])
            continue
        addStones(newStones, stone * 2024, stones[stone])
    stones = newStones

print("--- %s seconds ---" % (time.time() - start_time))
print("result", sum([x for x in stones.values()]))