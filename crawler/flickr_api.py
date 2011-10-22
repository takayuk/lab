# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


import sys, os
sys.path.append(os.path.dirname(sys.argv[0]))

import json
import cgi, urllib

import copy


class FlickrAPI:

    def __init__(self, api_key = 'flickr_api'):

        self.method_map = {
            'flickr.photos.getInfo': self.photos_getinfo,
            'flickr.people.getPublicPhotos': self.people_getpublicphotos,
            'flickr.people.getPublicGroups': self.people_getpublicgroups,
            'flickr.contacts.getPublicList': self.contacts_getpubliclist,
            'flickr.favorites.getPublicList': self.favorites_getpubliclist,
            'flickr.groups.pools.getPhotos': self.groups_pools_getphotos,
            'flickr.photos.comments.getList': self.photos_comments_getlist,
        }
        self.query_template = { 'format': 'json', 'nojsoncallback': '1' }
        
        #from pit import Pit
        #self.api = Pit.get(api_key)
        self.api = { 'key': '8cc9b4664c0c9ee5cfc10cadbfd2ac87' }


    def request(self, method, args_map): 
        
        args = '&'.join(
            ["%s=%s" % (cgi.escape(arg[0]), cgi.escape(arg[1])) for arg in args_map.items()])

        request_url = "http://www.flickr.com/services/rest/?api_key=%s&method=%s&%s" % (
                self.api['key'], method, args)
       
        return json.load(urllib.urlopen(request_url))


    def call(self, method, args):

        call_method = self.method_map[method]
        return call_method(args)
    
        
    def photos_getinfo(self, args):
        
        query = copy.copy(self.query_template)

        for k, v in args.items():
            query.setdefault(k, str(v))

        try:
            response = self.request('flickr.photos.getInfo', query)
            return response['photo']['owner']

        except KeyError as e:
            return None
        except ValueError as e:
            return None


    def photos_comments_getlist(self, args):
        
        import copy
        query = copy.copy(self.query_template)

        for k, v in args.items():
            query.setdefault(k, str(v))

        result = []

        try:
            response = self.request('flickr.photos.comments.getList', query)
            result += [ (args['photo_id'], item['author'], item['datecreate']) for item in response['comments']['comment'] ]
            #result += [ (item['author'], item['datecreate']) for item in response['comments']['comment'] ]

        except KeyError as e:
            return []
        except ValueError as e:
            return []

        return list(set(result))

   
    def groups_pools_getphotos(self, args):

        import copy
        query = copy.copy(self.query_template)

        for k, v in args.items():
            query.setdefault(k, str(v))

        local_args = { 'perpage': '500', 'page': '1' }

        for k, v in local_args.items():
            if not k in query:
                query.setdefault(k, str(v))
        
        result = []

        page = 1
        totalpage = None

        while True:
            try:
                response = self.request('flickr.groups.pools.getPhotos', query)
                result += [ (item['id'], item['owner']) for item in response['photos']['photo'] ]

                if not totalpage:
                    totalpage = int(response['photos']['pages'])

            except KeyError:
                return []
            except ValueError:
                return []

            page += 1

            if page <= totalpage:
                query['page'] = str(page)
            else:
                break
        
        return list(set(result))




    def people_getpublicgroups(self, args):
        
        import copy
        query = copy.copy(self.query_template)

        for k, v in args.items():
            query.setdefault(k, str(v))

        result = []

        try:
            response = self.request('flickr.people.getPublicGroups', query)
            result += [ (item['nsid'], item['name']) for item in response['groups']['group'] ]

        except KeyError as e:
            print(e.message)
            return []
        except ValueError as e:
            print(e.message)
            return []

        return list(set(result))


    def favorites_getpubliclist(self, args):

        import copy
        query = copy.copy(self.query_template)

        for k, v in args.items():
            query.setdefault(k, str(v))

        local_args = { 'perpage': '500', 'page': '1' }

        for k, v in local_args.items():
            if not k in query:
                query.setdefault(k, str(v))
        
        result = []

        page = 1
        totalpage = None

        while True:
            try:
                response = self.request('flickr.favorites.getPublicList', query)
                result += [ (item['id'], item['owner']) for item in response['photos']['photo'] ]

                if not totalpage:
                    totalpage = int(response['photos']['pages'])

            except KeyError:
                return []
            except ValueError:
                return []

            page += 1

            if page <= totalpage:
                query['page'] = str(page)
            else:
                break
        
        return list(set(result))

    
    def people_getpublicphotos(self, args):
        
        import copy
        query = copy.copy(self.query_template)

        for k, v in args.items():
            query.setdefault(k, str(v))

        local_args = { 'perpage': '500', 'extras': 'date_upload,date_taken,last_update,views' }

        for k, v in local_args.items():
            if not k in query:
                query.setdefault(k, str(v))
        
        result = []

        page = 1
        totalpage = None

        while True:
            try:
                response = self.request('flickr.people.getPublicPhotos', query)
                result += [ (item['id'], item['dateupload']) for item in response['photos']['photo'] ]

                if not totalpage:
                    totalpage = int(response['photos']['pages'])
            
            except (KeyError, ValueError), inst:
                #print(inst)
                return []
            
            page += 1

            if page <= totalpage:
                query['page'] = str(page)
            else:
                break
        
        return list(set(result))



    def contacts_getpubliclist(self, args):
        
        import copy
        query = copy.copy(self.query_template)

        for k, v in args.items():
            query.setdefault(k, str(v))

        local_args = { 'perpage': '1000' }

        for k, v in local_args.items():
            if not k in query:
                query.setdefault(k, str(v))
        
        result = []

        page = 1
        totalpage = None

        while True:
            try:
                response = self.request('flickr.contacts.getPublicList', query)
                result += [ item['nsid'] for item in response['contacts']['contact'] ]

                if not totalpage:
                    totalpage = int(response['contacts']['pages'])
            
            except (KeyError, ValueError), inst:
                print(inst)
                return []
            
            page += 1

            if page <= totalpage:
                query['page'] = str(page)
            else:
                break
        
        return list(set(result))


def option():

    from optparse import OptionParser
    
    parser = OptionParser()
   
    parser.add_option('-o', '--output', dest = 'output', default = '.')
    parser.add_option('-f', '--file', dest = 'filepath')
    #parser.add_option('-d', '--dir', dest = 'dirpath')
    #parser.add_option('-i', '--iteration', dest = 'iteration', type = 'int', default = 1)
    parser.add_option('-l', '--pagelimit', dest = 'pagelimit', type = 'int', default = 1)
    #parser.add_option('-w', '--waittime', dest = 'waittime', type = 'int', default = 60)
    parser.add_option('-m', '--method', dest = 'method')
    parser.add_option('-u', '--urlid', dest = 'urlid')
 
    (options, args) = parser.parse_args()

    if not options.method: parser.error("need specified method.")
    
    return (options, args)



if __name__ == '__main__':

    (options, args) = option()

    call_method = method_map[options.method]

    call_method(options.output)

