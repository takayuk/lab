# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import numpy


K = 4
alpha = 0.5
beta = 0.5

path = 'text'


def flatten(L):
    
    if isinstance(L, list) or isinstance(L, tuple):
        return reduce( lambda a,b: a + flatten(b), L, [] )
    else:
        return [L]


docs = [ zip( *[ [ int(x) for x in w.split(':') ] for w in line.split() ] )
    for line in open(path).read().split('\n') if line ]


V = len(set( flatten([ doc[0] for doc in docs ]) ))
M = len(docs)

z_m_n = []
n_m_z = numpy.zeros((M, K))
n_z_t = numpy.zeros((K, V))

n_z = numpy.zeros(K)

N = sum([ len(doc[0]) for doc in docs ])

for m, doc in enumerate([ d[0] for d in docs ]):
    
    z_n = numpy.random.randint(0, K, len(doc))
    z_m_n.append(z_n)

    for t, z in zip(doc, z_n):
        print(t, z)
        n_m_z[m, z] += 1
        n_z_t[z, t] += 1
        n_z[z] += 1


print(z_m_n)
print(n_z_t)
print(n_z)

