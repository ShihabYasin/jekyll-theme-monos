---
layout: post
title: Kudane Algo(DP)-Find maximum contiguous subarray
date: 2018-01-05 16:20:23 +0900
category: Algorithm
tag: Algorithm
---
#### Kadane Algo(DP): find the maximum contiguous subarray



<pre class="code" style="background-color: rgb(217,238,239,255);">
from sys import maxsiz
from typing import List


def kudane(arr: List[int]):
mxsofar, mxendinghere, start, end, skiprun = -maxsize - 1, 0, 0, 0, 0
for i in range (len (arr)):  # from index 0 -> len(arr)
mxendinghere += arr[i]
if mxsofar < mxendinghere:
mxsofar = mxendinghere
start = skiprun
end = i
if mxendinghere < 0:  # for -ve val skip to next val as adding -ve val will not increase mxsofar sum
mxendinghere = 0
skiprun = i + 1
return start, end, mxsofar


a = [-2, -3, 4, -1, -2, 1, 5, -3]
print (kudane (a))
</pre>

