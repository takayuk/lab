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


def boost2(dataset):

    T = 3
    M = 3
    (N, K) = ( len(dataset), len(dataset[0][0]) )

    D = numpy.zeros((M, N), dtype = numpy.float64)
    D[0] = numpy.ones(N, dtype = numpy.float64) / N 

    #err = numpy.zeros(M, dtype = numpy.float64)
    alpha = numpy.zeros(M, dtype = numpy.float64)

    h = []

    for t in range(T-1):

        for k in range(K):
            (x, y) = ([ [d[0][k]] for d in dataset ], [ float(d[1]) for d in dataset ])
            
            problem = svm_problem(y, x)
            param = svm_parameter('-s 0 -t 0 -q')

            learning = svm_train(problem, param)
            h.append(learning)
            
            label = svm_predict(y, x, learning)

            f_bool2bin = lambda x: 1 if x else 0
            ans = [ f_bool2bin(l == r) for l, r in zip(label[0], y) ]

            #err[t] = sum([ D[t][i] * ans[i] for i in range(N) ])
            err = sum([ D[t][i] * ans[i] for i in range(N) ])
            print(err)
            try:
                #alpha[t] = math.log( (1.0-err[t]) / err[t] ) / 2
                alpha[t] = math.log( (1.0-err) / err ) / 2
            except ValueError:
                print((1.0-err[t])/err[t])

            for i in range(N):
                D[t+1][i] = D[t][i] * math.exp(-alpha[t] * ans[i])
            
            D[t] /= D[t].sum()

    

def boost(dataset):

    T = 10
    K = len(dataset[0][0])

    D = len(dataset)

    w = numpy.ones((T, D), dtype = numpy.float64) / D
    
    e = numpy.zeros(T, dtype = numpy.float64)

    #thresh = 0.005

    alpha = numpy.zeros(T, dtype = numpy.float64)

    h = []

    for t in range(T):

        #k = 0
        #d = numpy.zeros(D, dtype = int)

        for k in range(K):

            local_h = []
            for th in numpy.arange(-0.1, 0.1, step = 0.001):
                f = lambda x: 1 if x > th else -1
                pred = [ f(x[0][k]) for x in dataset ]
                kotaeawase = [ p for p, t in zip(pred, [ x[1] for x in dataset ]) if p == t ]
                seikai_rate = float(len(kotaeawase)) / D

                if len(local_h) == 0:
                    local_h.append((seikai_rate, th))
                elif seikai_rate > local_h[-1][0]:
                    local_h.append((seikai_rate, th))

            h.append(local_h[ local_h.index(max(local_h)) ])

        print(h)
        break
        """
        for i, data in enumerate(dataset):
            (x, y) = data
            d[i] = 1 if x > thresh else 0

            e[t] = sum([ w[t-1][i] for x in range(D) ]) / D
            alpha[t] = math.log( (1.0 - e[t]) / e[t] )
            w[t+1][i] = w[t][i] * math.exp( ((-1)**d[i]) * alpha[t] )

        print(e)
        print(alpha)
        print(w)
        """


if __name__ == '__main__':

    numpy.random.seed(64)
    D = 15
    K = 4

    dataset = zip([ [ numpy.random.normal(1, 1.2) for j in range(K) ] for i in range(D) ], [1] * D)
    dataset += zip([ [ numpy.random.normal(-1, 1.2) for j in range(K) ] for i in range(D) ], [-1] * D)
    #print(dataset)
    
    D = len(dataset)

    boost2(dataset)
    
    #f_z2n = lambda x: -1 if x == 0 else 1
    #data = [ numpy.random.dirichlet( numpy.ones(K, dtype = numpy.float64) ) for i in range(D) ]
    #dataset = zip(numpy.random.dirichlet( numpy.ones(D, dtype = numpy.float64) / D ), [ f_z2n(numpy.random.randint(2)) for i in range(D) ])
    #dataset = zip(data, [ f_z2n(numpy.random.randint(2)) for i in range(D) ])
    #boost(dataset)

    exit()






    
    (N, K) = (20, 10)
    #(link_thresh, noise_thresh) = (0.25, 0.3)
    (link_thresh, noise_thresh) = (0.2, 0.3)

    numpy.random.seed(64)
    
    graph = numpy.zeros((N, N), dtype = numpy.int)

    z = [ numpy.random.dirichlet(numpy.ones(K)/K) for i in range(N) ]

    #g = networkx.Graph()

    edges = 0
    for i in range(N):
        for j in range(i+1, N):
            if (numpy.inner(z[i], z[j]) > link_thresh) and (numpy.random.random() > noise_thresh):
                graph[i][j] = graph[j][i] = 1
                edges += 1
                #g.add_edge(i, j)

    print( edges, (N * (N-1)) / 2 )
    """
    networkx.draw_spring(g)
    plt.savefig('graph.png')
    print(graph)
    """
    
    dataset = []
    for i in range(N):
        for j in range(i+1, N):
            if graph[i][j] > 0:
                #dataset.append(((i, j), 1))
                dataset.append(([ z[i][k] * z[j][k] for k in range(K) ], 1))
            else:
                #dataset.append(((i, j), -1))
                dataset.append(([ z[i][k] * z[j][k] for k in range(K) ], -1))

    boost(dataset)
