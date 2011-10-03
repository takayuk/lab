# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys

term_to_id = {}
docids = []

with file(sys.argv[1]) as opened:
    for line in opened:
        doc = unicode(line.strip().replace(' ',''))
        if len(doc) < 1: continue
        
        for term in doc:
            try:
                term_to_id[term]
            except KeyError:
                term_to_id[term] = len(term_to_id)+1

        docids.append([ term_to_id[term] for term in doc ])

id_to_term = dict(zip(term_to_id.values(), term_to_id.keys()))

with file(sys.argv[2], 'w') as opened:

    for ids in docids:
        opened.write('%s\n' % ' '.join([ str(id) for id in ids ]))

