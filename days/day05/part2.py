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




def sortSequence(seq: list, movedAfter: dict):
    for i in range(len(seq)-1):
        e = seq[i]
        for j in range(i+1, len(seq)):
            f = seq[j]
            if(f not in rules): continue
            if(e in rules[f]):
                # print("failed sequence", seq, "because", e, "must be after", f, rules[f])
                rem = seq.pop(i)
                seq.insert(j,rem)
                if(f in movedAfter):
                    movedAfter[f].append(e)
                else:
                    movedAfter[f] = [e]
                
                if(e in movedAfter):
                    for m in movedAfter[e]:
                        fr = seq.pop(seq.index(m))
                        seq.insert(j, fr)
                return sortSequence(seq, movedAfter)
    return seq


result = 0
for sequence in sequences:
    sortedSeq = sortSequence(sequence.copy(), {})
   
    if(sortedSeq == sequence):
        continue
    result += sortedSeq[math.floor(len(sortedSeq)/2)]


print("--- %s seconds ---" % (time.time() - start_time))
print("result", result)