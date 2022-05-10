---
layout: post
title: EASY-> Sort a K-sorted array.
date: 2019-01-04 16:20:23 +0900
category: Algorithm
tag: Algorithm
---

Given a k–sorted array(any element may be misplaced by no more than k positions) from the correct sorted order.

<pre>
For example,

Input:

arr = [1, 4, 5, 2, 3, 7, 8, 6, 10, 9]
k = 2

Output:[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
</pre>



### * Solution Idea:


* Sort by k+1 items window, as any misplacement might occur within this window only.
* K+1 sized min-heap will do the job. ```arr = [already-sorted] <- [on-k+1-min-heap] <- [upcoming-elements].```
* Initially [already-sorted] has no element, for a k+1-min heap from arr[:k+1] elements, ```heapreplace(pop, collect & then push)``` for remaining elements in arr.

<pre>
Time Complexity: O(nlog(k))
Space Complexity: O(k)
</pre>


### * Python Solution:

<pre class="code" style="background-color: rgb(217,238,239,255);">
from heapq import heapreplace, heapify, heappop

def sort_k_sorted_arr(nums, k):
pq = nums[0:k + 1]
heapify (pq)
index = 0
for i in range (k + 1, len (nums)):
nums[index] = heapreplace (pq, nums[i])
index = index + 1

while pq:  # Getting remaining elements from PQ
nums[index] = heappop (pq)
index += 1


if __name__ == '__main__':
nums, k = [1, 4, 5, 2, 3, 7, 8, 6, 10, 9], 2
sort_k_sorted_arr (nums, k)
print (nums)

</pre>
