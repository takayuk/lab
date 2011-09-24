# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys, os
import numpy
import random
import copy
import math

sys.path.append(os.path.join(os.pardir, 'util'))
import similarity


K = 4
N = 4

y = numpy.zeros((N, N), dtype = int)
w = numpy.zeros((N, N, K), dtype = float)

T = 0.03
TRAIN_RATE = 0.7

SIZE_E = N * (N-1)

numpy.random.seed(4)
random.seed(16)


class Classifier(object):
    def __init__(self):
        self.verbose = False

    def set_training_sample(self, X, Y, w = None):
        self.X = X
        self.Y = Y
        if w:
            self.weights = w
        else:
            self.set_uniform_weights()

    def set_uniform_weights(self):
        N = len(self.Y)
        weights = (1.0 / N) * numpy.ones(N)
        self.weights = weights


def train(T, k = 1):
    X = [ 0.1, 0.2, 0.01, 0.3 ]
    Y = [ -1, 1, -1, 1 ]

    N = 10 * (10 - 1)
    w = (1.0/N)*numpy.ones(N)

    weak_classifier_ensemble = []
    alpha = []

    for t in range(T):
        sys.stdout.write('.')

        weak_learner = Classifier()
        weak_learner.set_training_sample(X, Y)
        weak_learner.weights = w
        weak_leaner.train()



train(T = 1)
exit()

beta = numpy.random.random_sample(size = K)
beta /= beta.sum()


n_z = []
for i in range(N):
    z = numpy.random.random_sample(size = K)
    z /= z.sum()
    
    n_z.append(z)

for i in range(N):
    for j in range(i+1, N):
        if sum([ beta[k] * n_z[i][k] * n_z[j][k] for k in range(K) ]) > T:
            y[i,j] = y[j,i] = 1
        else:
            y[i,j] = y[j,i] = -1

        for k in range(K):
            w[i,j][k] = w[j,i][k] = n_z[i][k] * n_z[j][k]

print(y)


exit()


"""
linklist = []

for i in range(len(n_z)):
    for j in range(i+1, len(n_z)):
        
        link_prob = sum([ beta[k] * n_z[i][k] * n_z[j][k] for k in range(K) ])

        if link_prob > T:
            linklist.append((i, j))

N_train = int(float(len(linklist)) * TRAIN_RATE)
train = random.sample(linklist, N_train)


_beta = numpy.array([ 1.0 / float(K) for k in range(K) ])
#_beta = numpy.random.random_sample(size = K)
_beta /= _beta.sum()

gamma_table = {}

q = 1000000.0
while q > 1.0e-4:
    
    for link in train:
        if not link in gamma_table:
            gamma_table[link] = numpy.zeros(K, dtype = float)

        gamma_bunbo = sum([ _beta[k] * n_z[link[0]][k] * n_z[link[1]][k] for k in range(K) ])

        for k in range(K):
            gamma_table[link][k] = (_beta[k] * n_z[link[0]][k] * n_z[link[1]][k]) / gamma_bunbo


    _new_beta = numpy.zeros(K, dtype = float)
    for k in range(K):
        _new_beta_bunbo = sum([ gamma_table[t].sum() for t in train ])
        _new_beta_bunshi = sum([ gamma_table[t][k] for t in train ])

        _new_beta[k] = _new_beta_bunshi / _new_beta_bunbo

    _new_beta /= _new_beta.sum()
    
    q = 0.0
    for link in train:
        q += math.log(sum([ _new_beta[k] * n_z[link[0]][k] * n_z[link[1]][k] for k in range(K) ]) / sum([ _beta[k] * n_z[link[0]][k] * n_z[link[1]][k] for k in range(K) ]))
    
    for _ in range(K): _beta[_] = _new_beta[_]

    
print('train data: %d' % len(train))

print('true beta')
print(beta)

print('estimated beta')
print(_beta)

#sim1 = similarity.kldivergence(beta, _beta)
#sim2 = similarity.kldivergence(_beta, beta)
sim = similarity.cosine(_beta, beta)
print(sim)
"""


