# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


from multiprocessing import Process, Array
from numpy.random import normal, randint

import math
import json


def dataset(seqsize = 10):

    means = [ (24, 54), (65, 23), (76, 81) ]

    dataset = []
    for i in range(seqsize):
        dataset.append(tuple(normal( means[randint(len(means))], 8.0, size = len(means[0]) )))

    return dataset


def meanshift(table_x, table_y, segment, dataset):

    kernel_width = options.kernel_size

    for localid, data in enumerate(segment):
        mean = data[1]
        
        for itr in range(options.iteration):
            nsum = [0] * 2
            div = 0
            for j in range(len(dataset)):
                dist = math.sqrt( ((dataset[j][0] - mean[0]) ** 2) + ((dataset[j][1] - mean[1]) ** 2))
                if dist <= kernel_width:
                    nsum[0] += dataset[j][0]
                    nsum[1] += dataset[j][1]
                    div += 1

            nextmean = [0] * 2
            nextmean[0] = float(nsum[0]) / float(div)
            nextmean[1] = float(nsum[1]) / float(div)

            mdist = math.sqrt( ((mean[0] - nextmean[0]) ** 2) + ((mean[1] - nextmean[1]) ** 2))
            mean = nextmean
            if mdist < 3.0e-5:
                break

        table_x[data[0]] = mean[0]
        table_y[data[0]] = mean[1]

        if localid % 1000 == 0: print(localid)


def mapper(dataset, procsize):

    segments = {}
    for i, data in enumerate(dataset):

        index = i % procsize
        if index not in segments:
            segments[index] = []

        segments[index].append((i, data))

    return segments


def args():

    script_usage = 'Usage: %s [options] -f <path to validation-set> -o <output_path> --docdist <path to docdist>'

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

    if options.input_path:
        data = [ line.strip().split() for line in open(options.input_path).readlines() ]
        for i in range(len(data)):
            data[i] = [ float(value) for value in data[i] ]
    else:
        data = dataset(seqsize = 100)

    segments = mapper(data, procsize = options.numof_procs)

    table_x = Array('d', [0] * len(data))
    table_y = Array('d', [0] * len(data))

    procs = [ Process(target = meanshift, args = (table_x, table_y, segment, data)) for segment in segments.values() ]

    for proc in procs: proc.start()
    for proc in procs: proc.join()
    
    results = zip(table_x[:], table_y[:])

    cluster_table = {}
    for i in range(len(results)):

        make_newcluster = True
        for k in cluster_table.keys():
            nx = cluster_table[k][0][0]
            ny = cluster_table[k][0][1]

            if math.sqrt(((nx - results[i][0])**2) + ((ny - results[i][1])**2)) < options.merge_thresh:
                cluster_table[k].append( (i, data[i]) )
                make_newcluster = False
                break
        
        if make_newcluster:
            cluster_table[len(cluster_table)] = [ results[i], (i, data[i]) ]


    with file(options.output_path, 'w') as opened:
        opened.write(json.dumps(cluster_table))
        
