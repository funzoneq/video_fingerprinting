
# Squared Euclidean Distance

import sys
import json

def sqed( N, M, K, p, q ):
    total = 0
    for i in xrange(N*M):
        for k in xrange(K):
            total += (p[k][i]-q[k][i]) ** 2
    d = total / (N*M*K)
    return d

def main():
    try:
        N = int(sys.argv[1])
        M = int(sys.argv[2])
        K = int(sys.argv[3])
        pfilename = sys.argv[4]
        qfilename = sys.argv[5]
    except IndexError:
        print >>sys.stderr, "usage: {0} N M K p.json q.json".format(sys.argv[0])
        return
    
    with open(pfilename) as f:
        p = json.load(f)

    with open(qfilename) as f:
        q = json.load(f)
        
    print sqed( N, M, K, p, q )


if __name__ == "__main__":
    main()