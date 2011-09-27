# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


def load_file_json(filename):
    
    import json
    data = json.load(open(filename))

    corpus = []

    for u, groups in data.items():
        corpus.append(groups)

    return corpus


def load_file(filename):

    corpus = []

    with file(filename) as opened:

        for j, line in enumerate(opened):
            if j == 0:
                continue

            terms = []
            for word in line.strip().split()[1:]:

                tf = word.split(':')
                terms += [ int(tf[0]) ] * int(tf[1])

            corpus.append(terms)
    return corpus


class Vocabulary:
    
    def __init__(self, excluds_stopwords=False):
        self.vocas = []        # id to word
        self.vocas_id = dict() # word to id
        self.docfreq = []      # id to document frequency
    
    
    def term_to_id(self, term):
        if not term in self.vocas_id:
            voca_id = len(self.vocas)
            self.vocas_id[term] = voca_id
            self.vocas.append(term)
            self.docfreq.append(0)
        else:
            voca_id = self.vocas_id[term]

        return voca_id


    def doc_to_ids(self, doc):
        
        list = []
        words = dict()
        for term in doc:
            id = self.term_to_id(term)
            if id != None:
                list.append(id)
                words[id] = 1

        for id in words: self.docfreq[id] += 1
        return list
    
    
    def __getitem__(self, v):
        return self.vocas[v]

    def size(self):
        return len(self.vocas)

    def id_to_term(self, id):
        return self.vocas[id]

