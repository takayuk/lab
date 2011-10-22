# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import sys, os
sys.path.append(os.path.dirname(sys.argv[0]))

import flickr_api
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

            filepath = os.path.join(self.basedir, '%s.json' % args)

            for args_photo in args:
                response = self.api.call(method = self.method, args = args)
                #response = self.api.call(method = self.method, args = { 'user_id': args })
                #response = self.api.call(method = self.method, args = { 'photo_id': args })
                with file(filepath, 'w') as opened:
                    opened.write(json.dumps(response))
            
            time.sleep(0.05)


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


def args():

    script_usage = 'Usage: python %s [options]\n\t-f <path to dataset>\n\t-m <API method>\n\t--np <threads>\n\t-o <path to output>' % sys.argv[0]

    import optparse
    parser = optparse.OptionParser(usage = script_usage)
    parser.add_option('-f', '--file', dest = 'filename')
    parser.add_option('-m', '--method', dest = 'api_method')
    parser.add_option('--np', dest = 'threads', type = 'int', default = 1)
    parser.add_option('-o', dest = 'basedir', default = '.')

    (opts, args) = parser.parse_args()

    if not (opts.filename and opts.basedir):
        parser.error(script_usage)

    return (opts, args)



if __name__ == '__main__':

    (options, args) = args()
 
    argslist = json.load(open(options.filename))
    
    bot = Snapbot(options.api_method, argslist, numof_thread = options.threads, output_dir = options.basedir)
    bot.run()

