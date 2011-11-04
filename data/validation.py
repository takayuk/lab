# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import numpy
import json
import sys, os
import networkx


W = json.load(open(sys.argv[1]))

F = []
with file(sys.argv[2]) as opened:
    for line in opened:
        F.append(json.loads(line))

K = len(W)
TOP_K = 30

graph = networkx.Graph()
graph.add_edges_from(json.load(open('out.edges.true')))

N = tuple(graph.nodes())


r = {}
for u in N:
    for v in N:
        if u >= v:
            continue
        r[(u, v)] = sum([ F[u][k] * F[v][k] * W[k] for k in range(K) ])

print(len(r))
rank = sorted(r.items(), key = lambda x:x[1], reverse = True)

topk_rank = rank[:TOP_K]
print(topk_rank)
for top in topk_rank:
    if top[0] in graph.edges():
        print(top[0])

