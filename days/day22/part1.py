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

result = 0
for line in file:
    n = int(line)
    for i in range(2000):
        n = evolveNumber(n)
    result += n

print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)