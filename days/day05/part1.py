import time
import math
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read().splitlines()



rules = {}
sequences = []

for line in file:
    if(len(line) == 0): continue
    if(line.find("|") != -1):
        v,b = [int(x) for x in line.split("|")]
        if(v not in rules):
            rules[v] = [b]
        else:
            rules[v].append(b)
        continue
    sequences.append([int(x) for x in line.split(",")])



def checkSequence(seq: list):
    for i in range(len(seq)-1):
        e = seq[i]
        for j in range(i+1, len(seq)):
            f = seq[j]
            if(f not in rules): continue
            if(e in rules[f]):
                print("failed sequence", seq, "because", e, "is in", f, rules[f])
                return False
    return True


result = 0
for sequence in sequences:
    if(checkSequence(sequence)):
        result += sequence[math.floor(len(sequence)/2)]


print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)