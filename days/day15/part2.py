import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()
replaces = { "#" : "##", "@" : "@.", "O": "O.", ".": ".."}

def move(pos: tuple, dir: tuple):
    return (pos[0] + dir[0], pos[1] + dir[1])

def isWall(pos: tuple):
    return pos in walls

def isBox(pos: tuple):
    if(pos in boxes):
        return pos
    leftPos = move(pos, (-1,0))
    if(leftPos in boxes):
        return leftPos
    return False

def getBoxArea(box: tuple[int]):
    return [box, move(box, (1,0))]

def canMoveBox(box: tuple[int], dir: tuple[int]) -> tuple[bool, list[tuple[int]]]:
    isHorizontal = dir == directionMap["<"] or dir == directionMap[">"]
    isMovingRight = dir == directionMap[">"]
    boxesToMove : list[tuple[int]] = [box]
    newPos = move(box, dir)
    positionsToCheck =  [newPos]
    if(not isHorizontal):
        positionsToCheck.append(move(newPos, (1,0)))
    elif(isMovingRight):
        positionsToCheck.append(move(newPos, (1,0)))
    for pos in positionsToCheck:
        if(isWall(pos)):
            return False, []
        foundBox = isBox(pos)
        if(foundBox and foundBox not in boxesToMove):
            canMoveFoundBox, boxesToMoveFoundBox = canMoveBox(foundBox, dir)
            if(not canMoveFoundBox):
                return False, []
            for next in boxesToMoveFoundBox:
                if(next not in boxesToMove):
                    boxesToMove.append(next)
    return True, boxesToMove


def checkRobotMovement(robot: tuple[int], dir: tuple[int]) -> tuple[bool, list[tuple[int]]]:
    newPos = move(robot, dir)
    if(isWall(newPos)):
        return False, []
    checkForBox = isBox(newPos)
    if(checkForBox):
        return canMoveBox(checkForBox, dir)
    return True, []

boxes : dict[tuple[int]] = {}
walls : dict[tuple[int]] = {}
robot : tuple[int] = (0,0)
directionMap = { "^" : (0,-1), ">" : (1,0), "v" : (0,1), "<" : (-1,0)}
directions =  [directionMap[x] for x in directionMap]
instructions: list[tuple[int]] = []

maxX = 0
maxY = 0
for y, line in enumerate(file):
    if(len(line) == 0):
        continue
    if(line[0] in directionMap):
        instructions += ([directionMap[x] for x in line])
        continue
    maxY = y
    line = str.join("", [replaces[x] for x in line])
    maxX = max(maxX, len(line)-1)
    for x, char in enumerate(line):
        if(char == "O"):
            boxes[(x,y)] = 1
        elif(char == "#"):
            walls[(x,y)] = 1
        elif(char == "@"):
            robot = (x,y)


def printField():
    for y in range(0, maxY+1):
        line = ""
        x = 0
        while(x <= maxX):
            if((x,y) in boxes):
                line += "[]"
                x += 1
            elif((x,y) in walls):
                line += "#"
            elif((x,y) == robot):
                line += "@"
            else:
                line += "."
            x += 1
        print(line)
    print()

printField()

for instruction in instructions:
    canMove, boxesToMove = checkRobotMovement(robot, instruction)
    # print("instruction", [x for x in directionMap if directionMap[x] == instruction])
    if(not canMove):
        # print("can not move")
        # printField()
        continue
    if(len(boxesToMove) > 0):
        for box in reversed(boxesToMove):
            boxes.pop(box)
            boxes[move(box, instruction)] = 1
    robot = move(robot, instruction)

    # printField()

printField()

result = 0
for box in boxes:
    result += box[0] + box[1] * 100

print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)