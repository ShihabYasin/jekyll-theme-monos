---
layout: post
title: Python-BeautifulSoup
date: 2019-02-07 16:20:23 +0900
category: Python
tag: Python
---

## BeautifulSoup transforms a complex HTML document into a complex tree of Python objects, such as tag, navigable string, or comment.
* Install using pip```sudo pip3 install lxml bs4```.


### Let's consider a dummy HTML Example file:
```html
<!DOCTYPE html>
<html>
<head>
<title>Header</title>
<meta charset="utf-8">
</head>

<body>
<h2>Operating systems</h2>

<ul id="mylist" style="width:150px">
<li>Solaris</li>
<li>FreeBSD</li>
<li>Debian</li>
<li>NetBSD</li>
<li>Windows</li>
</ul>

<p>
FreeBSD is an advanced computer operating system used to
power modern servers, desktops, and embedded platforms.
</p>

<p>
Debian is a Unix-like computer operating system that is
composed entirely of free software.
</p>

</body>
</html>
</pre>

### 1. Get tags:
<pre class="code" style="background-color: rgb(217,238,239,255);">
#!/usr/bin/python

from bs4 import BeautifulSoup

with open('index.html', 'r') as f:

contents = f.read()

soup = BeautifulSoup(contents, 'lxml')

print(soup.h2)
print(soup.head)
print(soup.li)
</pre>
### 2. Get  tags, name, text:
<pre class="code" style="background-color: rgb(217,238,239,255);">
#!/usr/bin/python

from bs4 import BeautifulSoup

with open('index.html', 'r') as f:

contents = f.read()

soup = BeautifulSoup(contents, 'lxml')

print(f'HTML: {soup.h2}, name: {soup.h2.name}, text: {soup.h2.text}')
</pre>
### 3. Traverse Tags:
<pre class="code" style="background-color: rgb(217,238,239,255);">
#!/usr/bin/python

from bs4 import BeautifulSoup

with open('index.html', 'r') as f:

contents = f.read()

soup = BeautifulSoup(contents, 'lxml')

for child in soup.recursiveChildGenerator():

if child.name:

print(child.name)
</pre>
### 4. Getting DOM Child:
<pre class="code" style="background-color: rgb(217,238,239,255);">
#!/usr/bin/python

from bs4 import BeautifulSoup

with open('index.html', 'r') as f:

contents = f.read()

soup = BeautifulSoup(contents, 'lxml')

root = soup.html

root_childs = [e.name for e in root.children if e.name is not None]
print(root_childs)

</pre>


### 5. Get all descendants:
<pre class="code" style="background-color: rgb(217,238,239,255);">
#!/usr/bin/python

from bs4 import BeautifulSoup

with open('index.html', 'r') as f:

contents = f.read()

soup = BeautifulSoup(contents, 'lxml')

root = soup.body

root_childs = [e.name for e in root.descendants if e.name is not None]
print(root_childs)
</pre>
### 6. Find elements by Id
<pre class="code" style="background-color: rgb(217,238,239,255);">
#!/usr/bin/python

from bs4 import BeautifulSoup

with open('index.html', 'r') as f:

contents = f.read()

soup = BeautifulSoup(contents, 'lxml')

#print(soup.find('ul', attrs={ 'id' : 'mylist'}))
print(soup.find('ul', id='mylist'))
</pre>
### 7. Get all tags:
<pre class="code" style="background-color: rgb(217,238,239,255);">
#!/usr/bin/python

from bs4 import BeautifulSoup

with open('index.html', 'r') as f:

contents = f.read()

soup = BeautifulSoup(contents, 'lxml')

for tag in soup.find_all('li'):
print(f'{tag.name}: {tag.text}')
</pre>
### 8.  CSS selectors:
<pre class="code" style="background-color: rgb(217,238,239,255);">
#!/usr/bin/python

from bs4 import BeautifulSoup

with open('index.html', 'r') as f:

contents = f.read()

soup = BeautifulSoup(contents, 'lxml')

print(soup.select('li:nth-of-type(3)'))
</pre>
