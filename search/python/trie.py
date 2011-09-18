# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


class Node:

    def __init__(self, x, bros = None, child = None):

        self.data = x
        self.bros = bros
        self.child = child

        self.doc_ids = []

    def set_child(self, x, doc_id):
        child = Node(x, self.child, doc_id)
        self.child = child

        # Added...
        #self.doc_ids.append(id)
        print(self.doc_ids)
        
        return child

    def get_child(self, x):

        child = self.child
        while child:
            if child.data == x: break
            child = child.bros
        return child

    def traverse(self, leaf):
        if self.data == leaf:
            yield []
        else:
            child = self.child
            while child:
                for x in child.traverse(leaf):
                    yield [ self.data ] + x
                child = child.bros



class Trie:
    """ Trie-tree for text search.
    """


    def __init__(self, x = None):
        self.root = Node(None)
        self.leaf = x

    def search(self, seq):
        node = self.root
        for x in seq:
            node = node.get_child(x)
            if node is None: return False

        return node.get_child(self.leaf) is not None

    #def insert(self, seq, doc_id):
    def insert(self, seq):
        # Rootから 
        node = self.root
        for x in seq:
            child = node.get_child(x)
            if not child:
                #child = node.set_child(x)
                child = node.set_child(x, doc_id)
            node = child

            if not node.get_child(self.leaf):
                #node.set_child(self.leaf)
                node.set_child(self.leaf, doc_id)

    def traverse(self):
        node = self.root.child
        while node:
            for x in node.traverse(self.leaf):
                yield x
            node = node.bros


if __name__ == '__main__':

    def make_suffix_trie(seq):
        a = Trie()

        for j, doc in enumerate(seq):
            print(doc)
            for x in range(len(doc)):
                a.insert(doc[x:])
        return a

    s = make_suffix_trie(['aba'])

    for x in s.traverse():
        print(x)
    
    for x in ['a', 'bc', 'x', 'ab', 'xxxxfdaj']:
        #print(x)
        r = s.search(x)
        #print(r)
        """
        for y in s.common_prefix(x):
            print(y)

        """

