# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import json
import numpy


#valid=json.load(open('sample_1_valid_1.json'))
train = json.load(open('sample_1_train_1.json'))

"""
urlid=[line.strip().split()[2] for line in open('flickr_original.urlid').readlines()]
id2name=dict(zip(range(1,len(urlid)+1),urlid))
"""

lbl=[line.strip().split() for line in open('flickr_original.lbl').readlines()]
for i in range(len(lbl)):
    lbl[i]=[int(v) for v in lbl[i]]

"""
g_urlid = [line.strip().split()[2] for line in open('flickr-com.urlid').readlines()]
name2id=dict(zip(g_urlid, range(1, len(g_urlid)+1)))
"""
"""
worddist = {}
wd_lbl = [line.strip().split() for line in open('worddist_i-20.lbl').readlines()]
for l in wd_lbl:
    worddist[int(l[0])] = [float(z) for z in l[1:]]
    K = len(worddist[int(l[0])])
"""
#result = []

docdist = json.load(open('docdist_i-20_train.json'))
K = len(docdist[docdist.keys()[0]])

params = {}
with file('em_params.lbl', 'w') as opened:
    
    for u, vlist in train.items():

        for v in vlist:
            param = numpy.zeros(K+1, dtype=numpy.float64)

            try:
                #bunbo = len( set(lbl[int(u)]) | set(lbl[v]) )
                bunbo = len( set(lbl[int(u)-1]) | set(lbl[v-1]) )
            except IndexError:
                print(u, v)

            if bunbo == 0:
                param[0] = 0.0
            else:
                param[0] = float(len( set(lbl[int(u)-1]) & set(lbl[v-1]) )) / float(bunbo)
            
            for k in range(1, K+1):
                #param[k] = docdist[u][k-1] * docdist[str(v)][k-1]
                param[k] = 1.0 - (docdist[u][k-1] * docdist[str(v)][k-1])

            opened.write('%s %s %s\n' % (u, v, ' '.join([ str(p) for p in param ])))
        print(u)
