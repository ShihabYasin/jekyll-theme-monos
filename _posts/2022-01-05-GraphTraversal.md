---
layout: post 
title: Graph Traversal Algo in Python 
date: 2022-01-05 16:20:23 +0900 
category: Algorithm
tag: Algorithm
---

## BFS DFS TopologicalSort Code in python
 

<p align="center">
  <img width="150" height="100" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/12.png?raw=true">
</p>
 


### DFS Study:
* Recursive
```python
adjmat =[[0,3,4],[3,5,6]]
adjls = {i: adjmat[i] for i in range(len(adjmat))}
visited = set()
def dfs(root):
    if root in visited:
        return # False
    if not adjls[root]:
        visited.add(root)
        return # True
    for n in adjls[root]:
        dfs(n)
    visited.add(root)
    return True
```

* Iterative:



### Topological Sort (for DAG only)  


```python
def tpdfs(adjMat: List[List[int]] = [[0,3,4],[3,5,6]]): # Given graph as adjMat
    adjls = {i: adjMat[i] for i in range(len(adjMat))}
    visited, topoorder = [], []

    def dfs(root):
        if root in visited:
            return 
        if not adjls[root]:
            visited.append(root)
            topoorder.append(root)
            return True
        visited.append(root)
        for n in adjls[root]:
            dfs(n) # if topo order impossible
        topoorder.append(root)

    for n in range(len(adjMat)):
        dfs(n)
    return topoorder
```
 
* Applications: 

1. Topological sort can be used to quickly find the shortest paths from the weighted directed acyclic graph.
2. It is used to check whether there exists a cycle in the graph or not
Topological sort is useful to find the deadlock condition in an operating system
3. It is used in course scheduling problems to schedule jobs
4. It is used to find the dependency resolution 
5. Topological sort is very useful to find sentence ordering in very fewer efforts 
6. It is used in manufacturing workflows or data serialization in an application 
7. It is used for ordering the cell evaluation while recomputing formula values in an excel sheet or spreadsheet. 
   

### BFS Study:

* Iterative
 
```python
from collections import deque


class TreeNode:
    def __init__(self, left=None, right=None, val=-1):
        self.left, self.right, self.val = left, right, val


def bfs(root: TreeNode):  # iterative bfs using Queue

    if not root: return

    q = deque ()
    q.append (root)

    while q:
        node = q.popleft ()
        if node:  # if node not None / last nodes
            q.append (node.left)
            q.append (node.right)
```

