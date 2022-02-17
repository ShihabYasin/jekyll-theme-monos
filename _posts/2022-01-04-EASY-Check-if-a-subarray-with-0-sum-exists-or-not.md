---
layout: post 
title: Given an integer array, check if it contains a subarray (contiguous elements) whose sum is 0.
date: 2022-01-04 16:20:23 +0900 
category: Algorithm
tag: Algorithm
---

> Example: <br>
> Input:  { 3, 4, -7, 3, 1, 3, 1, -4, -2, -2 } <br> 
> Output: True  <br> 
> The subarrays with a sum of 0 are: <br> 
> { 3, 4, -7 } <br> 
> { 4, -7, 3 } etc. <br> 
> 
> Input:  { 3, 4, 2, 6, -2 } <br> 
> Output: False  <br> 




### * Solution Idea: 


Let a series, [some x ints] , 1 , (-2) , 2 , (-1) , [other y ints]. 1,-2, 2,-1 sums to 0. Let, SUM([some x ints]) = x0. <br> 
> x0 + 1 = x1</n> <br> 
> x1 + (-2) = x2 <br> 
> x2 + 2 = x3 <br> 
> x3 + (-1) = x4 <br> 
> ------------------------ <br> 
> x0 + x1 + x2 + x3 =  x1 + x2 + x3 + x4  <br> 
> or x0 = x4 <br> 


It seems after summing up to ([some x ints] , 1 , (-2) , 2 , (-1)) sum returns to x0 ( where x0 = SUM([some x ints])). <br> 
If no 0-sum subarray exist, x0 = x4 this condition can never be hold. This condition only holds if at least one 0-sum subarray exists. <br> 
 <br> 
Time Complexity: O(n) <br> 
Space Complexity: O(n) <br> 


### * Python Solution:
```python
from typing import List


def hasZeroSumSubarray(numsL: List[int]):
    prevSums = {0}  # if array contains a 0
    totalSum = 0
    for i in nums:
        totalSum += i
        if totalSum in prevSums:
            return True
        prevSums.add (totalSum)
    return False


if __name__ == '__main__':
    nums = [4, 6, 3, -1, 2, -4, 89, 4, 2, 7, 1, 1]
    # nums = [4, 6, 37, 1, 1]
    print (hasZeroSumSubarray (nums))

```
