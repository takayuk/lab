# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


"""
    Implementation of Mean-shift Clustering.
"""

from multiprocessing import Process, Array

from numpy import array, zeros
from numpy.random import normal, randint

import sys
import math
import json


def dataset(seqsize = 10, K = 2):

    means = []
    for i in range(seqsize):
        means.append( tuple([ randint(100) for k in range(K) ]) )

    dataset = []
    for i in range(seqsize):
        dataset.append( tuple(normal( means[randint(len(means))], 8.0, size = K )) )

    return dataset


def mp_meanshift(table, segment, dataset):
    """ Multi-processing Mean-shift clustering.
    """

    kernel_width = options.kernel_size

    K = len(dataset[0])

    for localid, data in enumerate(segment):
        mean = data[1]

        start_index = data[0] * K
        
        for itr in range(options.iteration):
            nsum = zeros(K)
            div = 0
            for j in range(len(dataset)):
                
                dist = math.sqrt( sum([ (dataset[j][k] - mean[k]) ** 2 for k in range(K) ]) )
                if dist <= kernel_width:
                    nsum += array(dataset[j])
                    div += 1

            nextmean = nsum / float(div)
            
            mdist = math.sqrt( sum([ ((mean[k] - nextmean[k]) ** 2) for k in range(K) ]))
            mean = nextmean
            if mdist < 3.0e-5:
                break

        for k in range(K):
            table[ start_index + k ] = mean[k]


def meanshift(dataset):
    """ Mean-shift clustering.
    """
    
    kernel_width = options.kernel_size

    K = len(dataset[0])
    table = zeros(len(dataset) * K)

    for i, data in enumerate(dataset):
        mean = data
        start_index = i * K
        
        for itr in range(options.iteration):
            nsum = zeros(K)
            div = 0
            for j in range(len(dataset)):
                dist = math.sqrt( sum([ (dataset[j][k] - mean[k]) ** 2 for k in range(K) ]) )
                if dist <= kernel_width:
                    nsum += array(dataset[j])
                    div += 1

            nextmean = nsum / float(div)
            
            mdist = math.sqrt( sum([ ((mean[k] - nextmean[k]) ** 2) for k in range(K) ]))
            mean = nextmean
            if mdist < 3.0e-5:
                break

        for k in range(K):
            table[ start_index + k ] = mean[k]

    return table


def mapper(dataset, procsize):

    segments = {}
    for i, data in enumerate(dataset):

        index = i % procsize
        if index not in segments:
            segments[index] = []

        segments[index].append((i, data))

    return segments


def args():

    script_usage = 'Usage: python %s [options]\n\t-f <path to dataset>\n\t-i <iteration>\n\t-k <kernel size>\n\t-m <threshold of merging>\n\t--np <processes>\n\t-o <path to output>' % sys.argv[0]

    import optparse
    parser = optparse.OptionParser(usage = script_usage)
    parser.add_option('-f', '--file', dest = 'input_path', default = '')
    parser.add_option('-i', '--iteration', dest = 'iteration', type = 'int', default = 10)
    parser.add_option('-k', '--kernelsize', dest = 'kernel_size', type = 'float', default = 16.0)
    parser.add_option('-m', '--mergethresh', dest = 'merge_thresh', type = 'float', default = 3.0e-3)
    parser.add_option('--np', dest = 'numof_procs', type = 'int', default = 1)
    parser.add_option('-o', dest = 'output_path', default = '')
    
    
    (opts, args) = parser.parse_args()

    if not opts.output_path:
        parser.error(script_usage)

    return (opts, args)


if __name__ == '__main__':

    (options, args) = args()

    # Read dataset or Make artifical dataset.
    if options.input_path:
        data = [ line.strip().split() for line in open(options.input_path).readlines() ]
        for i in range(len(data)):
            data[i] = [ float(value) for value in data[i] ]
    else:
        data = dataset(seqsize = 6000, K = 50)


    # Deployment for each process and Running.
    K = len(data[0])
    if options.numof_procs > 1:

        segments = mapper(data, procsize = options.numof_procs)
        table = Array( 'd', [0] * len(data) * K )

        procs = [ Process(target = mp_meanshift, args = (table, segment, data)) for segment in segments.values() ]
        for proc in procs: proc.start()
        for proc in procs: proc.join()
    else:
        table = meanshift(data)


    # Formatting results.
    results = []
    for i in range(len(data)):
        results.append( tuple([ table[(i*2) + k] for k in range(K) ]) )


    # Merging cluster using merge threshold.
    cluster_table = {}
    for i in range(len(results)):

        make_newcluster = True
        for c in cluster_table.keys():

            nv = cluster_table[c][0]

            if math.sqrt( sum([ (nv[k] - results[i][k]) ** 2 for k in range(K) ]) ) < options.merge_thresh:
                cluster_table[c].append( (i, data[i]) )
                make_newcluster = False
                break

        if make_newcluster:
            cluster_table[len(cluster_table)] = [ results[i], (i, data[i]) ]


    # Writing results to file.
    with file(options.output_path, 'w') as opened:
        opened.write(json.dumps(cluster_table))


