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

            #filepath = os.path.join(self.basedir, '%s.json' % args[0])
            filepath = os.path.join(self.basedir, '%s.json' % args)

            """
            if not os.path.exists(filepath):
                with file(filepath, 'w') as opened: pass
            """
            #for args_photo in args[1]:
            for args_photo in args:
                response = self.api.call(method = self.method, args = { 'photo_id': args })
                #response = self.api.call(method = self.method, args = { 'user_id': args_photo })
                """
                with file(filepath, 'a') as opened:
                    opened.write('%s\n' % json.dumps(response))
                """
                with file(filepath, 'w') as opened:
                    opened.write(json.dumps(response))
            """
            response = self.api.call(method = self.method, args = { 'user_id': args })
            with file(filepath, 'w') as opened:
                opened.write(json.dumps(response))
            """ 
            print(len(self.args_list))
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

    """
    pathlist = sorted(glob.glob('./temp/*.json'))

    names = [ os.path.basename(path).split('.')[0] for path in glob.glob(sys.argv[2] + '/*.json') ]
    table = dict(zip(names, [1] * len(names)))

    for i, path in enumerate(pathlist):
        name = os.path.basename(path).split('.')[0]

        with file(path) as opened:
            for j, line in enumerate(opened):
                argslist += [ id for id in json.loads(line) if not id in table ]
                #photos = json.loads(line)
                #argslist += [ v[1] for v in photos ]
    argslist = list(set(argslist))

    size = 10000
    div_argslist = [ argslist[i:i+size] for i in range(0, len(argslist), size) ]
    print(len(div_argslist))
    for i, div in enumerate(div_argslist):
        with file('div_argslist_%d.json' % i, 'w') as opened:
            opened.write(json.dumps(div))
    exit()
    """
    
    bot = Snapbot(options.api_method, argslist, numof_thread = options.threads, output_dir = options.basedir)
    bot.run()

