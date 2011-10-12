# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


def split_seq(seq, size = 1):
    return [ seq[i:i+size] for i in range(0, len(seq), size) ]

