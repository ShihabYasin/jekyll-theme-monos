---
layout: post
title: Python-Builtins
date: 2019-02-12 16:20:23 +0900
category: Python
tag: Python
---

<html lang="en">

<head>


</head>

<body>

<header>


</header>

<div class="container">


<div class="content">

<h1>Python any &amp; all builtins</h1>




<h2>Python any</h2>

<p>
The <code>any</code> builtin function returns <code>True</code> if any element
of the iterable is true. If the iterable is empty, it returns
<code>False</code>.
</p>

<pre class="compact">
def any(it):
  for el in it:
      if el:
          return True
  return False
</pre>

<p>
The <code>any</code> is equivalent to the above code.
</p>


<pre class="compact">
vals = [False, False, True, False, False]

if any(vals):
    print('There is a truthy value in the list')
else:
    print('There is no truthy value in the list')
</pre>

<p>
With the <code>any</code> function, we check if there is any truthy
value in the list.
</p>


<h2>Python any practical example</h2>

<p>
Our next goal is to find out if there are some users older than the
specified age.
</p>

<div class="codehead">users_age.py</div>
<pre class="code">
#!/usr/bin/env python

from datetime import datetime, date
from dateutil.relativedelta import relativedelta


users = [
  {'name': 'John Doe', 'date_of_birth': '1987-11-08', 'active': True},
  {'name': 'Jane Doe', 'date_of_birth': '1996-02-03', 'active': True},
  {'name': 'Robert Brown', 'date_of_birth': '1977-12-12', 'active': True},
  {'name': 'Lucia Smith', 'date_of_birth': '2002-11-17', 'active': False},
  {'name': 'Patrick Dempsey', 'date_of_birth': '1994-01-04', 'active': True}
]

user_dts = [datetime.strptime(user['date_of_birth'], "%Y-%m-%d") for user in users]

val = 40
today = datetime.now()
data = [relativedelta(today, dt).years &gt; val for dt in user_dts]

if any(data):
    print(f'There are users older than {val}')
else:
    print(f'There are no users older than {val}')
</pre>

<p>
We have a list of users. Each user is represented as a dictionary. One of the keys of
the dictionary is the date of birth.
</p>

<pre class="explanation">
user_dts = [datetime.strptime(user['date_of_birth'], "%Y-%m-%d") for user in users]
</pre>

<p>
With a Python list comprehension, we create a list of user datetime objects. With the
<code>strptime</code> function, we transform the <code>date_of_birth</code> string values
into <code>datetime</code> objects.
</p>

<pre class="explanation">
val = 40
</pre>

<p>
We want to find out if there is any user older than forty.
</p>

<pre class="explanation">
today = datetime.now()
</pre>

<p>
We get the current date and time.
</p>

<pre class="explanation">
data = [relativedelta(today, dt).years &gt; val for dt in user_dts]
</pre>

<p>
With another list comprehension, we create a list of boolean values. The
<code>relativedelta</code> function calculates the years between the current
datetime and the user's birthday datetime. If the difference in years is greater
than the given value (40), the expression returns True; False otherwise.
</p>

<pre class="explanation">
if any(data):
    print(f'There are users older than {val}')
else:
    print(f'There are no users older than {val}')
</pre>

<p>
We pass the created list of boolean values to the <code>any</code> function.
</p>

<pre class="compact">
$ ./users_age.py
There are users older than 40
</pre>

<p>
There is at least one user older than forty.
</p>


<h2>Python all</h2>

<p>
The <code>all</code> builtin function returns <code>True</code>
if all elements of the iterable are true (or if the iterable is empty).
</p>

<pre class="compact">
def all(it):
    for el in it:
        if not el:
            return False
    return True
</pre>

<p>
The <code>all</code> is equivalent to the above code.
</p>


<pre class="compact">
vals = [True, False, True, True, True]

if all(vals):
    print('All values are truthy')
else:
    print('All values are not thruthy')
</pre>

<p>
With the <code>all</code> function, we check if all values are truthy.
</p>


<h2>Python all practical example</h2>

<p>
We want to find out if all users are active.
</p>

<div class="codehead">users_active.py</div>
<pre class="code">
#!/usr/bin/env python


users = [
  {'name': 'John Doe', 'occupation': 'gardener', 'active': True},
  {'name': 'Jane Doe', 'occupation': 'teacher', 'active': True},
  {'name': 'Robert Brown', 'occupation': 'driver', 'active': True},
  {'name': 'Lucia Smith', 'occupation': 'hair dresser', 'active': False},
  {'name': 'Patrick Dempsey', 'occupation': 'programmer', 'active': True}
]


if all([user['active'] for user in users]):
    print('All users are active')
else:
    print('There are inactive users')
</pre>

<p>
We have a list of users. The users have the <code>active</code> property.
</p>

<pre class="explanation">
if all([user['active'] for user in users]):
    print('All users are active')
else:
    print('There are inactive users')
</pre>

<p>
With the <code>all</code> function we check, if all users are active.
</p>

<pre class="compact">
$ ./users_active.py
There are inactive users
</pre>






</div> <!-- content -->

<div class="rtow">





</div>

</div> <!-- container -->



</body>
</html>
