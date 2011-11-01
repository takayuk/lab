# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


from svm import *
from svmutil import *

from numpy import random
random.seed(64)

K = 2
D = 10

data_p = [ [ random.normal(1, 1.6) for k in range(K) ] for i in range(D) ]
label_p = [1] * len(data_p)

data_n = [ [ random.normal(-1, 1.6) for k in range(K) ] for i in range(D) ]
label_n = [-1] * len(data_n)


problem = svm_problem(label_p + label_n, data_p + data_n)
param = svm_parameter('-s 0 -t 0')

learning = svm_train(problem, param)
print(dir(learning))

label = svm_predict([1]*len(data_p), data_p, learning)

print(label[0])
"""
for x in data_p:
    print(x)
    label = svm_predict([1], [x], learning)
    print(label)
"""
