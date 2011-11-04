# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import numpy
import networkx
import sys, os

import site
site.addsitedir('../clustering/lda')
site.addsitedir('../predict')

from hdplda import HDPLDA
import em2
import train
import sbp

#(K, V) = (8, 10)
(K, V) = (8, 16)
(N, M) = (20, 100)

TRIAL = 10

if len(sys.argv) < 2:
    numpy.random.seed(1)
else:
    numpy.random.seed(int(sys.argv[1]))


H = numpy.random.dirichlet([5] + [1] * (K-1))

W2 = numpy.ones((K, K), dtype = numpy.float64)
W2[0][0] *= 4.0
#W2[1][1] *= 1.0
#W2[0][1] *= 4.0
#W2[1][0] *= 4.0
#W2[1][2] *= 3.0
W2 /= W2.sum()
#print(W2)

G_0 = sbp.sbp_g_0(numpy.random, base = H, gamma = 0.5)
#print(G_0)
#Z = [ sbp.sbp_g_j(numpy.random, base = G_0, alpha = 0.8) for i in range(M) ]
#Z = [ sbp.sbp_g_j(numpy.random, base = G_0, alpha = 0.1) for i in range(M) ]
G = [ sbp.sbp_g_j(numpy.random, base = G_0, alpha = 0.1) for i in range(M) ]
#for g in Z: print(g)

    
graph = networkx.Graph()


theta = []
theta_p = []
for u in range(M):
    #theta.append( numpy.array([ float(x) for x in numpy.random.multinomial(K, Z[u]) ]) )
    theta.append( numpy.array([ float(x) for x in numpy.random.multinomial(N, G[u]) ]) )
    theta_p.append( theta[-1] / theta[-1].sum() )

    theta_p[-1] += 0.08
    theta_p[-1] /= theta_p[-1].sum()
    #print(theta_p[-1])


for u in range(M):
    for v in range(M):
        if u >= v: continue

        r_uv = 0
        for k in range(K):
            for l in range(K):
                r_uv += theta_p[u][k] * theta_p[v][l] * W2[k][l]

        if r_uv > 0.01:
            make_link = 0
            for trial in range(TRIAL):
                if numpy.random.binomial(1, r_uv) > 0:
                    make_link += 1
            if make_link > 1:
                graph.add_edge(u, v)
                #print('\t' + str((u, v, r_uv)))
            else:
                #print(u, v, r_uv)
                pass

print(len(graph.edges()), ((M * (M-1))/2))

U = graph.nodes()

train, valid = train.train_and_valid(graph.edges(), 0.7, 1)

KVtable = {
        0: [0,1],
        1: [2,3],
        2: [4,5],
        3: [6,7],
        4: [8,9],
        5: [10,11],
        6: [12,13],
        7: [14,15]}

beta = [
        [8, 8, 2, 1, 3, 1, 2, 2, 1, 2],
        [2, 1, 8, 8, 1, 1, 2, 4, 1, 1],
        [1, 1, 4, 1, 8, 8, 2, 1, 2, 1],
        [1, 1, 4, 1, 3, 2, 2, 1, 8, 9],
        [1, 1, 4, 1, 3, 2, 8, 8, 1, 4],
        [1, 1, 8, 1, 3, 2, 2, 1, 8, 2],
        [1, 1, 4, 1, 8, 8, 2, 1, 1, 2],
        [1, 1, 4, 1, 3, 2, 2, 1, 8, 9]]
phi = [ numpy.random.dirichlet(beta[k]) for k in range(K) ]

docs = []
for u in range(M):
    doc = []
    for n in range(N):
        z = numpy.random.binomial(1, theta_p[u]).argmax()
        kouho = KVtable[z]
        x = kouho[ numpy.random.randint(len(kouho)) ]
        doc.append(x)

    docs.append(doc)


lda = HDPLDA(K = 4, gamma = 0.5, alpha = 0.1, base = 0.05, docs = docs, V = V)
for i in range(50):
    lda.inference()
    #print(lda.perplexity())

G_ = lda.topic_prob()
K_ = len(G_[0])

#for g_ in G_: print(g_)

#worddist = lda.worddist()
#K_ = len(worddist)

Z_ = []
for u in range(M):
    #z_ = numpy.array([ float(x) for x in numpy.random.multinomial(K_, G_[u]) ])
    z_ = numpy.array([ float(x) for x in numpy.random.multinomial(N, G_[u]) ])
    z_ += 1.0
    z_ /= z_.sum()
    Z_.append(z_)

#for _ in Z_: print(_)


#W_ = em2.map_estimator2(Z_, train)
W_ = em2.map_estimator3(Z_, train)

#print(W_)
W_ += 0.01
W_ /= W_.sum()
#print(W_)


pairs = []
for u in U:
    for v in U:
        if u == v: continue
        pairs.append( tuple(sorted([u, v])) )
pairs = list(set(pairs))


for pair in pairs:

    u, v = pair
    #r = sum([ Z_[u][k] * Z_[v][k] * W_[k] for k in range(K_) ])
    r = 0
    for k in range(K_):
        for l in range(K_):
            r += Z_[u][k] * Z_[v][l] * W_[k][l]

    if pair in graph.edges():
        print('\t' + str((u, v, r)))
        pass
    else:
        print(u, v, r)
        pass

exit()


for u, vlist in links.items():

    for v in vlist:

        #r = sum([ Z_[u][k] * Z_[v][k] for k in range(K_) ])
        r = sum([ Z_[u][k] * Z_[v][k] * W_[k] for k in range(K_) ])
        print(u, v, r)

    print('')

    for v in U:
        if u == v:
            continue
        #r = sum([ Z_[u][k] * Z_[v][k] for k in range(K_) ])
        r = sum([ Z_[u][k] * Z_[v][k] * W_[k] for k in range(K_) ])
        print(u, v, r)

    print('---')


