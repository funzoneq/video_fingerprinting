
import sys
import Image
from math import *
from collections import namedtuple
import json

from glob import glob

vector = namedtuple("vector", "x y")
vector.length = lambda self: sqrt(self.x**2 + self.y**2)

RA = namedtuple("RA","r a")
vector2ra = lambda v: RA(v.length(), atan2(v.y, v.x)) #4&5

def G(data, x, y):
    return vector( data[x+1,y]-data[x-1,y], data[x,y+1]-data[x,y-1] ) #2&3

def main():
    
    for pattern in sys.argv[1:]:
        result = []
        files = sorted(glob(pattern))
        for filename in files:
            try:
                img = Image.open( filename )
            except:
                print >>sys.stderr, "couldn't open", filename
                continue
            
            data = img.load()
            ras = []
            for y in xrange(1,img.size[1]-1):
                for x in xrange(1,img.size[0]-1):
                    g = G(data, x, y)
                    ra = vector2ra(g)
                    ras.append( ra )
        
            c = sum(map(lambda x: x.r*x.a, ras)) / sum(map(lambda x: x.r, ras)) #6
            
            result.append( c )
        print json.dumps(result)
    
if __name__ == "__main__":
    main()