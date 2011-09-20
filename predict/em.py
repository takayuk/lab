# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import json
import numpy
import math
import copy

train = json.load(open('sample_1_train_1.json'))

f_k_data = [ line.strip().split() for line in open('em_params.lbl').readlines() ]

f_k = {}
for f in f_k_data:
    f_k[(int(f[0]), int(f[1]))] = numpy.array([ float(v) for v in f[2:] ])

K = len(f_k[f_k.keys()[0]])

gamma_table = {}
beta_table = {}

for _u, vlist in train.items():
    u = int(_u)
    
    beta = numpy.random.random(K)
    beta /= beta.sum()
   
    q = 100000000.0
    while q > 1.0e-3:
        
        for v in vlist:

            if not (u, v) in gamma_table:
                gamma_table[(u, v)] = numpy.zeros(K, dtype=numpy.float64)

            gamma_bunbo = 0.0
            gamma_bunshi = 0.0
            for kk in range(K):
                gamma_bunbo += beta[kk] * f_k[(u, v)][kk]

            for k in range(K):
                gamma_table[(u, v)][k] = (beta[k] * f_k[(u, v)][k]) / gamma_bunbo

        new_beta_bunbo = 0.0
        new_beta_bunshi = 0.0

        new_beta = numpy.zeros(K, dtype = numpy.float64)

        for k in range(K):
            for v in vlist:
                new_beta_bunbo += gamma_table[(u, v)].sum()
                new_beta_bunshi += gamma_table[(u, v)][k]
    
            new_beta[k] = new_beta_bunshi / new_beta_bunbo
        new_beta /= new_beta.sum()

        q = 0.0
        for v in vlist:
            for k in range(K):
                q += gamma_table[(u, v)][k] * (math.log(new_beta[k]) - math.log(beta[k]))

        for k in range(K):
            beta[k] = new_beta[k]

        beta_table[u] = copy.deepcopy(list(beta))

    print(u)

#print(beta_table)
with file('beta.json', 'w') as opened:
    opened.write(json.dumps(beta_table))

