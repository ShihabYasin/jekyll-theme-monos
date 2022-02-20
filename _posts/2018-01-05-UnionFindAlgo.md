---
layout: post 
title: UnionFind Algorithm in Python 
date: 2018-01-05 16:20:23 +0900 
category: Algorithm
tag: Algorithm
---

* Union Find Algorithm:

```python

class UnionFind:
    def __init__(self):
        self.parent = {}

    def make_set(self, v):
        self.parent[v] = v

    def find_set(self, v):
        if v == self.parent[v]:
            return v
        self.parent[v] = self.find_set (self.parent[v])
        return self.parent[v]

    def union_sets(self, a, b):
        a = self.find_set (a)
        b = self.find_set (b)
        if a != b:
            self.parent[b] = a


class UnionFindbySize:
    def __init__(self):
        self.parent = {}
        self.size = {}

    def make_set(self, v):
        self.parent[v] = v
        self.size[v] = 1

    def find_set(self, v):
        if v == self.parent[v]:
            return v
        self.parent[v] = self.find_set (self.parent[v])
        return self.parent[v]

    def union_sets(self, a, b):
        a = self.find_set (a)
        b = self.find_set (b)
        if a != b:
            if self.size[a] < self.size[b]:
                tmp = a
                a = b
                b = a
            self.parent[b] = a
            self.size[a] += self.size[b]


class UnionFindbyRank:  # Rank is Tree height, starting from 0
    def __init__(self):
        self.parent = {}
        self.treeHeight = {}

    def make_set(self, v):
        self.parent[v] = v
        self.treeHeight[v] = 0

    def find_set(self, v):
        if v == self.parent[v]:
            return v
        self.parent[v] = self.find_set (self.parent[v])
        return self.parent[v]

    def union_sets(self, a, b):
        a = self.find_set (a)
        b = self.find_set (b)
        if a != b:
            if self.treeHeight[a] < self.treeHeight[b]:
                tmp = a
                a = b
                b = a
            if self.treeHeight[a] == self.treeHeight[b]:
                self.treeHeight[a] += 1
```


