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
    if not adjls[root]:
        return True
    if root in visited:
        return False
    visited.add(root)
    for n in adjls[root]:
        if not dfs(n): return False
    visited.remove(root)
    return True
```

* Iterative:
```python

```

### Topological Sort

```python
given__adjmat = [[1, 3, 2], [2, 0, 6], [4, 1, 3]]

adjls = {i: given__adjmat[i] for i in range (len (given__adjmat))}
visited, toposortorder = [], [],  # toposortorder contains result
tlnodes = 10

def dfstopo(root):
    if not adjls[root]:
        return True
    if root in visited:
        return False
    visited.append (root)
    for n in adjls[root]:
        if not dfstopo (n): return False
    toposortorder.append (root)    

for nd in range (tlnodes): # for disconnected components
    dfstopo (nd)
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