
import sys
import os
from sqed import sqed
import json

file0 = "video/90a0c369_Husky_Dogs_Singing_Gwen_Stefani.mp4.json"
file1 = "video/c370134a_A_Very_Happy_Duck.mp4.json"


with open(file0) as f:
    p = json.load(f)

with open(file1) as f:
    q = json.load(f)

N = 4
M = 2
K = 100

result = []
for k in xrange(K):
    result2 = []
    for i in xrange(N*M):
        s = (p[k][i]-q[k][i]) ** 2
        result2.append( s )
    result.append(result2)

from pprint import pprint
pprint(result)