# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import random


def dataset(size = 10):

    
    docs = []
    for i in range(size):
        print(i)
        docs.append( ' '.join([ str(random.randint(10, 1000)) for i in range(random.randint(10, 1000)) ]) )

    return docs


doc_to_ids = {}
termid_to_docids = {}
term_to_id = {}


def build():

    for docid, termids in doc_to_ids.items():
        for termid in termids:
            try:
                termid_to_docids[termid].append(docid)
            except KeyError:
                termid_to_docids[termid] = [ docid ]


def tfidf(term_id, doc_id = None):

    try:
        tf = float( doc_to_ids[doc_id][term_id] ) / float( sum(doc_to_ids[doc_id].values()) )
        df = float( len(termid_to_docids[term_id]) )
    except KeyError:
        (tf, df) = (0, 1)

    return (tf / df)


if __name__ == '__main__':

    docs = dataset(10000)

    for j, doc in enumerate(docs):

        term_freq = {}
        for term in doc.split():
            try:
                term_id = term_to_id[term]
            except KeyError:
                term_id = term_to_id[term] = len(term_to_id)+1


            try:
                term_freq[term_id] += 1
            except KeyError:
                term_freq[term_id] = 1
            
        doc_to_ids[j+1] = term_freq

    build()

    for i in range(100):
        val = tfidf(term_id = random.randint(1, len(term_to_id)-2), doc_id = random.randint(1, len(doc_to_ids)-2))
        print(val)

