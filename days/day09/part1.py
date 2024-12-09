import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

diskMap = [int(x) for x in file[0]]

empty = -1
blocks = []
id = 0
for i,c in enumerate(diskMap):
    if i % 2 == 0:
        blocks += [id for n in range(c)]
        id += 1
    else:
        blocks += [empty for n in range(c)]
    
def calcCheckSum(blocks:list):
    return sum([v*i if v != empty else 0 for i,v in enumerate(blocks)])

placer = 0
picker = len(blocks) - 1
while(placer < picker):
    while(blocks[placer] != empty and placer < picker):
        placer += 1
    while(blocks[picker] == empty and picker > placer):
        picker -= 1
    if(placer == picker):
        break
    r = blocks.pop(picker)
    picker -= 1
    blocks[placer] = r


print("--- %s seconds ---" % (time.time() - start_time))
print("result", calcCheckSum(blocks))