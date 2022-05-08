---
layout: post 
title:  Some Python Collections Library Usage   
date: 2018-07-14 16:20:23 +0900 
category: Python 
tag: Python 
---

## Some usage of Python Collections Library:
* Counter: 
 
```python
from collections import defaultdict, Counter

st = "aaaccvvvvvbbb"
for key, val in dict(Counter(st)).items():
    print(key,val)
```

* defaultdict: 
 
```python
from collections import defaultdict, Counter
d = defaultdict(list) # {key: list}. set, int,float,str etc. values in dict possible
print(d.get(11, -1)) # -1/None/anydefaultvalue for if key not found in d
d[11] = 'Eleven'
print(d.get(11, -1)) 
```