# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import numpy
import hashlib
import json
import sys, os

mean = 0.0
var = float(sys.argv[2])

if __name__ == '__main__':

    numpy.random.seed(1)
    data = [ numpy.array([ float(x) for x in line ]) * 10.0 for line in json.load(open(sys.argv[1])) ]
    K = len(data[0])

    N = len(data)
    L = 500
    k_ = 3
    
    Lx = numpy.zeros((L, N, k_))

    pstable_hash = {}

    average = numpy.zeros((N, k_))
    for L_ in range(L):
        
        a_ = [ list(numpy.random.normal(mean, var, size = K)) for i in range(k_) ]
        
        for i in range(len(data)):
            g = numpy.array([ numpy.dot(a_[l], data[i]) for l in range(k_) ])
            Lx[L_][i] = g

            average[i] += Lx[L_][i] 

    average /= L

    for i, avg in enumerate(average):
        key = ''.join([ str('%.1f' % round(j, 1)) for j in avg ])

        try:
            pstable_hash[key].append(data[i])
        except KeyError:
            pstable_hash[key] = [ data[i] ]

    for h, item in pstable_hash.items():
        print(h, item)
