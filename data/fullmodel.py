# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import numpy
import networkx
from matplotlib import pylab

import json
import sys, os


def plot(out_filepath, graph):

    fig = pylab.figure(1)

    pylab.subplot(211)
    networkx.draw_spring(graph, node_size = 8, with_labels = False)

    deg = {}
    for d in [ len(graph.edges(n)) for n in graph.nodes() ]:
        try:
            deg[d] += 1
        except KeyError:
            deg[d] = 1

    print(deg)
    
    pylab.subplot(212)
    plot = deg.items()

    pylab.loglog([ x[0] for x in plot ], [ x[1] for x in plot ], '.')

    pylab.savefig(out_filepath + '.png')


def fullmodel(alpha = 0.5, beta = 0.5, gamma = 0.5, base = 0.05, K = 8, V = 50, M = 10, N = 30, rseed = 16, out_filepath = 'out'):

    numpy.random.seed(rseed)

    G_j = [ numpy.random.dirichlet( numpy.ones(K) * alpha ) for j in range(M) ]
    W = [ numpy.random.dirichlet( numpy.ones(K) / K ) for k in range(K) ]

    phi = [ numpy.random.dirichlet( numpy.ones(V) * beta ) for k in range(K) ]
    theta = [ numpy.random.multinomial(N, G_j[u]) for u in range(M) ]

    graph = networkx.Graph()

    theta_prob = [ numpy.array([ float(x) for x in theta[u] ]) / theta[u].sum() for u in range(M) ]

    docs = []
    for u in range(M):
        doc = []
        for n in range(N):
            z = numpy.random.multinomial(1, theta_prob[u]).argmax()
            x = numpy.random.multinomial(1, phi[z]).argmax()
            doc.append(str(x))

        docs.append(doc)


    for u in range(M):
        for v in range(M):
            if u == v:
                continue

            r_uv = sum([ theta_prob[u][k] * theta_prob[v][k] * W[k][k] for k in range(K) ])

            if numpy.random.binomial(1, r_uv) > 0:
                graph.add_edge(u, v)


    print(len(graph.edges()), (M * (M-1))/2)
    with file(out_filepath + '.edges', 'w') as opened:
        opened.write( json.dumps(graph.edges()) )

    with file(out_filepath + '.docs', 'w') as opened:
        opened.write( json.dumps(docs) )

    plot(out_filepath, graph)


if __name__ == '__main__':

    try:
        fullmodel(alpha = 3.2, gamma = 3.2, K = 5, M = 300, rseed = int(sys.argv[1]))
    except IndexError:
        fullmodel(alpha = 3.2, gamma = 3.2, K = 5, M = 300)


