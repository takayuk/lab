from svm import *
from svmutil import *

if __name__=='__main__':
    #label = [1,-1,1]
    label = [1,-1]
    #data = [[0.2, 0.0, 1.0], [0.1, 0.99, 0.1], [0.3, 0.0, 0.3]]
    data = [[0.2], [0.1]]
    problem = svm_problem(label, data)
    #parameter = svm_parameter('-s 0 -t 0')
    #parameter = svm_parameter('-c 3 -t 0')
    parameter = svm_parameter('-t 0 -c 3')
    t = svm_train(problem, parameter)
    test_label = [1, 1, -1, -1]
    #test_data = [[0.7, 0.03, 0.8], [0.2, 0.13, 0.33], [0.1, 1.0, 0.8], [0.1, 0.96, 0.2]]
    test_data = [[0.7], [0.2], [0.1], [0.1]]
    result = svm_predict(test_label, test_data , t)

    print '-------------------'
    for r in result:
        print r
