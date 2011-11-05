# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import re
import sys, os
import numpy

import bagofwords as bow


#
# Unicode ひらがな [ 3041 - 309F ]
# Unicode カタカナ [ 30A1 - 30F9 ]
# Unicode 漢字 [ 4E00 - 9FBB ]
#

kigou = re.compile( u'[^\u3041-\u309f|\u30a1-\u30f9|\u4e00-\u9fbb]' )
hiragana = re.compile( u'[\u3041-\u309f]' )


def cutoff(regex, sentence, delim = ' '):
    return [ word for word in re.sub(regex, ' ', sentence).split(delim) if len(word) > 0 ]


term_to_id = {}
corpus = []


with file(sys.argv[1]) as opened:

    for j, line in enumerate(opened):

	"""
        result = bow.bagofwords(sentence = unicode(line, 'utf-8'), target_feature = ["名詞", "未知語"])
        for v in result:
            print(v[0])

	print('done')
        break
	"""
        
	token = cutoff( hiragana, re.sub(kigou, ' ', unicode(line, 'utf-8')) )
	if len(token) > 0:
		print(line)
        #print(' '.join(token))

	"""
        for term in token:
            id = term_to_id.get(term)
            if not id:
                term_to_id[term] = len(term_to_id)

        docids = numpy.array([ term_to_id.get(term, len(term_to_id)) for term in token ], dtype = int) + 1
        #print(term_to_id)
        #print(docids)
        #print(unicode(line))
        #print(' '.join(token))
        corpus.append(docids)

	"""
#print(len(term_to_id))
#print(len(corpus))
exit()

print(len(gram_table))

exclusive_gram = []
for gram, freq in gram_table.items():

    #if len(hiragana.findall(gram)) == 2:
    if len(hiragana.findall(gram)) > 0:
        exclusive_gram.append(gram)

print(len(gram_table))


for gram in exclusive_gram:
    del(gram_table[gram])


print(len(gram_table))

for gram, freq in gram_table.items():
    print(gram)
