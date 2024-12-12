import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()


field = []
directions = [(1,0), (0,1), (-1,0), (0,-1)]
maxY = len(file)-1
maxX = len(file[0])-1
for y, line in enumerate(file):
    field.append([x for x in line])

def checkOutOfBounds(pos: tuple):
    return (pos[0] < 0 or pos[0] > maxX or pos[1] < 0 or pos[1] > maxY)

def addPosition(pos: tuple, dir: tuple):
    return (pos[0] + dir[0], pos[1] + dir[1])

def getValue(pos: tuple) -> str:
    return field[pos[1]][pos[0]]

def printField(fieldToPrint: list):
    if(len(fieldToPrint) > 20):
        return
    for y in range(len(fieldToPrint)):
        line = ""
        for x in range(len(fieldToPrint[y])):
            line += str(fieldToPrint[y][x])
        print(line)
    print()

def assignIdTo(value: str, id: int, pos: tuple):
    field[pos[1]][pos[0]] = id
    for dir in directions:
        nextPos = addPosition(pos, dir)
        if(checkOutOfBounds(nextPos)):
            continue
        nextPosVal = getValue(nextPos)
        if(isinstance(nextPos, int)): 
            continue
        if(nextPosVal != value):
            continue
        assignIdTo(value, id, nextPos)

uid = 0
for y in range(maxY+1):
    for x in range(maxX+1):
        if(isinstance(getValue((x,y)), int)):
            continue
        assignIdTo(getValue((x,y)), uid, (x,y))
        uid += 1
      

def calcRegion(region:int,pos: tuple, checkedPos: set):
    checkedPos[pos] = 1
    area = 1
    fences = 0
    for dir in directions:
        adjPos = addPosition(pos, dir)
        if(checkOutOfBounds(adjPos)):
            fences += 1
            continue
        if(adjPos in checkedPos):
            continue
        value = getValue(adjPos)
        if(value != region):
            fences += 1
            continue
        a,f = calcRegion(region, adjPos, checkedPos)
        area += a
        fences += f
    return (area, fences)


regionsChecked = {}
sum = 0
for y in range(maxY+1):
    for x in range(maxX+1):
        r = getValue((x,y))
        if(r in regionsChecked):
            continue
        regionsChecked[r] = 1
        area, fences = calcRegion(r, (x,y), {})
        # print("region",r,"has area:", area, "  fences:", fences)
        sum += area * fences


print("--- %s seconds ---" % (time.time() - start_time))
print("result", sum)