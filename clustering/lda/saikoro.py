# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

from numpy import random
import json
import sys

import site
site.addsitedir('/home/takayuk/workspace/lab/util')

import similarity

import networkx


# Constants.
(M, N) = (300, 50)
(K, V) = (20, 200)

T = 0.5

random.seed(32)

#(alpha, beta) = (0.5, 0.5)


# Probabilities for each user.
docs = []

alpha = [ random.gamma(1, 1) for m in range(M) ]
doc_theta = [ random.dirichlet([ alpha[m] ] * K) for m in range(M) ]

#beta = random.gamma(1, 1)
beta = random.beta(1, 1)
#corpus_phi = [ random.dirichlet([ beta ] * K) for k in range(K) ]
corpus_phi = [ random.dirichlet([ beta ] * V) for k in range(K) ]


# Network.
graph = networkx.Graph()

for i in range(M):
    for j in range(M):
        if i == j:
            continue

        s_ij = similarity.similarity(doc_theta[i], doc_theta[j], 'kld')
        s_ji = similarity.similarity(doc_theta[j], doc_theta[i], 'kld')

        if s_ij < T and s_ji < T:
            graph.add_edge(i, j)

E_size_comp = (M * (M-1)) / 2
E_size_graph = len(graph.edges())

print('%d / %d - %f' % (E_size_graph, E_size_comp, float(E_size_graph) / E_size_comp))

with file(sys.argv[1] + '.edges', 'w') as opened:
    opened.write(json.dumps(graph.edges()))


docs = []

for m in range(M):

    z = random.multinomial(1, doc_theta[m]).argmax()
    x_list = [ random.multinomial(1, corpus_phi[z]).argmax() for n in range(N) ]

    doc = {}
    for i in range(N):
        try:
            doc[str(x_list[i])] += 1
        except KeyError:
            doc[str(x_list[i])] = 1

    docs.append(doc)


print(docs)

#with file(sys.argv[1], 'w') as opened:
with file(sys.argv[1] + '.x1', 'w') as opened:

    for doc in docs:
        #opened.write('%s\n' % doc)
        #buf = ' '.join([ '%d:%d' % (term, freq) for term, freq in doc.items() ])

        buf = []
        for term, freq in doc.items():
            buf += [ str(term) ] * freq
        opened.write('%s\n' % ' '.join(buf))



###################################################################

N = 30
(K, V) = (15, 150)

alpha = [ random.gamma(1, 1) for m in range(M) ]
doc_theta = [ random.dirichlet([ alpha[m] ] * K) for m in range(M) ]

#beta = random.gamma(1, 1)
beta = random.beta(1, 1)
corpus_phi = [ random.dirichlet([ beta ] * V) for k in range(K) ]

docs = []

for m in range(M):

    z = random.multinomial(1, doc_theta[m]).argmax()
    x_list = [ random.multinomial(1, corpus_phi[z]).argmax() for n in range(N) ]

    doc = {}
    for i in range(N):
        try:
            doc[str(x_list[i])] += 1
        except KeyError:
            doc[str(x_list[i])] = 1

    docs.append(doc)


with file(sys.argv[1] + '.x2', 'w') as opened:

    for doc in docs:
        #opened.write('%s\n' % doc)
        #buf = ' '.join([ '%d:%d' % (term, freq) for term, freq in doc.items() ])

        buf = []
        for term, freq in doc.items():
            buf += [ str(term) ] * freq
        opened.write('%s\n' % ' '.join(buf))













exit()

"""
from matplotlib import pylab
fig = pylab.figure()
networkx.draw_spring(graph)
fig.savefig('graph.png')
"""

exit()

#opened = file(sys.argv[1], 'w')
#opened.write('%s\n' % doc_str)
#opened.close()


info = {}
info['K'] = K
info['V'] = V
info['alpha'] = alpha
info['theta'] = beta
info['rseed'] = 32

with file('.log', 'a') as opened:
    opened.write('%s\n' % json.dumps(info))

