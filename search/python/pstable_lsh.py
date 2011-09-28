# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import numpy

import hashlib


mean = 0.0
var = 0.1
K = 2


def to_hash(a, n):

    K = len(n)

    """
    g = [0] * K
    for i in range(K):
        g[i] = sum([n[k] * a[i][k] for k in range(K)])
    """
    g = sum([n[k] * a[0][k] for k in range(K)])
    
    #return [ sum([n[k] * a[i][k] for k in range(K)]) for i in range(K) ]
    return g

"""
def new_lshkey(x, y):

    #g = to_hash(x, y)
    g = to_hash(n)
    keys = [int(round(g[i])) for i in range(K)]
    
    #return md5.new(''.join([str(_) for _ in keys])).hexdigest()
    return hashlib.md5(''.join([str(_) for _ in keys])).hexdigest()


def new_hashtable(nodes):

    table = {}
    for n in nodes:
        key = new_lshkey(n[0], n[1])

        try:
            table[key].append(n)
        except KeyError:
            table.setdefault(key, [n])

    return table
"""

if __name__ == '__main__':

    #import matplotlib.pylab as plt
    plotsx = list(numpy.random.normal(1.0, 0.5, 1000))
    plotsy = list(numpy.random.normal(1.0, 0.5, 1000))

    plotsx += list(numpy.random.normal(-1.0, 0.5, 1000))
    plotsy += list(numpy.random.normal(-1.0, 0.5, 1000))

    scale = 10.0
    plotsx = [ x * scale for x in plotsx ]
    plotsy = [ y * scale for y in plotsy ]
    
    #plt.plot(plotsx, plotsy, ',')

    L = 200
    tables = []
    for l in range(L):
        t = {}
        a = [list(abs(numpy.random.normal(mean, var, K))) for i in range(K)]
        for n in zip(plotsx, plotsy):
            key = to_hash(a, n)
            key = round(key, 4)
            #key = [ round(k, 4) for k in key ]
            #key = hashlib.md5(''.join([str(y) for y in key]))
            try:
                t[key].append(n)
            except KeyError:
                t.setdefault(key, [n])

        tables.append((t, a))

    queryx = numpy.random.normal(1.0, 0.5)
    queryy = numpy.random.normal(1.0, 0.5)

    queryx *= scale
    queryy *= scale

    sr = []
    for ts in tables:
        k = to_hash(ts[1], (queryx, queryy))
        k = round(k, 4)
        #k = [ round(kk, 4) for kk in k ]
        #k = hashlib.md5(''.join([str(y) for y in k]))
        if k in ts[0]:
            sr += ts[0][k]

    print((queryx, queryy))
    print(set(sr))

    import math
    mindist = 10000000.0
    nei = None
    for x, y in zip(plotsx, plotsy):
        dist = math.sqrt(((queryx - x) ** 2) + ((queryy - y) ** 2))

        if dist < mindist:
            mindist = dist
            nei = (x, y)

    print(nei)
    #plt.savefig('plot.png')
