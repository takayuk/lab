# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys, os
import numpy
import random
import copy
import math

sys.path.append(os.path.join(os.pardir, 'util'))
import similarity

import networkx
import matplotlib.pylab as plt

import optparse

#from svm import *
#from svmutil import *

import json


def args():

    script_usage = 'Usage: %s [options] \
            -n <num of nodes> -k <dim of topic-vec> --rseed <random seed> -o <output>' % sys.argv[0]

    parser = optparse.OptionParser(usage = script_usage)
    parser.add_option('-n', dest = 'N', type = 'int', default = 100)
    parser.add_option('-k', dest = 'K', type = 'int', default = 10)
    parser.add_option('-l', dest = 'LINK_RATE', type = 'float', default = 0.08)
    parser.add_option('--rseed', dest = 'rseed', type = 'int', default = 1)
    parser.add_option('-o', dest = 'output_path')

    (opts, args) = parser.parse_args()

    if not opts.output_path:
        parser.error(script_usage)

    return (opts, args)


if __name__ == '__main__':
   
    (options, args) = args()
   
    #N = options.N
    #K = options.K
    
    EPS = 1.0e-6
    EM_EPS = 1.0e-3
    
    #LINK_RATE = options.LINK_RATE
    TRAIN_RATE = 0.7
 
    numpy.random.seed(options.rseed)
    random.seed(options.rseed)

    #beta = numpy.random.random_sample(size = K)
    #beta /= beta.sum()

    #T = 0.00001
   
    n_z = []
    n_z = [ l.strip().split() for l in open('pools.docdist').readlines() ]
    N = len(n_z)
    K = len(n_z[0])
    
    for i in range(len(n_z)):
        n_z[i] = [ float(v) for v in n_z[i] ]
        if n_z[i][0] != n_z[i][0]:
            n_z[i] = [0] * K

    """
    for i in range(N):
        z = numpy.random.random_sample(size = K)
        z /= z.sum()
        n_z.append(z)
    """

    lbl = [ l.strip().split() for l in open('/home/takayuk/dataset/expdata/dataset/set1/set1_0926_bi.lbl').readlines() ]
    for i in range(len(lbl)):
        lbl[i] = [ int(v) for v in lbl[i] ]

    u_id = 18631
    v_ids = set(lbl[u_id-1])

    linklist = networkx.Graph()
    
    #nodes = set([ u_id ]) | v_ids
    nodes = v_ids
    for n in nodes:
        for m in set(lbl[n-1]) & nodes:
            linklist.add_edge(n, m)

    ids = [ l.strip().split()[2] for l in open('/home/takayuk/dataset/expdata/dataset/set1/set1_0926_bi.urlid').readlines() ]
    i2n = dict(zip(range(1, len(ids)+1), ids))

    ids_p = [ l.strip().split()[2] for l in open('set1_bi_1.urlid').readlines() ]
    n2i_p = dict(zip(ids_p, range(1, len(ids)+1)))

    # Added.
    #n2i_p[ i2n[18631] ] = len(n2i_p)+1

    print(len(nodes))

    N_train = int(float(len(nodes)) * TRAIN_RATE)
    #N_train = int(float(len(linklist.edges())) * TRAIN_RATE)
    #train = random.sample(linklist.edges(), N_train)
    train = random.sample(list(nodes), N_train)
    print(train)

    valid = nodes - set(train)
    print(valid)
    print('train data: %d' % len(train))


    # linklistをtrain_linklistとvalid_linklistに分ける.
    train_linklist = networkx.Graph()
    valid_linklist = networkx.Graph()
    for link in linklist.edges():
        print(link)
        if (link[0] in train) and (link[1] in train):
            train_linklist.add_edge(link[0], link[1])
        else:
            valid_linklist.add_edge(link[0], link[1])

    print(len(train_linklist.edges()))
    print(len(valid_linklist.edges()))
    exit()

    _beta = numpy.ones(K) / K

    gamma_table = {}

    while True:
        #for link in train:
        for link in train_linklist.edges():
            
            if not link in gamma_table:
                gamma_table[link] = numpy.zeros(K, dtype = float)

            l0 = n2i_p[ i2n[link[0]] ] - 1
            l1 = n2i_p[ i2n[link[1]] ] - 1

            gamma_bunbo = sum([ _beta[k] * n_z[l0][k] * n_z[l1][k] for k in range(K) ])

            for k in range(K):
                if gamma_bunbo > EPS:
                    gamma_table[link][k] = (_beta[k] * n_z[l0][k] * n_z[l1][k]) / gamma_bunbo
                else:
                    gamma_bunbo = EPS
                    gamma_table[link][k] = (_beta[k] * n_z[l0][k] * n_z[l1][k]) / gamma_bunbo


        _new_beta = numpy.zeros(K, dtype = float)
        for k in range(K):
            #_new_beta_bunbo = sum([ gamma_table[t].sum() for t in train ])
            _new_beta_bunbo = sum([ gamma_table[t].sum() for t in train_linklist.edges() ])
            #_new_beta_bunshi = sum([ gamma_table[t][k] for t in train ])
            _new_beta_bunshi = sum([ gamma_table[t][k] for t in train_linklist.edges() ])

            try:
                _new_beta[k] = _new_beta_bunshi / _new_beta_bunbo
            except ZeroDivisionError:
                _new_beta_bunbo = EPS
                _new_beta[k] = _new_beta_bunshi / _new_beta_bunbo

        _new_beta /= _new_beta.sum()
        
        q = 0.0
        #for link in train:
        for link in train_linklist.edges():
            l0 = n2i_p[ i2n[link[0]] ] - 1
            l1 = n2i_p[ i2n[link[1]] ] - 1

            #q += math.log(sum([ _new_beta[k] * n_z[link[0]][k] * n_z[link[1]][k] for k in range(K) ]) / sum([ _beta[k] * n_z[link[0]][k] * n_z[link[1]][k] for k in range(K) ]))
            bb = sum([ _beta[k] * n_z[l0][k] * n_z[l1][k] for k in range(K) ])
            #q += math.log(sum([ _new_beta[k] * n_z[l0][k] * n_z[l1][k] for k in range(K) ]) / sum([ _beta[k] * n_z[l0][k] * n_z[l1][k] for k in range(K) ]))
            bc = sum([ _new_beta[k] * n_z[l0][k] * n_z[l1][k] for k in range(K) ])

            if bb > EPS:
                q += math.log(sum([ _new_beta[k] * n_z[l0][k] * n_z[l1][k] for k in range(K) ]) / bb)
            else:
                bb = EPS
                try:
                    q += math.log(sum([ _new_beta[k] * n_z[l0][k] * n_z[l1][k] for k in range(K) ]) / bb)
                except ValueError:
                    q += math.log(1.0)

        print(q)
        for k in range(K): _beta[k] = _new_beta[k]
        
        if q < EM_EPS: break

    
    #sim = similarity.cosine(_beta, beta)
    #sim = similarity.kldivergence(beta, _beta)
    #print(sim)

    # Laplace smoothing.
    _beta += 0.5
    _beta /= _beta.sum()
    
    #sim_geta = similarity.cosine(_beta, beta)
    #sim_geta = similarity.kldivergence(beta, _beta)
    #print(sim_geta)

    print(_beta)
    
    pos_pred = []
    neg_pred = []

    for u in range(len(train)):
        for v in range(len(train)):
            if u >= v: continue
            
            _u = n2i_p[ i2n[train[u]] ] - 1
            _v = n2i_p[ i2n[train[v]] ] - 1

            link_prob = sum([ _beta[k] * n_z[_u][k] * n_z[_v][k] for k in range(K) ])

            #if (_u, _v) in train_linklist.edges() or (_v, _u) in train_linklist.edges():
            if (train[u], train[v]) in train_linklist.edges() or (train[v], train[u]) in train_linklist.edges():
                pos_pred.append(link_prob)
            else:
                neg_pred.append(link_prob)

    print(len(pos_pred))
    print(len(neg_pred))
    print(pos_pred[:10])
    print(neg_pred[:10])
    """
    for u in range(N):
        for v in range(N):
            if u >= v: continue
            link_prob = sum([ _beta[k] * n_z[u][k] * n_z[v][k] for k in range(K) ])

            if (u, v) in linklist:
                pos_pred.append(link_prob)
            else:
                neg_pred.append(link_prob)
    """
    #estimated_threshold = math.fabs(T + ((max(neg_pred) - min(pos_pred))/2.0))
    estimated_threshold = math.fabs(((max(neg_pred) - min(pos_pred))/2.0))
    print(estimated_threshold)
    
    valid = list(valid)
    #for u in range(len(valid)):
    #HOSEI = -0.003
    result = []
    for HOSEI in numpy.arange(-0.005, 0.005, 0.0001):
        
        (good_precision, bad_precision) = (0, 0)
        (good_recall, bad_recall) = (0, 0)
        (A,B,C,D) = (0,0,0,0)
 
        for u in range(len(valid)):
            #for v in range(len(valid)):
            for v in range(len(valid)):
                if u >= v: continue
                #print(valid[u], valid[v])
                
                _u = n2i_p[ i2n[valid[u]] ] - 1
                _v = n2i_p[ i2n[valid[v]] ] - 1

                link_prob = sum([ _beta[k] * n_z[_u][k] * n_z[_v][k] for k in range(K) ])

                #if link_prob >= estimated_threshold:
                if link_prob >= estimated_threshold + HOSEI:
                    A+=1
                    if (valid[u], valid[v]) in valid_linklist.edges() or (valid[v], valid[u]) in valid_linklist.edges():
                        C+=1
                else:
                    B+=1
                    if (valid[u], valid[v]) in valid_linklist.edges() or (valid[v], valid[u]) in valid_linklist.edges():
                        #bad_recall += 1
                        pass
                    else:
                        #good_recall += 1
                        pass

        #print(estimated_threshold + HOSEI, good_precision, bad_precision, good_recall, bad_recall)
        #print(estimated_threshold + HOSEI, float(C) / float(A), float(C)/float(B))
        try:
            print('%e,%e,%e' % (estimated_threshold + HOSEI, float(C) / float(A), float(C)/float(B)))
            result.append((estimated_threshold + HOSEI, float(C) / float(A), float(C)/float(B)))
        except:
            pass

    import matplotlib.pylab as plt
    #plt.loglog([r[0] for r in result],[r[1] for r in result])
    plt.plot([r[0] for r in result],[r[1] for r in result])
    #plt.loglog([r[0] for r in result],[r[2] for r in result])
    plt.plot([r[0] for r in result],[r[2] for r in result])
    plt.plot([estimated_threshold, estimated_threshold], [0, 1.0])
    plt.savefig('RES.png')
    #print(good_precision, bad_precision)
    #print(good_recall, bad_recall)
    #print(valid_linklist.edges())
    exit()

    if not os.path.exists(options.output_path):
        print('File Not Found.')
        exit()

    with file(options.output_path, 'a') as opened:

        data = {}
        data['n'] = N
        data['k'] = k
        data['l'] = LINK_RATE
        data['s'] = options.rseed
        data['ll'] = len(linklist)
        data['tl'] = len(train)
        data['sim'] = sim
        data['simr'] = sim_geta
        data['t'] = T
        data['et'] = math.fabs(T + ((max(neg_pred) - min(pos_pred))/2.0))
        opened.write(json.dumps(data))
        opened.write('\n')


