# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import sys, os
sys.path.append(os.path.join(os.pardir, 'util'))

import similarity
import json
import numpy
import matplotlib.pylab as plt
import math

def load_label(path):
    """ Load label-list from file.
    """
    lbl = []
    with file(path) as opened:
        for line in opened:
            lbl.append([ int(v) for v in line.strip().split() ])

    return lbl


if __name__ == '__main__':

    # Calculate Jaccard-coefficient for all links.
    vals = json.load(open(sys.argv[1]))

    vals = [ int(v) for v in vals if int(v) > 0 ]
    total = float(len(vals))
    deg = {}
    for v in vals:
        try:
            deg[v] += 1
        except KeyError:
            deg[v] = 1

    for v in deg.keys():
        deg[v] = float(deg[v]) / total

    
    """
    range_step = 0.01
    total = float(len(vals))

    plots = {}
    for x in numpy.arange(1.0, step = range_step):
        plots[x] = float(len([ s for s in vals if x <= s < x + range_step ])) / total

    print(plots.values())
    """
    
    #plt.plot(numpy.arange(1.0, step = range_step), plots.values())
    #plt.plot(deg.keys(), deg.values(), ',')
    plt.loglog(deg.keys(), deg.values(), ',')
    #plt.xlim(-range_step, 1.0+range_step)
    plt.savefig(sys.argv[2] + '.png')

