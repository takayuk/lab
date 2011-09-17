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

    lbl = load_label(sys.argv[1])

    # Calculate Jaccard-coefficient for all links.
    jaccard_vals = []
    cosine_vals = []

    checktable = {}
    for i, label in enumerate(lbl):

        u = i+1
        for v in label:
            if len(lbl[v-1]) == 0: continue

            check_key = tuple(sorted([u, v]))
            if check_key not in checktable:

                sim_uv = similarity.jaccard(lbl[u-1], lbl[v-1])
                jaccard_vals.append(sim_uv)

                sim_uv_cos = (1.0 / math.sqrt(len(lbl[u-1]))) * (1.0 / math.sqrt(len(lbl[v-1]))) * float(len(set(lbl[u-1]) & set(lbl[v-1])))
                cosine_vals.append(sim_uv_cos)
                #sim_uv = float( len(set(lbl[u-1]) & set(lbl[v-1])) ) / float( len( 
                """
                orlist = sorted(list(set(lbl[u-1]) | set(lbl[v-1])))
                feat_u = [0.0] * len(orlist)



                """

                
                checktable[check_key] = 1
        print('%d / %d' % (i, len(lbl)))

    range_step = 0.01
    total = float(len(jaccard_vals))

    plots = {}
    for x in numpy.arange(1.0, step = range_step):
        plots[x] = float(len([ s for s in jaccard_vals if x <= s < x + range_step ])) / total

    print(plots.values())

    plt.plot(numpy.arange(1.0, step = range_step), plots.values())
    plt.xlim(-range_step, 1.0+range_step)
    plt.savefig(sys.argv[2] + '.png')

    with file(sys.argv[2] + '.json', 'w') as opened:
        opened.write(json.dumps(jaccard_vals))

    with file(sys.argv[2] + '.cos.json', 'w') as opened:
        opened.write(json.dumps(cosine_vals))
