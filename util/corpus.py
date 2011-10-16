# encoding: utf-8
# coding: utf-8


from pymongo import Connection
import bson

import traceback


class Corpus(object):
    
    def __init__(self, address = 'localhost', database = '', collection = ''):

        if len(database) == 0 or len(collection) == 0:
            print('Need specified name database or collection.')
            return
        
        self.connection = Connection('localhost', 27017)
        self.db = self.connection[database]

        self.collection = self.db[collection]


    def __del__(self):
        
        self.connection.disconnect()


    def append(self, record):
        """ ディクショナリ形式でデータを追加, .
        """
        try:
            if self.collection.find(record).count() > 0:
                pass
            else:
                self.collection.insert(record)
        except bson.errors.InvalidStringData as e:
            print(e.message)


    def find(self, queries = None):

        findresult = {}
        for i, r in enumerate(self.collection.find(queries)):
            findresult.setdefault(i, r)
   
        return tuple([record[1] for record in findresult.items()])


    def update(self, record, new_record):

        try:
            self.collection.update(record, new_record)
        except TypeError as e:
            print('%s #%s\n\tMessage: %s'
                    % (str(self.__class__.__name__), traceback.extract_stack()[-1][2], e.message))


    def exists(self, queries):

        find_count = 0
        for attr, value in queries.items():
            result = self.find({ attr: value })
            find_count += len(result)

        return find_count > 0


    def remove(self, item):
        
        self.collection.remove(item)


if __name__ == '__main__':

    import datetime, copy

    db = Corpus(database = 'temp', collection = 'flickr')

    db.append({ 'user_id': 'aaaa' })

    for item in db.find():

        print(item)

        new_record = copy.deepcopy(item)
        new_record.setdefault('date', {'year': year, 'month': month, 'day': day})

        print(new_record)

        db.update(item, new_record)
        new_item = db.find({'user_id': item['user_id']})
        print(new_item)
        break

