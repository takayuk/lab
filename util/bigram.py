# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import re
import sys, os

#
# Unicode ひらがな [ 3041 - 309F ]
# Unicode カタカナ [ 30A1 - 30F9 ]
# Unicode 漢字 [ 4E00 - 9FBB ]
#

kigou = re.compile( u'[^\u3041-\u309f|\u30a1-\u30f9|\u4e00-\u9fbb]' )
hiragana = re.compile( u'[\u3041-\u309f]' )

gram_table = {}

with file(sys.argv[1]) as opened:

    for j, line in enumerate(opened):
        
        bigram = []
        doc = re.sub(kigou, '', unicode(line))
        
        for x in range(len(doc)):
            #bigram.append( ''.join([doc[-(x+1)], doc[-x]]) )
            bigram.append( doc[x] )

        for gram in bigram:
            try:
                gram_table[gram] += 1
            except KeyError:
                gram_table[gram] = 1

        print(j)

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
