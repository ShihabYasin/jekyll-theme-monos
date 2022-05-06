---
layout: post 
title: Heap Notes for Python 
date: 2022-01-05 16:20:23 +0900 
category: DataStructure
tag: DataStructure
---

## Some usage of Python heapq:

1. Getting _**nlargest**_, **_nsmallest_** from a list etc.

```python
from heapq import nlargest, nsmallest
l = [('a',10), ('b',4)]
print(nlargest(2, l, key=lambda x: x[1]))
```

2. _**Heap**_ as it is. 


```python
import heapq as heap  # deafult get min heap formation, for max heap just negate all values
print("Min heap test")
lsvalue = [3, -4, -1, 15, 6, 79, -1, 0, 3, 44, 9]
pq = lsvalue[:]
heap.heapify (pq)
heap.heappush (pq, -100)  # adding new val in heap
for _ in range (0, len (pq)):
    print (heap.heappop (pq), end='  ')

# For max heap
print("\nMax heap test")
pq = [-x for x in lsvalue]
heap.heapify (pq)
heap.heappush (pq, -(-100))  # negating original input(-100) too

for _ in range (0, len (pq)):
    print ((-1) * heap.heappop (pq), end='  ') # -1 * to get original vals
```


3. _**Customized value/Node**_ based max heap.  
 

```python
import heapq
class Node:
    def __init__(self, val, count):
        self.val,self.count = val, count
    def __lt__(self, other):
        return self.count > other.count  # change < for min heap

lsnode = []
for i in range(10):
    lsnode.append(Node(i,i))
pq = lsnode[:6] # creating another variable not to overrirde else  work on lsnode
heapq.heapify(pq)
for i in range(len(pq)):
    print(heapq.heappop(pq).count)
```


4. _**Important APIs**_. 
```
['heappush', 'heappop', 'heapify', 'heapreplace: pop then push', 'merge: merges 2 sorted list',
           'nlargest', 'nsmallest', 'heappushpop']
```