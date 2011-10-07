# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import sys, os
import glob, json
import numpy


def acquire_rate(basedir = '.', outdir = '.'):

    table = {}
    for path in glob.glob(basedir + '/*.json'):

        with file(path) as opened:
            name = os.path.basename(path).split('.')[0]

            ids = []
            for line in opened:
                ids += [ item for item in json.loads(line) ]
            
            table[name] = ids

    
    exists_list = glob.glob(outdir + '/*.json')
    exists_table = dict(zip([ os.path.basename(path).split('.')[0] for path in exists_list ], [1] * len(exists_list)))

    print(len(exists_list))

    rate = {}
    for name, ids in table.items():
        rate[name] = len([ id for id in ids if id in exists_table ])

    score = numpy.zeros(len(table), dtype = numpy.float64)
    for i, name in enumerate(table.keys()):
        try:
            score[i] = float(rate[name]) / float(len(table[name]))
        except ZeroDivisionError:
            pass

    #score = numpy.array([ float(rate[name]) / float(len(table[name])) for name in table.keys() ])
    print(score.mean(), score.var())
    print(score.max())


if __name__ == '__main__':

    acquire_rate(sys.argv[1], sys.argv[2])
