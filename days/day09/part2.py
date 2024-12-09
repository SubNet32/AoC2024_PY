import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

diskMap = [int(x) for x in file[0]]

empty = -1
blocks = []
id = -1
for i,c in enumerate(diskMap):
    if i % 2 == 0:
        id += 1 
    blocks.append({"id":id if i % 2 == 0 else empty, "c":c})
   

def printBlocks(blocks:list):
    if(len(blocks) > 100): return
    printStr = ""
    for x in blocks:
        printStr += str.join("",[str(x["id"] if x["id"] != empty else ".") for _ in range(x["c"])])
    print(printStr)
    
def calcCheckSum(blocks:list):
    sum  = 0
    c = 0
    for i, x in enumerate(blocks):
        for _ in range(x["c"]):
            if(x["id"] != empty):
                sum += (x["id"]) * c
            c += 1
    return sum

printBlocks(blocks)

picker = len(blocks) - 1
while(True):
    while(blocks[picker]["id"] == empty and picker > 0):
        picker -= 1

    if(picker == 0):
        break
    reqSpace = blocks[picker]["c"]
    finder = 0
    while((blocks[finder]["id"] != empty or blocks[finder]["c"] < reqSpace) and finder < picker):
        finder += 1
   
    if(finder >= picker):
        picker -= 1
        continue

    r = blocks.pop(picker)
    blocks.insert(picker, {"id":empty, "c":r["c"]})
    picker -= 1

    blocks[finder]["c"] -= reqSpace
    if(blocks[finder]["c"] == 0):
        blocks[finder] = r
    else:
        blocks.insert(finder, r)
        picker += 1
    printBlocks(blocks)


print("--- %s seconds ---" % (time.time() - start_time))
print("result", calcCheckSum(blocks))