import time
import math
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

origin = []
field = []
directions = [(1,0), (0,1), (-1,0), (0,-1)]
diagDirections = [(1,1), (-1,-1), (-1,1), (1,-1)]
maxY = len(file)-1
maxX = len(file[0])-1
for y, line in enumerate(file):
    field.append([x for x in line])
    origin.append([x for x in line])

def checkOutOfBounds(pos: tuple):
    return (pos[0] < 0 or pos[0] > maxX or pos[1] < 0 or pos[1] > maxY)

def addPosition(pos: tuple, dir: tuple):
    return (pos[0] + dir[0], pos[1] + dir[1])

def rotPosition(pos: tuple):
    return (pos[1], -pos[0])

def getValue(pos: tuple) -> str:
    return field[pos[1]][pos[0]]

def printField(fieldToPrint: list, checkPos:list, center: tuple):
    # if(len(fieldToPrint) > 20):
    #     return
    for y in range(-1,len(fieldToPrint)+1):
        line = ""
        for x in range(-1,len(fieldToPrint[0])+1):
            if((x,y) in checkPos):
                line += "C"
            elif((x,y) == center):
                line += "X"
            elif(checkOutOfBounds((x,y))):
                line += "."
            else: line += str(fieldToPrint[y][x])
        print(line)
    print()

def printRegion(region: set):
    print([x[0] for x in region])
    minX = min([x[0] for x in region])
    maxX = max([x[0] for x in region])
    minY = min([x[1] for x in region])
    maxY = max([x[1] for x in region])
    for y in range(minY, maxY+1):
        line = ""
        for x in range(minX, maxX+1):
            if(not checkOutOfBounds((x,y))):
                # line += origin[y][x]
                if((x,y) in region):
                    line += "#"
                else:
                    line += "."
        print(line)
    print()


def init(value: str, id: int, pos: tuple):
    region = { pos: 1}
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
        region.update(init(value, id, nextPos))
    return region

uid = 0
regions = {}
for y in range(maxY+1):
    for x in range(maxX+1):
        if(isinstance(getValue((x,y)), int)):
            continue
        regions[uid] = init(getValue((x,y)), uid, (x,y))
        uid += 1

# [print(x, regions[x]) for x in regions]

def getBasicCorner(pos: tuple, region: set):
    corners = 0
    for dir in diagDirections:
        diagPos = addPosition(pos, dir)
        if(checkOutOfBounds(diagPos) or diagPos not in region):
            if(addPosition(pos, (dir[0], 0)) in region and addPosition(pos, (0, dir[1])) in region):
                corners += 1
            if(addPosition(pos, (-dir[0], 0)) in region and addPosition(pos, (0, -dir[1])) in region and addPosition(pos, (dir[0], 0)) not in region and addPosition(pos, (0, dir[1])) not in region):
                corners += 1
        elif(addPosition(pos, (dir[0], 0)) not in region and addPosition(pos, (0, dir[1])) not in region and addPosition(pos, (-dir[0], 0)) in region and addPosition(pos, (0, -dir[1]))):
                corners += 1
    return corners

uTurnDirections = [(-1,0), (0, -1), (1, 0)]
def isUTurnCorner(pos: tuple, region: set):
    turns = uTurnDirections.copy()
    for _ in range(4):
        foundTurn = True
        checkPos = []
        for dir in turns:
            turnPos = addPosition(pos, dir)
            checkPos.append(turnPos)
            if(turnPos in region):
                foundTurn = False
                break
        # print(checkPos)
        # printField(field, checkPos, pos)
        if(foundTurn):
            return True
        turns = [rotPosition(x) for x in turns]
    return False


sum = 0
for rKey in regions:
    region = regions[rKey]
    # print("checking region", rKey)
    corner = 0
    if(len(region) == 1):
        corner = 4
    else:
        for pos in region:
            if(isUTurnCorner(pos, region)):
                # print(pos, "is u turn corner")
                corner += 2
            else:
                basicCorners = getBasicCorner(pos, region)
                corner += basicCorners
                # if(basicCorners > 0):
                #     print(pos, "has basic corners:", basicCorners)
                
            
    # print("region", rKey, "has corner:", corner, " and area:", len(region))
    if(corner % 2 != 0):
            print("this should not happen")
            printRegion(region)
            exit()
    sum += corner * len(region)
    # print()

print("--- %s seconds ---" % (time.time() - start_time))
print("result", sum)