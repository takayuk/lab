# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import random
import json
import sys, os



def train_and_valid(data, trainrate, rseed):

    random.seed(rseed)

    N = len(data)
    
    train_ids = random.sample(range(N), int(len(data) * trainrate))
    valid_ids = list( set(range(N)) - set(train_ids) )

    train = [ data[i] for i in train_ids ]
    valid = [ data[i] for i in valid_ids ]

    return (train, valid)



if __name__ == '__main__':
    
    data = json.load(open(sys.argv[1]))

    TRAIN_RATE = 0.7

    N = len(data)

    train_ids = random.sample(range(N), int(len(data) * TRAIN_RATE))
    valid_ids = list( set(range(N)) - set(train_ids) )

    train = [ data[i] for i in train_ids ]
    valid = [ data[i] for i in valid_ids ]

    with file(sys.argv[1] + '.train', 'w') as opened:
        opened.write(json.dumps(train))

    with file(sys.argv[1] + '.valid', 'w') as opened:
        opened.write(json.dumps(valid))

