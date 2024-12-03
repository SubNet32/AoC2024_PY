import time
import re
from pathlib import Path 
start_time = time.time()
cwd = Path(__file__).parent
path = cwd.joinpath("input.txt")
file = open(path, "r").read()

expressions = re.findall(r"mul\(\d{1,3},\d{1,3}\)", file)

sum = 0
for e in expressions:
    a,b = str(e).replace("mul(", "").replace(")", "").split(",")
    sum += int(a)*int(b)

print("--- %s seconds ---" % (time.time() - start_time))
print("result", sum)