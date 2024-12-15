import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

def move(pos: tuple, dir: tuple):
    return (pos[0] + dir[0], pos[1] + dir[1])

def isWall(pos: tuple):
    return pos in walls

def isBox(pos: tuple):
    return pos in boxes

def checkMovement(robot: tuple[int], dir: tuple[int]) -> tuple[bool, list[tuple[int]]]:
    boxesToMove : list[tuple[int]] = []
    newPos = robot
    while(True):
        newPos = move(newPos, dir)
        if(isWall(newPos)):
            return False, {}
        if(isBox(newPos)):
            boxesToMove.append(newPos)
            continue
        return True, boxesToMove

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
        for x in range(0, maxX+1):
            if((x,y) in boxes):
                line += "O"
            elif((x,y) in walls):
                line += "#"
            elif((x,y) == robot):
                line += "@"
            else:
                line += "."
        print(line)
    print()

printField()

for instruction in instructions:
    canMove, boxesToMove = checkMovement(robot, instruction)
    # print("instruction", instruction)
    if(not canMove):
        # print("can not move")
        # print()
        continue
    if(len(boxesToMove) > 0):
        boxToMove = boxesToMove.pop(0)
        boxes.pop(boxToMove)
        if(len(boxesToMove) > 0):
            boxToMove = boxesToMove.pop(-1)
        boxToMove = move(boxToMove, instruction)
        boxes[boxToMove] = 1
    
    robot = move(robot, instruction)

#     printField()

# printField()

result = 0
for box in boxes:
    result += box[0] + box[1] * 100

print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)