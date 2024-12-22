import time
from pathlib import Path

from termcolor import colored 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

numPad = {
    "7": (0,0),
    "8": (1,0),
    "9": (2,0),
    "4": (0,1),
    "5": (1,1),
    "6": (2,1),
    "1": (0,2),
    "2": (1,2),
    "3": (2,2),
    "E": (0,3),
    "0": (1,3),
    "A": (2,3),
}

movePad = {
   "E" : (0,0),
   "^" : (1,0),
   "A" : (2,0),
   "<" : (0,1),
   "v" : (1,1),
   ">" : (2,1),
}

# index 0 if gt 0 else 1
directionsX = [">", "<"]
directionsY = ["v", "^"]

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

def translate(seq: str, source:  dict[str, tuple[int, int]], pathSet: dict[tuple[tuple[int, int], tuple[int, int]], list[str]]):
    pos = source["A"]
    outSeq = []
    for e in seq:
        targetPos = source[e]
        if(pos != targetPos):
            moveSeq = pathSet[(pos, targetPos)]
        else:
            moveSeq = ""
        # print(e, " -> ", moveSeq+["A"])
        pos = targetPos
        outSeq.append(moveSeq+"A")
    return outSeq

lenMap = dict[tuple[str, int], int]()
def calcLen(seq: str, n : int, pathSet: dict[tuple[tuple[int, int], tuple[int, int]], list[str]]):
    if(n == 0):
        return len(seq)
    if((seq, n) in lenMap):
        return lenMap[(seq, n)]
    translated = translate(seq, movePad, pathSet)
    totalLen = 0
    for t in translated:
        totalLen += calcLen(t, n-1, pathSet)
   
    lenMap[(seq, n)] = totalLen
    return totalLen
    

def sign(x:int):
    if(x == 0):
        return 0
    return 1 if x > 0 else -1

def getPaths(pos: tuple[int], target: tuple[int], path:str, pad: dict[str, tuple[int, int]]):
    dx = sign(target[0] - pos[0])
    dy = sign(target[1] - pos[1])
    if(dx == 0 and dy == 0):
        return [str.join("", path)]
    result = []
    px = (pos[0] + dx, pos[1])
    py = (pos[0], pos[1] + dy)
    if(dx != 0 and px != pad["E"]):
        left = dx < 0
        dir = directionsX[1 if left else 0]
        result += getPaths(px, target, path + [dir], pad)
    if(dy != 0 and py != pad["E"]):
        up = dy < 0
        dir = directionsY[1 if up else 0]
        result += getPaths(py, target, path + [dir], pad)
    return result


# contains all possible paths for each two positions on the movePad
movePadPaths = dict[tuple[str, str], list[str]]()
for k in movePad:
    for k2 in movePad:
        if(k == k2 or k == "E" or k2 == "E"):
            continue
        movePadPaths[(movePad[k], movePad[k2])] = getPaths(movePad[k], movePad[k2], [], movePad)

# pathSets is the list of all possible path combinations for the movePad
# done this way to find the best path set. As it turns out it's path set 19
pathSets :list[dict[tuple[tuple[int, int], tuple[int, int]], list[str]]] = []
pathSets.append(dict[tuple[tuple[int, int], tuple[int, int]], list[str]]())
for k in movePadPaths:
    l = len(movePadPaths[k])
    pl = len(pathSets)
    if(l > 1):
        for i in range(pl):
            pathSets.append(pathSets[i].copy())
    for i, p in enumerate(pathSets):
        if(l == 1 or i < pl):
            p[k] = movePadPaths[k][0]
        else:
            p[k] = movePadPaths[k][1]
        

result = 0
bestPathSet = {}
for line in file:
    pos = "A"
    totalLen = 0
    for e in line:
        paths = getPaths(numPad[pos], numPad[e], [], numPad)
        pos = e
        best = 0
        bestPIdx = 0
        for path in paths:
            path += "A"
            p = pathSets[19] # 19 is the index of the path set with the best performance
            lenMap.clear()
            cLen = calcLen(path, 25, p)
            if(best == 0 or cLen < best):
                bestPIdx = pathSets.index(p)
                best = cLen
          
        totalLen += best
        if(bestPIdx not in bestPathSet):
            bestPathSet[bestPIdx] = 1
        else:
            bestPathSet[bestPIdx] += 1
    result += totalLen * int(line[:-1])

print("best path set", [x for x in bestPathSet])

print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)

# > 123172722057464
# > 271241695091186
# < 308324721117162

