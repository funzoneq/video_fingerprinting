
import sys
from glob import glob 
from sqed import sqed
import os
import json

def main():
    dirname = sys.argv[1]
    files = glob(os.path.join(dirname, "*.json"))
    keys = {}
    for i,f in enumerate(files):
        keys[f] = chr(ord("A")+i)
        print keys[f], "=", f
    
    print " "*5,
    for f in files:
        print "%-8s"%keys[f],
    print
    for file0 in files:
        print "%-5s"%keys[file0],
        for file1 in files:
            with open(file0) as f:
                p = json.load(f)
        
            with open(file1) as f:
                q = json.load(f)
            d = sqed( 4, 2, 100, p, q )
            print "%5f"% d,
        print
            
if __name__ == "__main__":
    main()