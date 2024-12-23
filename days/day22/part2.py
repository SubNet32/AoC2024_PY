import time
import math
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()


def evolveNumber(number:int):
    number = (number ^ (number * 64)) % 16777216
    number = (number ^ math.floor(number / 32)) % 16777216
    number = (number ^ (number * 2048)) % 16777216
    return number

changes = dict[int, dict[list[int], int]]()
for lineOfFile in file:
    line = int(lineOfFile)
    n = line
    prevValue = line % 10
    priceChanges = dict[list[int], int]()
    currentChanges = []
    for i in range(2000):
        n = evolveNumber(n)
        value = n % 10
        currentChanges.append(value-prevValue)
        if(len(currentChanges) > 4):
            currentChanges.pop(0)
        if(i >= 3):
            key = tuple(currentChanges)
            if(not key in priceChanges):
                priceChanges[key] = value
      
        prevValue = value
    changes[line] = priceChanges

linesToTest = set[tuple[int,int,int,int]]()
for k in changes: 
    for line in changes[k]:
        linesToTest.add(line)
result = 0
bestSeq = tuple()
for line in linesToTest:
    total = 0
    for c in changes:
        if(line in changes[c]):
            total += changes[c][line]
    if(result == 0 or result < total):
        bestSeq = line
        result = total


print("--- %s seconds ---" % (time.time() - start_time))
print("bestSeq", bestSeq)
print("result", result)

