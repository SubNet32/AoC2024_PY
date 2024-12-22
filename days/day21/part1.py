import time
from pathlib import Path

from termcolor import colored 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()


# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
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


#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
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


def getMoveSeq(start: tuple[int], target: tuple[int], pad: dict[str, tuple[int, int]]):
    seq = []
    pos = start
    dx = target[0] - pos[0]
    dy = target[1] - pos[1]
    if(dx == 0 and dy == 0):
        return seq
        
    def moveX():
        for _ in range(abs(dx)):
            seq.append(directionsX[0 if dx > 0 else 1])
    def moveY():
        for _ in range(abs(dy)):
            seq.append(directionsY[0 if dy > 0 else 1])

    if(start[1] == pad["E"][1] and target[0] == pad["E"][0]):
        moveY()
        moveX()
    else:
        moveX()
        moveY()
    return seq


def translate(seq: list[str], source:  dict[str, tuple[int, int]]):
    pos = source["A"]
    outSeq = []
    for e in seq:
        targetPos = source[e]
        moveSeq = getMoveSeq(pos, targetPos, source)
        # print(e, " -> ", moveSeq+["A"])
        pos = targetPos
        outSeq += moveSeq
        outSeq.append("A")
    return outSeq

def sign(x:int):
    if(x == 0):
        return 0
    return 1 if x > 0 else -1

def getPaths(pos: tuple[int], target: tuple[int], path:list[str]):
    dx = sign(target[0] - pos[0])
    dy = sign(target[1] - pos[1])
    if(dx == 0 and dy == 0):
        return [path]
    result = []
    px = (pos[0] + dx, pos[1])
    py = (pos[0], pos[1] + dy)
    if(dx != 0 and px != numPad["E"]):
        left = dx < 0
        dir = directionsX[1 if left else 0]
        result += getPaths(px, target, path + [dir])
    if(dy != 0 and py != numPad["E"]):
        up = dy < 0
        dir = directionsY[1 if up else 0]
        result += getPaths(py, target, path + [dir])
    return result

result = 0
for line in file:
    pos = "A"
    totalLen = 0
    for e in line:
        paths = getPaths(numPad[pos], numPad[e], [])
        pos = e
        best = 1e10
        for test in paths:
            test += ["A"]
            r1 = translate(test, movePad)
            r2 = translate(r1, movePad)
            best = min(best, len(r2))
        totalLen += best
    result += totalLen * int(line[:-1])


print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)

# > 222102
# < 229246
# < 235218
# not 224782
# not 233106

# AAvAA^<A>Av<A^>AA<A>Av<A<A>>^AAA<A>vA^A
# AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A

# <A = 18
# >A = 10
# vA = 16
# ^A = 12

# <A ^A >^^A vvvA
# 18 12  20   18

