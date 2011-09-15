# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


def kldivergence(p, q):

    import math

    kldivergence = 0
    for k in range(len(p)):
        kldivergence += -p[k] * math.log(q[k] / p[k])

    return kldivergence


def cosine(p, q):

    cosine = 0
    for i, j in zip(p, q):
        cosine += i * j

    import math
    pnorm = math.sqrt(sum([ v**2 for v in p]))
    qnorm = math.sqrt(sum([ w**2 for w in q]))

    return (cosine / (pnorm * qnorm))


def jaccard(p, q):

    try:
        jaccard = float(len(set(p) & set(q))) / float(len(set(p) | set(q)))
    except ZeroDivisionError:
        jaccard = 0

    return jaccard


def similarity(p, q, method):

    methods = { 'kld': kldivergence, 'cos': cosine, 'jac': jaccard }
    sim = methods[method]

    return sim(p, q)


if __name__ == '__main__':

    p = [0.2, 0.5, 0.1, 0.2]
    q = [0.1, 0.3, 0.2, 0.4]
    
    s = similarity(p, q, method = 'kld')

    p = [1, 4, 324, 231, 5]
    q = [4, 5, 34, 52, 6]

    s = similarity(p, q, method = 'jac')

    print(s)

