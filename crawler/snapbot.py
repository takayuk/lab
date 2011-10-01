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
    def __init__(self, args_sem, args_list, api, method, output_dir):

        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.args_sem = args_sem
        self.args_list = args_list

        self.api = api

        self.basedir = output_dir
        self.method = method

    def _new_args(self):

        self.args_sem.acquire()
        args = self.args_list.pop()
        self.args_sem.release()

        return args

    def run(self):

        while len(self.args_list) > 0:

            args = self._new_args()

            with file(os.path.join(self.basedir, '%s.json' % (args[0])), 'w') as opened:
                for args_photo in args[1]:
                    response = self.api.call(method = self.method, args = { 'photo_id': args_photo })
                    opened.write('%s\n' % json.dumps(response))
            print(args[0])
            time.sleep(10.0)

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
            worker = Worker(self.args_sem, self.argslist, self.api, self.method, output_dir)
            self.workers.append(worker)
            worker.start()

    def run(self):

        print(self.method)
        for worker in self.workers:
            worker.join()


if __name__ == '__main__':

    #argslist = sorted([ l.strip().split()[2] for l in open(sys.argv[1]) ])
    argslist = []
    
    pathlist = sorted(glob.glob('/home/takayuk/dataset/expdata/dataset/set1/photos_0-2/*.json'))[:10000]
    for i, path in enumerate(pathlist):
        name = os.path.basename(path).split('.')[0]
        photos = json.load(open(path))

        argslist.append((name, photos))

    #print(argslist[:3])

    print(len(argslist))

    method = sys.argv[3]
    bot = Snapbot(method, argslist, numof_thread = int(sys.argv[4]), output_dir = sys.argv[2])
    bot.run()

