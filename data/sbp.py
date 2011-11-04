# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import numpy

def sbp_g_0(randomizer, base, gamma = 0.8):

    K = len(base)
    beta = numpy.zeros(K, dtype = numpy.float64)

    for k in range(K):
        
        stick = 1.0
        for l in range(k-1):
            stick *= 1.0 - beta[l]
        beta[k] = randomizer.beta(1, gamma) * stick

    beta /= beta.sum()

    return beta


def sbp_g_j(randomizer, base, alpha = 0.5):

    K = len(base)
    pi = numpy.zeros(K, dtype = numpy.float64)

    for k in range(K):

        stick = 1.0
        for l in range(k-1):
            stick *= 1.0 - pi[l]

        form = alpha * base[k]
        parm = 1.0 - sum([ base[l] for l in range(k) ])
        pi[k] = randomizer.beta( form, parm )

    pi /= pi.sum()

    return pi

if __name__ == '__main__':
    
    H = numpy.random.dirichlet([ 8, 1, 1, 1, 1, 1, 1, 1 ])
    
    beta = sbp_g_0(base = H)

    for j in range(10):
        pi = sbp_g_j(base = beta)
        print(pi)

