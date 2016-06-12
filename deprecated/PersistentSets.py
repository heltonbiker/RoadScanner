#!/usr/bin/env python
# coding: utf-8

import os

class PersistentSet(object):
    def __init__(self, fname):
        self._fname = fname
        self._items = {}

        if (not os.path.exists(self._fname)):
            with open(self._fname, 'w'):
                pass
        else:
            with open(self._fname) as itemsfile:
                for line in itemsfile:
                    self._deserializeItem(line)

    def _deserializeItem(self, string):
        raise Exception("not implemented")

    def __getitem__(self, key):
        return self._items[key]


class NodeSet(PersistentSet):
    def __init__(self, fname):
        super(NodeSet, self).__init__(fname)
        self._lastIndex = len(self._items)

    def _deserializeItem(self, string):
        index, lat, lon = map(int, string.strip().split(';'))
        node = (lat, lon)        
        self._items[node] = index

    def addNode(self, node):
        if node in self._items.values():
            return -1
        self._lastIndex += 1
        index = self._lastIndex        
        self._items[node] = index
        with open(self._fname, 'a') as nodesfile:
            nodesfile.write("{};{};{}\n".format(index, node[0], node[1]))
        return index

    def contains(self, node):
        return node in self._items

    def latlons(self):
        return zip(*list(self._items))


class EdgeSet(PersistentSet):
    def __init__(self, fname):
        super(EdgeSet, self).__init__(fname)

    def _deserializeItem(self, string):
        return tuple(map(int, string.strip().split(';')))

    def addEdge(self, edge):
        if edge in self._items:
            return
        with open(self._fname, 'a') as edgesfile:
            edgesfile.write("{};{}\n".format(*edge))


    def contains(self, edge):
        pass

    def latlonpairs(self):
        return [[]]


class Seeds(object):
    def __init__(self, fname):
        self._fname = fname
        self._seeds = deque()

        if (not os.path.exists(self._fname)):
            with open(self._fname, 'w'):
                pass
        else:
            with open(self._fname) as nodesfile:
                self._seeds = deque([tuple(map(int, l.split(';'))) for l in nodesfile if l])

    def push(self, seed):
        if seed not in self._seeds:
            self._seeds.append(seed)
            with open(self._fname, 'w') as out:
                out.writelines(["{};{}\n".format(*seed) for seed in self._seeds])

    def pop(self):
        return self._seeds.popleft()

    def purge(self, node):
        if node in self._seeds:
            self._seeds.remove(node)

    def latlons(self):
        return zip(*self._seeds) 
