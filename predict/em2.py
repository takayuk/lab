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

    with file(options.feature_path) as opened:
        n_z = [ json.loads(line) for line in opened ]

    K = len(n_z[0])

    train = [ tuple(link) for link in json.load(open(options.train_path)) ]
    valid = [ tuple(link) for link in json.load(open(options.valid_path)) ]

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
        print(q)

    print('done...')
    
    #sim = similarity.cosine(_beta, beta)
    #sim = similarity.kldivergence(beta, _beta)
    #print(sim)

    # Laplace smoothing.
    _beta += 0.5
    #_beta += 0.1
    _beta /= _beta.sum()

    with file(options.feature_path + '.w', 'w') as opened:
        opened.write(json.dumps(list(_beta)))

    print(_beta)
    exit()

    #for link in train:
    for link in valid:
        print(link)
        r = sum([ n_z[link[0]][k] * _beta[k] * n_z[link[1]][k] for k in range(K) ])
        print(link, r)

    linkall = []
    for i in range(100):
        for j in range(i+1, 100):
            linkall.append((i, j))
    linkall = set(linkall)
    linkall = linkall - set(train) - set(valid)

    for ex in linkall:
        r = sum([ n_z[ex[0]][k] * _beta[k] * n_z[ex[1]][k] for k in range(K) ])
        print(ex, r)
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
