# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys

import networkx
from matplotlib import pylab

N = int(sys.argv[1])
K = int(sys.argv[2])
graph = networkx.watts_strogatz_graph(n = N, k = K, p = 0.8, seed = 32)

networkx.draw_spring(graph)

degrees = graph.degree( graph.nodes() ).values()

distrib = {}

for k in degrees:
    try:
        distrib[k] += 1
    except KeyError:
        distrib[k] = 1

for k in distrib:
    distrib[k] = float(distrib[k]) / len(graph.nodes())

plot = distrib.items()


fig = pylab.figure()

pylab.loglog( [ x[0] for x in plot ], [ x[1] for x in plot ], ',' )
fig.savefig('deg.png')
