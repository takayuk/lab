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


(K, V) = (4, 10)
(N, M) = (20, 32)


peaks = [ [1, 1, 1, 7], [7, 1, 1, 1], [4, 1, 4, 1] ]


"""
def poi(s):

    a = numpy.zeros(K)
    for i in range(K-1):
        a[i] = numpy.random.poisson(2)
    a[-1] = numpy.random.poisson(s)

    return a + 1.0
"""

if len(sys.argv) < 2:
    rseed = 3
    numpy.random.seed(rseed)
else:
    numpy.random.seed(int(sys.argv[1]))


#prob = [ 10, 9, 7, 5, 4, 6, 8, 9 ]

Z = []
for i in range(M):
    #Z.append( numpy.random.dirichlet(poi(prob[i])) )
    peak = peaks[ numpy.random.randint(3) ]
    Z.append( numpy.random.dirichlet( peak ) )

# W <- dir( peaks[0] + peaks[1] + peaks[2] )
W = numpy.random.dirichlet([ 12, 3, 6, 9 ])

graph = networkx.Graph()


theta = []
theta_p = []
for u in range(M):
    theta.append( numpy.array([ float(x) for x in numpy.random.multinomial(K, Z[u]) ]) )
    theta_p.append( theta[-1] / theta[-1].sum() )
     

for u in range(len(Z)):
    for v in range(len(Z)):
        if u >= v: continue
       
        r_uv = sum([ theta_p[u][k] * theta_p[v][k] * W[k] for k in range(K) ])

        if numpy.random.binomial(1, r_uv) > 0:
            graph.add_edge(u, v)
            #print(u, v, r_uv)
        else:
            #print('Rejected', u, v, r_uv)
            pass
print(len(graph.edges()), ((M * (M-1))/2))

train, valid = train.train_and_valid(graph.edges(), 0.7, 1)


# (V, K)のphiをつくる
#phi = [ numpy.random.dirichlet([ 1, 8, 1, 8, 2, 2, 3, 3, 8, 8 ]) for k in range(K) ]

beta = [
        [8, 8, 2, 1, 3, 1, 2, 2, 1, 2],
        [2, 1, 8, 8, 1, 1, 2, 4, 1, 1],
        [1, 1, 4, 1, 8, 8, 2, 1, 2, 1],
        [1, 1, 4, 1, 3, 2, 2, 1, 8, 9]]

phi = [ numpy.random.dirichlet(beta[k]) for k in range(K) ]


docs = []
for u in range(M):
    doc = []
    for n in range(N):
        z = numpy.random.multinomial(1, Z[u]).argmax()
        x = numpy.random.multinomial(1, phi[z]).argmax()
        doc.append(x)

    docs.append(doc)

lda = HDPLDA(4, 0.5, 2.0, 0.05, docs, V)
for i in range(50):
    lda.inference()
    #print(lda.perplexity())

G_ = lda.topic_prob()

Z_ = []
for u in range(M):
    z_ = numpy.array([ float(x) for x in numpy.random.multinomial(len(G_[0]), G_[u]) ])

    z_ += 0.1
    z_ /= z_.sum()
    Z_.append(z_)

W_ = em2.map_estimator2(Z_, train, valid)

K_ = len(W_)

N = graph.nodes()
r = {}
for u in N:
    for v in N:
        if u >= v:
            continue

        r[(u, v)] = sum([ Z_[u][k] * Z_[v][k] * W_[k] for k in range(K_) ])

rank = sorted(r.items(), key = lambda x:x[1], reverse = True)
topk_rank = rank[:20]
print(topk_rank)

for link in valid:
    u = link[0]

    for v in N:
        if u == v: continue

        
    break





