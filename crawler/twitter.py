# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.dirname(sys.argv[0]))

import base64, urllib, urllib2
import json, re, time
from pit import Pit

import corpus


class StreamingAPI:

    def __init__(self, db_name, coll_name):

        self.base_url = 'http://stream.twitter.com/1/statuses/sample.json'

        self.config = Pit.get('twitter_api_gardenhose')
        
        self.user = self.config['user']
        self.passwd = self.config['passwd']

        self.db = corpus.Corpus(database = db_name, collection = coll_name)
    
    def _request(self):

        request = urllib2.Request('http://stream.twitter.com/1/statuses/sample.json')
        basic = base64.encodestring('%s:%s' % (user, passwd))[:-1]
        request.add_header('Authorization', 'Basic %s' % basic)
    
        response = urllib2.urlopen(request)
        for line in response:
            if line.strip() is not '':
                yield line

    def call(self):

        while True:
            stream = self._request()
            
            while True:
                try:
                    streaming_response = json.loads(stream.next())
                    self.db.append(streaming_response)
                
                except StopIteration as e:
                    print(e.message)
                    time.sleep(10)
                    break
                
                except KeyError, ValueError:
                    pass


if __name__ == '__main__':

    hankaku_all = re.compile(r"^[!-~]+$")

    import sys
    db = corpus.Corpus(database = 'corpus', collection = sys.argv[1])

    client = StreamingAPI(db_name = 'corpus', coll_name = 'twitter')
