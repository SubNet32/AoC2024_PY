import time
import re
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read()

groups = re.findall(r"(mul\(\d{1,3},\d{1,3}\))|(do\(\))|(don't\(\))", file)
expressions = [x for row in groups for x in row if x != ""]
sum = 0
enabled = True
for e in expressions:
    if(e == "do()"):
        enabled = True
        continue
    if(e == "don't()"):
        enabled = False
        continue
    if(not enabled):
        continue
    a,b = str(e).replace("mul(", "").replace(")", "").split(",")
    sum += int(a)*int(b)

print("--- %s seconds ---" % (time.time() - start_time))
print("result", sum)