---
layout: post 
title: Graph Traversal Algo in Python 
date: 2022-01-05 16:20:23 +0900 
category: Algorithm
tag: Algorithm
---

## BFS DFS TopologicalSort Code in python

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
```python

```

### Topological Sort
 
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