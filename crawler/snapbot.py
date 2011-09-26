# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import sys, os
sys.path.append(os.path.dirname(sys.argv[0]))

import flickr_callapi
#import twitter

import threading
import time
import json
import glob

class Worker(threading.Thread):
    """ スレッド化されたBot本体.
    """
    def __init__(self, args_sem, args_list, api, output_dir):

        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.args_sem = args_sem
        self.args_list = args_list

        self.api = api

        self.basedir = output_dir

    def _new_args(self):

        self.args_sem.acquire()
        args = self.args_list.pop()
        self.args_sem.release()

        return args

    def run(self):

        while len(self.args_list) > 0:

            args = self._new_args()

            response = self.api.call(method = 'flickr.contacts.getPublicList', args = { 'user_id': args })

            time.sleep(0.1)

            #with file('1st/%s.json' % args, 'w') as f:
            with file(os.path.join(self.basedir, '%s.json' % args), 'w') as opened:
            #with file('expdata/2nd/%s.json' % args, 'w') as f:
                #f.write(json.dumps(response))
                opened.write(json.dumps(response))


class Snapbot():
    """ ネットワーク情報のスナップショットを取得するBot.
    """
    def __init__(self, method, argslist, numof_thread = 1, output_dir = '.'):

        self.method = method
        self.argslist = argslist

        self.args_sem = threading.Semaphore()

        self.api = flickr_callapi.FlickrAPI()

        self.workers = []
        for i in range(numof_thread):
            worker = Worker(self.args_sem, self.argslist, self.api, output_dir)
            self.workers.append(worker)
            worker.start()

    def run(self):

        for worker in self.workers:
            worker.join()


if __name__ == '__main__':

    basedir = sys.argv[1]
    #output_dir = sys.argv[2]

    #path_list = glob.glob('expdata/1st/*.json')
    #path_list = glob.glob('%s/*.json' % basedir)
    argslist = [ os.path.basename(path).split('.')[0] for path in glob.glob('%s/*.json' % basedir) ]

    with file('/home/takayuk/dataset/expdata/set1/set1_0915_bi.lbl') as opened:
        for line in opened:
            urlid += [ int(l) for l in line.strip().split() ]

    urlid = list(set(urlid))
    print(len(urlid))
    exit()

    """
    names = []
    for i, path in enumerate(path_list):
        names += json.load(open(path))
        print(i)
    """

    """
    checked_list = [ os.path.basename(path).split('.')[0] for path in path_list ]
    checked_table = dict(zip(checked_list, [1] * len(checked_list)))
    """
   
    #argslist = list(set(names))
    print(len(argslist))

    method = sys.argv[3]
    bot = Snapbot(method, argslist, numof_thread = int(sys.argv[4]), output_dir = sys.argv[2])
    bot.run()

    '''
    for path in path_list:
        
        #data = json.load(open(path))
        #data = [ arg for arg in data if not arg in checked_table ]
        
        #argslist = json.load(open(sys.argv[2]))
        #argslist = data
        
        bot = Snapbot(method, argslist, numof_thread = int(sys.argv[4]), output_dir = sys.argv[2])
        bot.run()

        """
        for i in data:
            checked_table.setdefault(i, 1)

        print('%s done...' % path)
        """
        
        del(bot)
    '''

    """
    _api = flickr_callapi.FlickrAPI()
    root = _api.call('flickr.contacts.getPublicList', { 'user_id': '44754523@N05' })

    with file(sys.argv[2], 'w') as f:
        f.write(json.dumps(root))
    """
    """
    
    argslist = json.load(open(sys.argv[2]))
    bot = Snapbot(method, argslist, numof_thread = int(sys.argv[3]))
    bot.run()
    """
