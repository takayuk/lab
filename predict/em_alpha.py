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

EPS = 1.0e-6
EM_EPS = 1.0e-3


def map_estimator():
   
    numpy.random.seed(options.rseed)
    random.seed(options.rseed)

    Z = []
    with file('testset2.x1.hdplda') as opened:
        z = [ json.loads(line) for line in opened ]
    Z.append(z)

    with file('testset2.x2.hdplda') as opened:
        z = [ json.loads(line) for line in opened ]
    Z.append(z)

    #K = [ len(n_z[0][0]), len(n_z[1][0]) ]

    w = [ json.load(open('testset2.x1.hdplda.w')), json.load(open('testset2.x2.hdplda.w')) ]

    n_z = {}
    #for i in range(100):
    for i in range(300):
        #for j in range(i+1, 100):
        for j in range(i+1, 300):
            c0 = sum([ Z[0][i][k] * w[0][k] * Z[0][j][k] for k in range(len(Z[0][0])) ])
            c1 = sum([ Z[1][i][k] * w[1][k] * Z[1][j][k] for k in range(len(Z[1][0])) ])
            n_z[(i, j)] = [ c0, c1 ]

    train = [ tuple(link) for link in json.load(open('testset2.edges.train')) ]
    #valid = [ tuple(link) for link in json.load(open(options.valid_path)) ]
    valid = [ tuple(link) for link in json.load(open('testset2.edges.valid')) ]

    _beta = numpy.ones(2) / 2

    gamma_table = {}
    """
    gamma_table[ij] = numpy.zeros(2)
    gamma_table[ij][0] = sum([ w[0][k] * n_z[0][ij[0]][k] * n_z[0][ij[1]][k] for k in range(K[0]) ])
    gamma_table[ij][1] = sum([ w[1][k] * n_z[1][ij[0]][k] * n_z[1][ij[1]][k] for k in range(K[1]) ])

    print(gamma_table)
    """

    K = 2

    while True:
        for link in train:

            if not link in gamma_table:
                gamma_table[link] = numpy.zeros(K, dtype = float)

            #gamma_bunbo = sum([ _beta[k] * n_z[link[0]][k] * n_z[link[1]][k] for k in range(K) ])
            gamma_bunbo = sum([ _beta[k] * n_z[link][k] for k in range(K) ])

            for k in range(K):
                try:
                    #gamma_table[link][k] = (_beta[k] * n_z[link[0]][k] * n_z[link[1]][k]) / gamma_bunbo
                    #gamma_table[ij][k] = (_beta[k] * n_z[link[0]][k] * n_z[link[1]][k]) / gamma_bunbo
                    gamma_table[link][k] = (_beta[k] * n_z[link][k]) / gamma_bunbo
                except ZeroDivisionError:
                    gamma_bunbo = EPS
                    #gamma_table[link][k] = (_beta[k] * n_z[link[0]][k] * n_z[link[1]][k]) / gamma_bunbo
                    gamma_table[link][k] = (_beta[k] * n_z[link][k]) / gamma_bunbo

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
            #q += math.log(sum([ _new_beta[k] * n_z[link[0]][k] * n_z[link[1]][k] for k in range(K) ]) / sum([ _beta[k] * n_z[link[0]][k] * n_z[link[1]][k] for k in range(K) ]))
            q += math.log(sum([ _new_beta[k] * n_z[link][k] for k in range(K) ]) / sum([ _beta[k] * n_z[link][k] for k in range(K) ]))

        for k in range(K): _beta[k] = _new_beta[k]
        
        if q < EM_EPS: break
        print(q)

    #print('done...')


    result = {}
    
    for link in train:
        #print(link, (_beta[0] * n_z[link][0]) + (_beta[1] * n_z[link][1]) )

        if not link[0] in result: result[link[0]] = {}
        result[link[0]][link[1]] = (_beta[0] * n_z[link][0]) + (_beta[1] * n_z[link][1])

    #print('---')
    for link in valid:
        #print(link, (_beta[0] * n_z[link][0]) + (_beta[1] * n_z[link][1]) )
    
        if not link[0] in result: result[link[0]] = {}
        result[link[0]][link[1]] = (_beta[0] * n_z[link][0]) + (_beta[1] * n_z[link][1])
    
    
    #print('---')
    linkall = []
    for i in range(100):
        #for j in range(i+1, 100):
        for j in range(100):
            if i != j:
                linkall.append((i, j))

    nolinks = set(linkall) - set(train) - set(valid)

    for n in nolinks:
        c0 = sum([ Z[0][n[0]][k] * Z[0][n[1]][k] * w[0][k] for k in range(len(Z[0][0])) ])
        c1 = sum([ Z[1][n[0]][k] * Z[1][n[1]][k] * w[1][k] for k in range(len(Z[1][0])) ])

        r_n = (_beta[0] * c0) + (_beta[1] * c1)
        #print(n, r_n)

        if not n[0] in result: result[n[0]] = {}
        result[n[0]][n[1]] = r_n


    trueset = json.load(open('testset2.edges'))
    graph = {}
    for l in trueset:
        if l[0] not in graph: graph[l[0]] = []
        graph[l[0]].append(l[1])

    for TopK in range(10, 100, 5):
       
        precision = 0
        for u in range(100):

            if u not in graph:
                continue

            rank = sorted(result[u].items(), key = lambda x:x[1], reverse = True)[:TopK]
            #rank = sorted(result[u].items(), key = lambda x:x[1], reverse = True)[:len(graph[u])]

            for v in rank:
                if u > v[0]: continue
                if tuple([u, v[0]]) in set(valid):
                    precision += 1
                """
                if v in graph[u]:
                    print('OK')
                """

        print('%d / %d' % (precision, len(trueset)))
        
    precision = 0

    avg = 0.0
    for u in range(300):

        local_prec = 0
        if u not in graph:
            continue

        TopK = len(graph[u])
        rank = sorted(result[u].items(), key = lambda x:x[1], reverse = True)[:TopK]
        #rank = sorted(result[u].items(), key = lambda x:x[1], reverse = True)[:len(graph[u])]

        for v in rank:
            if u > v[0]: continue
            if tuple([u, v[0]]) in set(valid):
                precision += 1
                local_prec += 1
            """
            if v in graph[u]:
                print('OK')
            """

        avg += float(local_prec) / TopK
        print('%d / %d' % (local_prec, TopK))
    print('%d / %d' % (precision, len(trueset)))

    print(avg/300.0)
    exit()
   













    #sim = similarity.cosine(_beta, beta)
    #sim = similarity.kldivergence(beta, _beta)
    #print(sim)

    # Laplace smoothing.
    #_beta += 0.5
    _beta += 0.05
    _beta /= _beta.sum()

    print(_beta)

    #for link in train:
    for link in valid:
        print(link)
        r = sum([ n_z[link[0]][k] * _beta[k] * n_z[link[1]][k] for k in range(K) ])
        print(link, r)

    linkall = []
    for i in range(100):
        #for j in range(i+1, 100):
        for j in range(100):
            if i != j:
                linkall.append((i, j))
    linkall = set(linkall)
    linkall = linkall - set(train) - set(valid)

    for ex in linkall:
        r = sum([ n_z[ex[0]][k] * _beta[k] * n_z[ex[1]][k] for k in range(K) ])
        print(json.dumps({list(ex): r}))
    #print(beta)
    #sim_geta = similarity.cosine(_beta, beta)
    #sim_geta = similarity.kldivergence(beta, _beta)
    #print(sim_geta)


def args():

    script_usage = 'Usage: %s [options] \
            -o <output> --feat <feature> --train <traing data> --valid <validation data> --rseed <random seed>' % sys.argv[0]

    parser = optparse.OptionParser(usage = script_usage)
    parser.add_option('--feat', dest = 'feature_path')
    parser.add_option('--train', dest = 'train_path')
    parser.add_option('--valid', dest = 'valid_path')
    parser.add_option('-o', dest = 'output_path')
    parser.add_option('--rseed', dest = 'rseed', type = 'int', default = 1)
    
    (opts, args) = parser.parse_args()

    """
    if not (opts.input_path and opts.output_path):
        parser.error(script_usage)
    """
    
    return (opts, args)


if __name__ == '__main__':

    (options, args) = args()

    map_estimator()
