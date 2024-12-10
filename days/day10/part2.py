import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

field = []
trailHeads = []
directions = [(1,0), (0,1), (-1,0), (0,-1)]
maxY = len(file)-1
maxX = len(file[0])-1
for y, line in enumerate(file):
    xLine = []
    for x, c in enumerate(line):
        xLine.append(int(c))
        if(c == "0"):
            trailHeads.append((x,y))
    field.append(xLine)
    

def printField(positions: list, mark = "X",):
    if(len(field) > 20):
        return
    for y in range(len(field)):
        line = ""
        for x in range(len(field[y])):
            if((x,y) in positions):
                line += mark
            else:
                line += str(field[y][x])
        print(line)
    print()

def checkOutOfBounds(pos: tuple):
    return (pos[0] < 0 or pos[0] >= len(field[0]) or pos[1] < 0 or pos[1] >= len(field))


def addPosition(pos: tuple, dir: tuple):
    return (pos[0] + dir[0], pos[1] + dir[1])

def getValue(pos: tuple):
    return field[pos[1]][pos[0]]

def checkTrail(pos: tuple, prevValue: int):
    result = 0
    for dir in directions:
        nextPos = addPosition(pos, dir)
        if(checkOutOfBounds(nextPos)):
            continue
        value = getValue(nextPos)
        if(value != prevValue+1):
            continue
        if(value == 9):
            result += 1
            continue
        
        result += checkTrail(nextPos, value)
    return result

result = 0
while(True):
    if(len(trailHeads) == 0):
        break
    trailHead = trailHeads.pop(0)
    foundPeaks = checkTrail(trailHead, 0)
    result += (foundPeaks)
    
   

print("--- %s seconds ---" % (time.time() - start_time))
print("result", (result))