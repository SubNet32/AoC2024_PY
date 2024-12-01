import time
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = str(cwd) + "\\input.txt"
file = open(path, "r").read().splitlines()

listA = []
listB = []

for line in file:
    terms = [int(x) for x in str.split(line, "   ")]
    listA.append(terms[0])
    listB.append(terms[1])

listA.sort()
listB.sort()

sum = 0
for i in range(len(listA)):
    sum += abs(listA[i] - listB[i])

print("--- %s seconds ---" % (time.time() - start_time))
print("result", sum)
