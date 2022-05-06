---
layout: post
title: Python-Magic-Methods
date: 2019-02-11 16:20:23 +0900
category: Python
tag: Python
---

<html lang="en">
<title>Python Magic Methods</title>
<head>


</head>

<body>

<header>



</header>

<div class="container">


<div class="content">

<h1>Python magic methods</h1>

<p>
Python Magic Methods tutorial describes what Python magic methods are and
shows how to use them. In this tutorial we cover some common magic methods.
</p>


<h2>Python magic methods</h2>

<p>
Python magic methods are special methods that add functionality to our custom
classes. They are surrounded by double underscores (e.g. __add__()).
</p>



<p>
There are many magic methods in Python. Most of them are used for very
specific situations. We will mention some of the more popular methods.
</p>


<h2>The __add__ method</h2>

<p>
The <code>__add__</code> method is used to implement addition operation.
In Python, numbers are not primitive literals but objects. The <code>num + 4</code>
expression is equivalent to <code>num.__add__(4)</code>.
</p>

<div class="codehead">add_dict.py</div>
<pre class="code">
#!/usr/bin/env python


class MyDict(dict):

    def __add__(self, other):

        self.update(other)
        return MyDict(self)


a = MyDict({'de': 'Germany'})
b = MyDict({'sk': 'Slovakia'})

print(a + b)
</pre>

<p>
In the example, we have a custom dictionary that implements the
addition operation with <code>__add__</code>.
</p>

<pre class="explanation">
class MyDict(dict):

def __add__(self, other):

    self.update(other)
    return MyDict(self)
</pre>

<p>
The custom dictionary inherits from the built-in <code>dict</code>.
The <code>__add__</code> method adds two dictionaries with the <code>update</code>
method and returns the newly created dictionary.
</p>

<pre class="explanation">
a = MyDict({'de': 'Germany'})
b = MyDict({'sk': 'Slovakia'})
</pre>

<p>
We create two simple dictionaries.
</p>

<pre class="explanation">
print(a + b)
</pre>

<p>
We add the two dictionaries.
</p>

<pre class="compact">
$ ./add_dict.py
{'de': 'Germany', 'sk': 'Slovakia'}
</pre>


<h2>The __init__ and __str__ methods</h2>

<p>
The <code>__init__</code> method is used to initialize objects. This method is
used to implement the constructor of the object. The
<code>__str__</code> gives a human-readable output of the object.
</p>

<div class="codehead">init_str.py</div>
<pre class="code">
#!/usr/bin/env python


class Person:

    def __init__(self, name, occupation):

        self.name = name
        self.occupation = occupation

    def __str__(self):

        return f'{self.name} is a {self.occupation}'


p = Person('John Doe', 'gardener')
print(p)
</pre>

<p>
In the example, we have a Person class with two attributes: <code>name</code>
and <code>occupation</code>.
</p>

<pre class="explanation">
def __init__(self, name, occupation):

    self.name = name
    self.occupation = occupation
</pre>

<p>
In the <code>__init__</code> method we set the instance variables to the values
that are passed to the constructor.
</p>

<pre class="explanation">
def __str__(self):

    return f'{self.name} is a {self.occupation}'
</pre>

<p>
The <code>__str__</code> method gives a nice short output of the object.
</p>

<pre class="compact">
$ ./init_str.py
John Doe is a gardener
</pre>



<h2>The __repr__ method</h2>

<p>
The <code>__repr__</code> method is called by the built-in function
<code>repr</code>. It is used on the Python shell when it evaluates
an expression that returns an object.
</p>

<p>
The <code>__str__</code> is used to give a human-readable version of
the object and the <code>__repr__</code> a complete representation of
the object. The output of the latter is also more suited for developers.
</p>

<p>
If  <code>__str__</code> implementation is missing then the
<code>__repr__</code> method is used as fallback.
</p>

<pre class="compact">
def __repr__(self):
    return '&lt;{0}.{1} object at {2}&gt;'.format(
      self.__module__, type(self).__name__, hex(id(self)))
</pre>

<p>
The default implementation of the <code>__repr__</code> method 
for an object looks like the above code.
</p>

<div class="codehead">repr_ex.py</div>
<pre class="code">
#!/usr/bin/env python


class Person:

    def __init__(self, name, occupation):
        
        self.name = name
        self.occupation = occupation

    def __str__(self):

        return f'{self.name} is a {self.occupation}'

    def __repr__(self):

        return f'Person{{name: {self.name}, occupation: {self.occupation}}}'


p = Person('John Doe', 'gardener')

print(p)
print(repr(p))
</pre>

<p>
The example implements both the <code>__str__</code> and the 
<code>__repr__</code> methods. 
</p>

<pre class="compact">
$ ./repr_ex.py
John Doe is a gardener
Person{name: John Doe, occupation: gardener}
</pre>



<h2>The __len__ and the __getitem__ methods</h2>

<p>
The <code>__len__</code> method returns the length of the container.
The method is called when we use the built-in <code>len</code> method on the object.
The <code>__getitem__</code> method defines the item access ([]) operator.
</p>

<div class="codehead">french_deck.py</div>
<pre class="code">
#!/usr/bin/env python

import collections
from random import choice


Card = collections.namedtuple('Card', ['suit', 'rank'])


class FrenchDeck:

    ranks = [str(i) for i in range(2, 11)] + list('JQKA')
    suits = ["heart", "clubs", "spades", "diamond"]

    def __init__(self):
        self.total = [Card(suit, rank)
                           for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self.total)

    def __getitem__(self, index):
        return self.total[index]


deck = FrenchDeck()

print(deck[0])
print(len(deck))
print(choice(deck))
</pre>

<p>
The methods are used to implement a french card deck.
</p>

<pre class="explanation">
Card = collections.namedtuple('Card', ['suit', 'rank'])
</pre>

<p>
We use a named tuple to define a <code>Card</code> class. The <code>namedtuple</code>
is a factory function for making a tuple class. Each card has a suit and a rank.
</p>

<pre class="explanation">
def __len__(self):
    return len(self.total)
</pre>

<p>
The <code>__len__</code> method returns the number of cards in the deck (52).
</p>

<pre class="explanation">
def __getitem__(self, index):
    return self.total[index]
</pre>

<p>
The <code>__getitem__</code> implements the indexing operation.
</p>

<pre class="explanation">
print(deck[0])
</pre>

<p>
We get the first card of the deck. This calls the <code>__getitem__</code>.
</p>

<pre class="explanation">
print(len(deck))
</pre>

<p>
This calls the <code>__len__</code> method.
</p>

<pre class="compact">
$ ./french_deck.py
Card(suit='heart', rank='2')
52
Card(suit='diamond', rank='A')
</pre>



<h2>The __int__ and __index__ methods</h2>

<p>
The <code>__int__</code> method is called to implement the built-in
<code>int</code> function. The <code>__index__</code> method implements type
conversion to an int when the object is used in a slice expression and the
built-in <code>hex</code>, <code>oct</code>, and <code>bin</code>
functions.
</p>

<div class="codehead">char_ex.py</div>
<pre class="code">
#!/usr/bin/env python


class Char:

    def __init__(self, val):
        self.val = val

    def __int__(self):
        return ord(self.val)

    def __index__(self):
        return ord(self.val)


c1 = Char('a')

print(int(c1))
print(hex(c1))
print(bin(c1))
print(oct(c1))
</pre>

<p>
In the example we create a custom <code>Char</code> class which implements
the <code>int</code>, <code>hex</code>, <code>bin</code>, and <code>oct</code>
functions.
</p>

<pre class="compact">
./char_ex.py
97
0x61
0b1100001
0o141
</pre>





<h2>The __eq__, __lt__ and __gt__ methods</h2>

<p>
The <code>__eq__</code> implements the <code>==</code> operator.
The <code>__lt__</code> implements the <code>&lt;</code> operator and the 
<code>__gt__</code> implements the <code>&gt;</code> operator.
</p>

<div class="codehead">pouch.py</div>
<pre class="code">
#!/usr/bin/env python

import collections

Coin = collections.namedtuple('coin', ['rank'])

# a gold coin equals to two silver and six bronze coins


class Pouch:

    def __init__(self):
        self.bag = []

    def add(self, coin):

        self.bag.append(coin)

    def __eq__(self, other):

        val1, val2 = self.__evaluate(other)

        if val1 == val2:
            return True
        else:
            return False

    def __lt__(self, other):

        val1, val2 = self.__evaluate(other)

        if val1 &lt; val2:
            return True
        else:
            return False

    def __gt__(self, other):

        val1, val2 = self.__evaluate(other)

        if val1 &gt; val2:
            return True
        else:
            return False

    def __str__(self):

        return str(self.bag)

    def __evaluate(self, other):

        val1 = 0
        val2 = 0

        for coin in self.bag:

            if coin.rank == 'g':
                val1 += 6

            if coin.rank == 's':
                val1 += 3

            if coin.rank == 'b':
                val1 += 1

        for coin in other.bag:

            if coin.rank == 'g':
                val2 += 6

            if coin.rank == 's':
                val2 += 3

            if coin.rank == 'b':
                val2 += 1

        return val1, val2


pouch1 = Pouch()

pouch1.add(Coin('g'))
pouch1.add(Coin('g'))
pouch1.add(Coin('s'))

pouch2 = Pouch()

pouch2.add(Coin('g'))
pouch2.add(Coin('s'))
pouch2.add(Coin('s'))
pouch2.add(Coin('b'))
pouch2.add(Coin('b'))
pouch2.add(Coin('b'))

print(pouch1)
print(pouch2)

if pouch1 == pouch2:
    print('Pouches have equal value')

elif pouch1 &gt; pouch2:
    print('Pouch 1 is more valueable than Pouch 2')
else:
    print('Pouch 2 is more valueable than Pouch 1')
</pre>

<p>
We have a pouch that can contain gold, silver, and bronze 
coins. A gold coin equals to two silver and six bronze coins.
In the example, we implement the three comparison operators
for the pouch object using the Python magic methods.
</p>

<pre class="explanation">
def __eq__(self, other):

    val1, val2 = self.__evaluate(other)

    if val1 == val2:
        return True
    else:
        return False
</pre>

<p>
In the <code>__eq__</code> method, we first evaluate the values of 
the two pouches. Then we compare them and return a boolean result.
</p>

<pre class="explanation">
def __evaluate(self, other):

    val1 = 0
    val2 = 0

    for coin in self.bag:

        if coin.rank == 'g':
            val1 += 6

        if coin.rank == 's':
            val1 += 3

        if coin.rank == 'b':
            val1 += 1

    for coin in other.bag:

        if coin.rank == 'g':
            val2 += 6

        if coin.rank == 's':
            val2 += 3

        if coin.rank == 'b':
            val2 += 1

    return val1, val2
</pre>

<p>
The <code>__evaluate</code> method calculates the values 
of the two pouches. It goes through the coins of the pouch 
and adds a value according to the rank of the coin.
</p>

<pre class="explanation">
pouch1 = Pouch()

pouch1.add(Coin('g'))
pouch1.add(Coin('g'))
pouch1.add(Coin('s'))
</pre>

<p>
We create the first pouch and add three coins to it.
</p>

<pre class="explanation">
if pouch1 == pouch2:
    print('Pouches have equal value')

elif pouch1 &gt; pouch2:
    print('Pouch 1 is more valueable than Pouch 2')
else:
    print('Pouch 2 is more valueable than Pouch 1')
</pre>

<p>
We compare the pouches with the comparison operators.
</p>


<h2>2D vector example</h2>

<p>
In the following example, we introduce a couple of other magic methods,
including <code>__sub__</code>, <code>__mul__</code>, 
and <code>__abs__</code>.
</p>

<div class="codehead">vector.py</div>
<pre class="code">
#!/usr/bin/env python

import math


class Vec2D:

    def __init__(self, x, y):

        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __ne__(self, other):
        return not self.__eq__(other)  


u = Vec2D(0, 1)
v = Vec2D(2, 3)
w = Vec2D(-1, 1)

a = u + v
print(a)

print(a == w)

a = u - v
print(a)

a = u * v

print(a)
print(abs(u))
print(u == v)
print(u != v)
</pre>

<p>
In the example, we have a <code>Vec2D</code> class. We can compare, add,
subtract, and multiply vectors. We can also calculate the lenght of a 
vector.
</p>

<pre class="compact">
$ ./vector.py
(2, 4)
False
(-2, -2)
3
1.0
False 
True
</pre>

</div> <!-- content -->

<div class="rtow">



</div>

</div> <!-- container -->



</body>
</html>
