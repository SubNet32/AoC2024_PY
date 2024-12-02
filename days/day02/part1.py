
import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()

minStep = 1
maxStep = 3

def isPairValid(a,b, dir): return b-a in range(min(minStep*dir, maxStep*dir), max(minStep*dir, maxStep*dir)+1)

def getDirection(a,b):
    if(a==b): return 0
    return 1 if b > a else -1
 
def checkTerms(terms):
    dir = getDirection(terms[0], terms[1])
    for i in range(len(terms)-1):
        if(not isPairValid(terms[i],terms[i+1], dir)):
            return False
        if(i == len(terms)-2):
            return True

result = 0
for line in file:
    terms = [int(x) for x in line.split()]
    if(checkTerms(terms)):
       result += 1
      



print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)