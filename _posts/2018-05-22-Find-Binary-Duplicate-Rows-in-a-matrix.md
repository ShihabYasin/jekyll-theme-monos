---
layout: post
title: EASY-> Find Binary Duplicate Rows in a matrix (Python)
date: 2018-05-22 16:20:23 +0900
category: Algorithm
tag: Algorithm
---

### Find duplicate rows present in a given binary matrix by traversing the matrix only once.
```python
from collections import defaultdict
if __name__ == '__main__':

    mat = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0]
        ]

    d = defaultdict(int)
    res = []
    for r in range(len(mat)):
        if d.get(tuple(mat[r]), None) is not None:
            res.append((d.get(tuple(mat[r])), r))
        else:
            d[tuple(mat[r])] = r
    print(res)
```

Time Complexity: O(N)
Space Complexity: O(M*N)

