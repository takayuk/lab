# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import json
import sys, os
import numpy
import math
import glob

ps = glob.glob('res/*')


for path in ps:
    
    sim = []
    simr = []
    t = []
    et = []

    with file(path) as opened:
        for line in opened:
            data = json.loads(line)
            sim.append(data['sim'])
            simr.append(data['simr'])
            t.append(data['t'])
            et.append(data['et'])

    nsim = numpy.array(sim)
    nsimr = numpy.array(simr)

    print(data['k']+1, data['l'])
    print('%f %f' % (numpy.average(nsim), numpy.var(nsim)))
    print('%f %f' % (numpy.average(nsimr), numpy.var(nsimr)))

    t_err = numpy.array([ math.fabs(_t - _et) for _t, _et in zip(t, et) ])
    print('%f %f' % (numpy.average(t_err), numpy.var(t_err)))

