# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys, os
import numpy

numpy.random.seed(int(sys.argv[1]))

beta = numpy.random.random_sample(size = 5)
beta /= beta.sum()

numpy.random.seed(int(sys.argv[2]))


n_z = []

for i in range(10):
    z = numpy.random.random_sample(size = 5)
    z /= z.sum()

    n_z.append(z)

for z in n_z:
    print(z)

K = len(n_z[0])
thresh = 0.04

for i in range(len(n_z)):
    for j in range(i+1, len(n_z)):

        link_prob = 0.0
        for k in range(K):
            link_prob += beta[k] * n_z[i][k] * n_z[j][k]

        if link_prob > thresh:
            print('%d -- %d %f' % (i, j, link_prob))


