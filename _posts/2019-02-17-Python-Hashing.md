---
layout: post
title: Python-Socket
date: 2019-02-18 16:20:23 +0900
category: Python
tag: Python
---
  

 

<html lang="en">
<title>Python hashing  - explaining hashing in Python</title>
<head>

</head>

<body>

<header>


</header>

<div class="container">



<div class="content">

<h1>Python Hashing</h1>

<p>
Hash tables are used to implement map and set data structures in many common programming
languages, such as C++, Java, and Python. Python uses hash tables for dictionaries and sets.
A <dfn>hash table</dfn> is an unordered collection of key-value pairs, where each key is unique.
Hash tables offer a combination of efficient lookup, insert and delete operations.
These are the best properties of arrays and linked lists.
</p>



<h2>Hashing</h2>

<p>
<dfn>Hashing</dfn> is the process of using an algorithm to map data of any size
to a fixed length. This is called a hash value. Hashing is used to create high
performance, direct access data structures where large amount of
data is to be stored and accessed quickly. Hash values are computed with hash functions.
</p>

<h2>Python hashable</h2>

<p>
An object is hashable if it has a hash value which never changes during its lifetime. (It can
have different values during multiple invocations of Python programs.)
A hashable object needs a <code>__hash__</code> method. In order to perform comparisons, a hashable
needs an <code>__eq__</code>  method.
</p>

<div class="note">
<strong>Note: </strong> Hashable objects which compare equal must have the same hash value.
</div>

<p>
Hashability makes an object usable as a dictionary key and a set member, because
these data structures use the hash value internally. Python immutable built-in
objects are hashable; mutable containers (such as lists or dictionaries) are
not. Objects which are instances of user-defined classes are hashable by
default. They all compare unequal (except with themselves), and their hash value
is derived from their <code>id</code>.
</p>

<div class="note">
<strong>Note: </strong> If a class does not define an <code>__eq__</code> method
it should not define a <code>__hash__</code> operation either; if it defines <code>__eq__</code>
but not <code>__hash__</code>, its instances will not be usable as items in hashable collections.
</div>

<h2>Python hash() function</h2>

<p>
The <code>hash</code> function returns the hash value of the object if it has one.
Hash values are integers. They are used to quickly compare dictionary keys during
a dictionary lookup. Objects can implement the <code>__hash__</code> method.
</p>


<h2>Python immutable builtins are hashable</h2>

<p>
Python immutable builtins, such as integers, strings, or tuples, are hashable.
</p>

<div class="codehead">builtin_hashables.py</div>
<pre class="code">
#!/usr/bin/env python

val = 100

print(val.__hash__())
print("falcon".__hash__())
print((1,).__hash__())
</pre>

<p>
The example prints the values of three hashables: an integer, a string, and a
tuple.
</p>

<h2>Python custom hashable example I</h2>

<p>
Python custom objects are hashable by default. Their hash is
derived from their Id.
</p>

<div class="codehead">custom_object.py</div>
<pre class="code">
#!/usr/bin/env python

class User:

    def __init__(self, name, occupation):

        self.name = name
        self.occupation = occupation

u1 = User('John Doe', 'gardener')
u2 = User('John Doe', 'gardener')

print('hash of user 1')
print(hash(u1))

print('hash of user 2')
print(hash(u2))

if (u1 == u2):
    print('same user')
else:
    print('different users')
</pre>

<p>
In the example, we have two instances of a <code>User</code>.
</p>

<pre class="explanation">
u1 = User('John Doe', 'gardener')
u2 = User('John Doe', 'gardener')
</pre>

<p>
We have two instances with the same data.
</p>

<pre class="explanation">
print('hash of user 1')
print(hash(u1))
</pre>

<p>
The <code>hash</code> function returns the hash value of the
object. The default implementation is derived from the Id of the object.
</p>

<pre class="compact">
$ python custom_object.py
hash of user 1
-9223371894419573195
hash of user 2
142435202673
different users
</pre>

<p>
Even though the user details are the same, the comparison yields differet objects.
In order to change it, we need to implement the <code>__eq__</code> method.
</p>


<h2>Python custom hashable example II</h2>

<p>
In the second example, we implement a custom <code>__eq__</code> method.
</p>

<div class="codehead">custom_object2.py</div>
<pre class="code">
#!/usr/bin/env python

class User:

    def __init__(self, name, occupation):

        self.name = name
        self.occupation = occupation

    def __eq__(self, other):

        return self.name == other.name \
            and self.occupation == other.occupation

    def __str__(self):
        return f'{self.name} {self.occupation}'


u1 = User('John Doe', 'gardener')
u2 = User('John Doe', 'gardener')

if (u1 == u2):
    print('same user')
    print(f'{u1} == {u2}')
else:
    print('different users')

users = {u1, u2}
print(len(users))
</pre>

<p>
Now the comparison returns the expected output for us; however, we cannot
insert the objects into a Python set; it would result in
<code>TypeError: unhashable type: 'User'</code>. In order to change this,
we implement the <code>__hash__</code> method.
</p>

<h2>Python custom hashable example III</h2>

<p>
In the third example, we implement the <code>__eq__</code> and
the <code>__hash__</code> methods.
</p>

<div class="codehead">custom_object3.py</div>
<pre class="code">
#!/usr/bin/env python

class User:

    def __init__(self, name, occupation):

        self.name = name
        self.occupation = occupation

    def __eq__(self, other):

        return self.name == other.name \
            and self.occupation == other.occupation

    def __hash__(self):
        return hash((self.name, self.occupation))

    def __str__(self):
        return f'{self.name} {self.occupation}'


u1 = User('John Doe', 'gardener')
u2 = User('John Doe', 'gardener')

users = {u1, u2}

print(len(users))

if (u1 == u2):
    print('same user')
    print(f'{u1} == {u2}')
else:
    print('different users')

print('------------------------------------')

u1.occupation = 'programmer'

users = {u1, u2}

print(len(users))

if (u1 == u2):
    print('same user')
    print(f'{u1} == {u2}')
else:
    print('different users')
</pre>

<p>
The example compares two objects that have custom implementation
of the <code>__eq__</code> and <code>__hash__</code> methods.
The objects can be inserted into a Python set and when an attribute is later
changed, we get the expected output.
</p>

<pre class="explanation">
def __hash__(self):
    return hash((self.name, self.occupation))
</pre>

<p>
The implementation of the <code>__hash__</code> function returns a hash 
value computed with the <code>hash</code> function from a tuple of attributes.
</p>

<pre class="compact">
$ python custom_object3.py
1
same user
John Doe gardener == John Doe gardener
------------------------------------
2
different users
</pre>


<!--
<h2>Python custom hashable example IV</h2>

<p>
In the fourth example, we add a mutable object to our custom class.
This results in un unexpected output.
</p>

<div class="note">
<strong>Note:</strong> If a class defines mutable objects and implements an
<code>__eq__</code> method, it should not implement <code>__hash__</code>, since the
implementation of hashable collections requires that a key’s hash value is
immutable.
</div>

<br>

<div class="codehead">custom_object4.py</div>
<pre class="code">
#!/usr/bin/env python

class User:

    def __init__(self, name, occupation, colours):

        self.name = name
        self.occupation = occupation
        self.colours = colours

    def __eq__(self, other):

        return self.name == other.name \
            and self.occupation == other.occupation

    def __hash__(self):
        return hash((self.name, self.occupation))

    def __str__(self):
        return f'{self.name} {self.occupation} {self.colours}'


u1 = User('John Doe', 'gardener', ['steelblue', 'green', 'red'])
u2 = User('John Doe', 'gardener', ['steelblue', 'green', 'red'])

s1 = {u1, u2}
print(len(s1))

if (u1 == u2):
    print('same user')
    print(f'{u1} == {u2}')
else:
    print('different users')

print('-----------------------')

u1.colours[1] = 'blue'

s2 = {u1, u2}
print(len(s2))

if (u1 == u2):
    print('same user')
    print(f'{u1} == {u2}')
else:
    print('different users')
</pre>

<p>
In the example, we have a list as an attribute. A list is a mutable object and
it has consequences for the hashing algorithm.
</p>

<pre class="explanation">
u1.colours[1] = 'blue'
</pre>

<p>
We change an element of a list of the first user. However, this is not
reflected.
</p>

<pre class="compact">
$ custom_object4.py
1
same user
John Doe gardener ['steelblue', 'green', 'red'] == John Doe gardener ['steelblue', 'green', 'red']
-----------------------
1
same user
John Doe gardener ['steelblue', 'blue', 'red'] == John Doe gardener ['steelblue', 'green', 'red']
</pre>

<p>
The output still says that the objects are equal.
</p> -->

<h2>Python @dataclass decorator</h2>

<p>
Since Python 3.7, we have the <code>dataclass</code> decorator, which
automatically generates some boilerplate code.
</p>

<p>
The dataclass decorator has a frozen argument (<code>False</code> by default).
If specified, the fields will be frozen (i.e. read-only). If
<code>eq</code> is set to <code>True</code>, which it is by default then the
<code>__hash__</code> method is implemented and object instances will be
hashable.
</p>

<div class="codehead">decorator.py</div>
<pre class="code">
#!/usr/bin/env python

from dataclasses import dataclass

@dataclass(frozen=True)
class User:

    name: str
    occupation: str


u1 = User('John Doe', 'gardener')
u2 = User('John Doe', 'gardener')

if (u1 == u2):
    print('same user')
    print(f'{u1} == {u2}')
else:
    print('different users')

users = {u1, u2}
print(len(users))
</pre>

<p>
The example uses the <code>@dataclass</code> decorator.
</p>

<pre class="compact">
$ python decorator.py
same user
User(name='John Doe', occupation='gardener') == User(name='John Doe', occupation='gardener')
1
</pre>


</div> <!-- content -->

<div class="rtow">





</div>

</div> <!-- container -->

<footer>

</footer>

</body>
</html>
