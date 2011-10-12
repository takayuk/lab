# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import numpy
import networkx
import matplotlib.pylab as plt
import math
import copy

from svm import *
from svmutil import *


EPS = 1.0e-6

f_bool2bin = lambda x: 1 if x else 0


def boost(dataset):

    T = 10
    M = 3
    (N, K) = ( len(dataset), len(dataset[0][0]) )

    w = [ numpy.ones(N, dtype = numpy.float64) / N ]

    alpha = numpy.zeros(M, dtype = numpy.float64)

    miss_classified_table = numpy.ones(N, dtype = int)

    h = []

    param = svm_parameter('-s 0 -t 0 -q')
    
    for t in range(T-1):

        data = [ (dataset[i][0], dataset[i][1], i) for i, x in enumerate(miss_classified_table) if x == 1 ]
        (tr_data, tr_labels) = ( [ x[0] for x in data ] , [ float(x[1]) for x in data ] )
        
        problem = svm_problem(tr_labels , tr_data)
            
        learning = svm_train(problem, param)
        pred_labels = svm_predict(tr_labels, tr_data, learning)

        h.append(learning)

        d = [ f_bool2bin(l == r) for l, r in zip(pred_labels[0], tr_labels) ]
        err = sum([ w[t][x[2]] * d[i] for i, x in enumerate(data) ]) / len(data)
        alpha[t] = math.log( (1.0-err) / err ) / 2

        w.append(copy.deepcopy(w[t]))
        for i, x in enumerate(data):
            w[t+1][x[2]] = w[t][x[2]] * math.exp( -alpha[t] * d[i] )

        for i, x in enumerate(data):
            if d[i] == 1: miss_classified_table[x[2]] = 0

        if len([ t for t in miss_classified_table if t == 1 ]) == 0:
            break

    data = [ (dataset[i][0], dataset[i][1], i) for i in range(N) ]
    (tr_data, tr_labels) = ( [ x[0] for x in data ] , [ float(x[1]) for x in data ] )


    valid = list(numpy.random.dirichlet( numpy.ones(K) / K ))
    
    sign = 0.0
    for i in range(1, len(w)):
        pred_labels = svm_predict([1], [valid], h[i-1])
        sign += alpha[i-1] * pred_labels[0][0] / alpha.sum()

    sign /= alpha.sum()

    print(sign)


if __name__ == '__main__':

    D = 100 
    K = 10

    dataset = zip([ [ numpy.random.normal(1, 1.2) for j in range(K) ] for i in range(D) ], [1] * D)
    dataset += zip([ [ numpy.random.normal(-1, 1.2) for j in range(K) ] for i in range(D) ], [-1] * D)
    
    D = len(dataset)

    boost(dataset)
