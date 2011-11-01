# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys, os
import numpy
import random
import copy
import math

sys.path.append(os.path.join(os.pardir, 'util'))
import similarity

import networkx
import matplotlib.pylab as plt

import optparse

from svm import *
from svmutil import *

import json


def args():

    script_usage = 'Usage: %s [options] \
            -n <num of nodes> -k <dim of topic-vec> --rseed <random seed> -o <output>' % sys.argv[0]

    parser = optparse.OptionParser(usage = script_usage)
    parser.add_option('-n', dest = 'N', type = 'int', default = 100)
    parser.add_option('-k', dest = 'K', type = 'int', default = 10)
    parser.add_option('-l', dest = 'LINK_RATE', type = 'float', default = 0.08)
    parser.add_option('--rseed', dest = 'rseed', type = 'int', default = 1)
    parser.add_option('-o', dest = 'output_path')

    (opts, args) = parser.parse_args()

    if not opts.output_path:
        parser.error(script_usage)

    return (opts, args)


if __name__ == '__main__':
   
    (options, args) = args()
   
    N = options.N
    K = options.K
    
    EPS = 1.0e-6
    EM_EPS = 1.0e-3
    
    LINK_RATE = options.LINK_RATE
    TRAIN_RATE = 0.7
 
    numpy.random.seed(options.rseed)
    random.seed(options.rseed)

    beta = numpy.random.random_sample(size = K)
    beta /= beta.sum()

    T = 0.00001
   
    n_z = []
    for i in range(N):
        z = numpy.random.random_sample(size = K)
        z /= z.sum()
        
        n_z.append(z)


    nodes = []
    linklist = []
    while True:
        linklist[:] = []
        nodes[:] = []

        for i in range(len(n_z)):
            for j in range(i+1, len(n_z)):
                
                link_prob = sum([ beta[k] * n_z[i][k] * n_z[j][k] for k in range(K) ])
                if link_prob > T:
                    linklist.append((i, j))
                    nodes += [i, j]

        linkrate = float(len(linklist) * 2) / float(N * (N-1))

        if linkrate > LINK_RATE:
            T += 0.00002
        else:
            nodes = list(set(nodes))
            break


    N_train = int(float(len(linklist)) * TRAIN_RATE)
    train = random.sample(linklist, N_train)

    print('train data: %d' % len(train))


    _beta = numpy.ones(K) / K

    gamma_table = {}

    while True:
        for link in train:
            
            if not link in gamma_table:
                gamma_table[link] = numpy.zeros(K, dtype = float)

            gamma_bunbo = sum([ _beta[k] * n_z[link[0]][k] * n_z[link[1]][k] for k in range(K) ])

            for k in range(K):
                try:
                    gamma_table[link][k] = (_beta[k] * n_z[link[0]][k] * n_z[link[1]][k]) / gamma_bunbo
                except ZeroDivisionError:
                    gamma_bunbo = EPS
                    gamma_table[link][k] = (_beta[k] * n_z[link[0]][k] * n_z[link[1]][k]) / gamma_bunbo

        _new_beta = numpy.zeros(K, dtype = float)
        for k in range(K):
            _new_beta_bunbo = sum([ gamma_table[t].sum() for t in train ])
            _new_beta_bunshi = sum([ gamma_table[t][k] for t in train ])

            try:
                _new_beta[k] = _new_beta_bunshi / _new_beta_bunbo
            except ZeroDivisionError:
                _new_beta_bunbo = EPS
                _new_beta[k] = _new_beta_bunshi / _new_beta_bunbo

        _new_beta /= _new_beta.sum()
        
        q = 0.0
        for link in train:
            q += math.log(sum([ _new_beta[k] * n_z[link[0]][k] * n_z[link[1]][k] for k in range(K) ]) / sum([ _beta[k] * n_z[link[0]][k] * n_z[link[1]][k] for k in range(K) ]))

        for k in range(K): _beta[k] = _new_beta[k]
        
        if q < EM_EPS: break

        
    #sim = similarity.cosine(_beta, beta)
    sim = similarity.kldivergence(beta, _beta)
    print(sim)

    # Laplace smoothing.
    _beta += 0.5
    _beta /= _beta.sum()
    
    #sim_geta = similarity.cosine(_beta, beta)
    sim_geta = similarity.kldivergence(beta, _beta)
    print(sim_geta)

    
    pos_pred = []
    neg_pred = []
    
    for u in range(N):
        for v in range(N):
            if u >= v: continue
            link_prob = sum([ _beta[k] * n_z[u][k] * n_z[v][k] for k in range(K) ])

            if (u, v) in linklist:
                pos_pred.append(link_prob)
            else:
                neg_pred.append(link_prob)

    estimated_threshold = math.fabs(T + ((max(neg_pred) - min(pos_pred))/2.0))
    print(estimated_threshold)


    if not os.path.exists(options.output_path):
        print('File Not Found.')
        exit()

    with file(options.output_path, 'a') as opened:

        data = {}
        data['n'] = N
        data['k'] = k
        data['l'] = LINK_RATE
        data['s'] = options.rseed
        data['ll'] = len(linklist)
        data['tl'] = len(train)
        data['sim'] = sim
        data['simr'] = sim_geta
        data['t'] = T
        data['et'] = math.fabs(T + ((max(neg_pred) - min(pos_pred))/2.0))
        opened.write(json.dumps(data))
        opened.write('\n')


