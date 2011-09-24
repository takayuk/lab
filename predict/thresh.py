# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys, os

with file(sys.argv[1]) as opened:
    for line in opened:
        if line.find('obj = ') > -1:
            (obj, rho) = line.strip().split(',')

obj = float(obj.split(' = ')[1])
rho = float(rho.split(' = ')[1])

#y = obj*x + rho

print(obj, rho)
thresh = (-rho) / obj

print(thresh)

