---
layout: post
title: Python-Magic-Methods
date: 2019-02-12 16:20:23 +0900
category: Python
tag: Python
---

## Python Magic Methods:

Python magic methods are special methods that add functionality to our custom classes. They are surrounded by double underscores (e.g. __add__()).

There are many magic methods in Python. Most of them are used for very specific situations. We will mention some of the more popular methods.

### The __add__ method:
The __add__ method is used to implement addition operation. In Python, numbers are not primitive literals but objects. The num + 4 expression is equivalent to num.__add__(4).
```python
#!/usr/bin/env python
class MyDict(dict):

    def __add__(self, other):

        self.update(other)
        return MyDict(self)


a = MyDict({'de': 'Germany'})
b = MyDict({'sk': 'Slovakia'})

print(a + b)
```

In the example, we have a custom dictionary that implements the addition operation with __add__.

```python
class MyDict(dict):

def __add__(self, other):

    self.update(other)
    return MyDict(self)
```

The custom dictionary inherits from the built-in dict. The __add__ method adds two dictionaries with the update method and returns the newly created dictionary.
```python
a = MyDict({'de': 'Germany'})
b = MyDict({'sk': 'Slovakia'})
```

We create two simple dictionaries.
```python
print(a + b)
```

We add the two dictionaries.
```shell
$ ./add_dict.py
{'de': 'Germany', 'sk': 'Slovakia'}
```

### The __init__ and __str__ methods:
The __init__ method is used to initialize objects. This method is used to implement the constructor of the object. The __str__ gives a human-readable output of the object.

```python
#!/usr/bin/env python


class Person:

    def __init__(self, name, occupation):

        self.name = name
        self.occupation = occupation

    def __str__(self):

        return f'{self.name} is a {self.occupation}'


p = Person('John Doe', 'gardener')
print(p)
```
In the example, we have a Person class with two attributes: name and occupation.
```python
def __init__(self, name, occupation):

    self.name = name
    self.occupation = occupation
```
In the __init__ method we set the instance variables to the values that are passed to the constructor.
```python
def __str__(self):

    return f'{self.name} is a {self.occupation}'
```

The __str__ method gives a nice short output of the object.
```shell
$ ./init_str.py
John Doe is a gardener
```