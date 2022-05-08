---
layout: post
title: Python-Argparse
date: 2019-02-24 16:20:23 +0900
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



<h2>Python Argparse</h2>

<p>
The <code>argparse</code> module makes it easy to write user-friendly
command-line interfaces. It parses the defined arguments from the
<code>sys.argv</code>.
</p>

<p>
The <code>argparse</code> module also automatically generates help and usage
messages, and issues errors when users give the program invalid arguments.
</p>

<p>
The <code>argparse</code> is a standard module; we do not need to install it.
</p>

<p>
A parser is created with <code>ArgumentParser</code> and a new parameter is
added with <code>add_argument</code>. Arguments can be optional, required, or
positional.
</p>

<h2>Python Argparse Optional Argument</h2>

<p>
The following example creates a simple argument parser.
</p>

<div class="codehead">optional_arg.py</div>
<pre class="code">
#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-o', '--output', action='store_true',
help="shows output")

args = parser.parse_args()

if args.output:
print("This is some output")
</pre>

<p>
The example adds one argument having two options: a short <code>-o</code> and
a long <code>--ouput</code>. These are optional arguments.
</p>

<pre class="explanation">
import argparse
</pre>

<p>
The module is imported.
</p>

<pre class="explanation">
parser.add_argument('-o', '--output', action='store_true',
help="shows output")
</pre>

<p>
An argument is added with <code>add_argument</code>. The <code>action</code>
set to <code>store_true</code> will store the argument as <code>True</code>, if present.
The help option gives argument help.
</p>

<pre class="explanation">
args = parser.parse_args()
</pre>

<p>
The arguments are parsed with <code>parse_args</code>. The parsed arguments are
present as object attributes. In our case, there will be
<code>args.output</code> attribute.
</p>

<pre class="explanation">
if args.output:
print("This is some output")
</pre>

<p>
If the argument is present, we show some output.
</p>

<pre class="compact">
$ optional_arg.py -o
This is some output
$ optional_arg.py --output
This is some output
</pre>

<p>
We run the program with the <code>-o</code> and <code>--output</code>.
</p>


$ optional_arg.py --help
usage: optional_arg.py [-h] [-o]

```optional arguments:
-h, --help    show this help message and exit
-o, --output  shows output
</pre>


<p>
We can show the program help.
</p>

<h2>Python Argparse Required Argument</h2>

<p>
An argument is made required with the <code>required</code> option.
</p>

<div class="codehead">required_arg.py</div>
<pre class="code">
#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--name', required=True)

args = parser.parse_args()

print(f'Hello {args.name}')
</pre>

<p>
The example must have the <code>name</code> option specified; otherwise
it fails.
</p>

<pre class="compact">
$ required_arg.py --name Peter
Hello Peter

$ required_arg.py
usage: required_arg.py [-h] --name NAME
required_arg.py: error: the following arguments are required: --name
</pre>


<h2>Python argparse positional arguments</h2>

<p>
The following example works with positional arguments. They
are created with <code>add_argument</code>.
</p>

<div class="codehead">positional_arg.py</div>
<pre class="code">
#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('name')
parser.add_argument('age')

args = parser.parse_args()

print(f'{args.name} is {args.age} years old')
</pre>

<p>
The example expects two positional arguments: name and age.
</p>

<pre class="compact">
parser.add_argument('name')
parser.add_argument('age')
</pre>

<p>
Positional arguments are created without the dash prefix
characters.
</p>

<pre class="compact">
$ positional_arg.py Peter 23
Peter is 23 years old
</pre>

<p>
This is sample output.
</p>

<h2>Python argparse dest</h2>

<p>
The <code>dest</code> option of the <code>add_argument</code> gives
a name to the argument. If not given, it is inferred from the option.
</p>

<div class="codehead">dest.py</div>
<pre class="code">
#!/usr/bin/env python

import argparse
import datetime



parser = argparse.ArgumentParser()

parser.add_argument('-n', dest='now', action='store_true', help="shows now")

args = parser.parse_args()

if args.now:

now = datetime.datetime.now()
print(f"Now: {now}")
</pre>

<p>
The program gives the <code>now</code> name to the <code>-n</code> argument.
</p>

<pre class="compact">
$ dest.py -n
Now: 2019-03-22 17:37:40.406571
</pre>




<h2>Python argparse type</h2>

<p>
The <code>type</code> argument determines the argument type.
</p>

<div class="codehead">rand_int.py</div>
<pre class="code">
#!/usr/bin/env python

import argparse
import random



parser = argparse.ArgumentParser()

parser.add_argument('-n', type=int, required=True,
help="define the number of random integers")
args = parser.parse_args()

n = args.n

for i in range(n):
print(random.randint(-100, 100))
</pre>

<p>
The program shows n random integers from -100 to 100.
</p>

<pre class="explanation">
parser.add_argument('-n', type=int, required=True,
help="define the number of random integers")
</pre>

<p>
The <code>-n</code> option expects integer value and it is
required.
</p>

<pre class="compact">
$ rand_int.py -n 3
92
-61
-61
</pre>

<p>
This is a sample output.
</p>

<h2>Python argparse default</h2>

<p>
The <code>default</code> option specifies the default value,
if the value is not given.
</p>

<div class="codehead">power.py</div>
<pre class="code">
#!/usr/bin/env python

import argparse



parser = argparse.ArgumentParser()

parser.add_argument('-b', type=int, required=True, help="defines the base value")
parser.add_argument('-e', type=int, default=2, help="defines the exponent value")
args = parser.parse_args()

val = 1

base = args.b
exp = args.e

for i in range(exp):
val *= base

print(val)
</pre>

<p>
The example computes exponentiation. The exponent value is not required;
if not given, the default will be 2.
</p>

<pre class="compact">
$ power.py -b 3
9
$ power.py -b 3 -e 3
27
</pre>


<h2>Python argparse metavar</h2>

<p>
The <code>metavar</code> option gives a name to the
expected value in error and help outputs.
</p>

<div class="codehead">metavar.py</div>
<pre class="code">
#!/usr/bin/env python

import argparse



parser = argparse.ArgumentParser()

parser.add_argument('-v', type=int, required=True, metavar='value',
help="computes cube for the given value")
args = parser.parse_args()

print(args)

val = args.v

print(val * val * val)
</pre>

<p>
The example names the expected value <code>value</code>. The default
name is <code>V</code>.
</p>

<pre class="compact">
$ metavar.py -h
usage: metavar.py [-h] -v value

optional arguments:
-h, --help  show this help message and exit
-v value    computes cube for the given value
</pre>

<p>
The given name is shown in the help output.
</p>


<h2>Python argparse append action</h2>

<p>
The <code>append</code> action allows to group repeating
options.
</p>

<div class="codehead">appending.py</div>
<pre class="code">
#!/usr/bin/env python

import argparse


parser = argparse.ArgumentParser()

parser.add_argument('-n', '--name', dest='names', action='append',
help="provides names to greet")

args = parser.parse_args()

names = args.names

for name in names:
print(f'Hello {name}!')
</pre>

<p>
The example produces greeting messages to all names specified with the
<code>n</code> or <code>name</code> options; they can be repeated
multipile times.
</p>

<pre class="compact">
$ appending.py -n Peter -n Lucy --name Jane
Hello Peter!
Hello Lucy!
Hello Jane!
</pre>


<h2>Python argparse nargs</h2>

<p>
The <code>nargs</code> specifies the number of command-line arguments
that should be consumed.
</p>

<div class="codehead">charseq.py</div>
<pre class="code">
#!/usr/bin/env python

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('chars', type=str, nargs=2, metavar='c',
help='starting and ending character')

args = parser.parse_args()

try:
v1 = ord(args.chars[0])
v2 = ord(args.chars[1])

except TypeError as e:

print('Error: arguments must be characters')
parser.print_help()
sys.exit(1)

if v1 > v2:
print('first letter must precede the second in alphabet')
parser.print_help()
sys.exit(1)
</pre>

<p>
The example shows a sequence of characters from character one to
character two. It expects two arguments.
</p>

<pre class="compact">
parser.add_argument('chars', type=str, nargs=2, metavar='c',
help='starting and ending character')
</pre>

<p>
With <code>nargs=2</code> we specify that we expect two arguments.
</p>

<pre class="compact">
$ charseq.py e k
e f g h i j k
</pre>

<p>
The program shows a sequence of characters from e to k.
</p>

<p>
Variable number of arguments can be set with the <code>*</code> character.
</p>

<div class="codehead">var_args.py</div>
<pre class="code">
#!/usr/bin/env python

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('num', type=int, nargs='*')
args = parser.parse_args()

print(f"The sum of values is {sum(args.num)}")
</pre>

<p>
The example computes the sum of values; we can specify
variable number of arguments to the program.
</p>

<pre class="compact">
$ var_args.py 1 2 3 4 5
The sum of values is 15
</pre>


<h2>Python argparse choices</h2>

<p>
The <code>choices</code> option limits arguments
to the given list.
</p>

<div class="codehead">mytime.py</div>
<pre class="code">
#!/usr/bin/env python

import argparse
import datetime
import time


parser = argparse.ArgumentParser()

parser.add_argument('--now', dest='format', choices=['std', 'iso', 'unix', 'tz'],
help="shows datetime in given format")

args = parser.parse_args()
fmt = args.format

if fmt == 'std':
print(datetime.date.today())
elif fmt == 'iso':
print(datetime.datetime.now().isoformat())
elif fmt == 'unix':
print(time.time())
elif fmt == 'tz':
print(datetime.datetime.now(datetime.timezone.utc))
</pre>

<p>
In the example, the <code>now</code> option can accept the following
values: <code>std</code>, <code>iso</code>, <code>unix</code>, or <code>tz</code>.
</p>

<pre class="compact">
$ mytime.py --now iso
2019-03-27T11:34:54.106643

$ mytime.py --now unix
1553682898.422863
</pre>

<p>
This is a sample output.
</p>

<h2>Head example</h2>

<p>
The following example mimics the Linux head command. It shows the n
lines of a text from the beginning of the file.
</p>

<div class="codehead">words.txt</div>
<pre class="code">
sky
top
forest
wood
lake
wood
</pre>

<p>
For the example, we have this small test file.
</p>

<div class="codehead">head.py</div>
<pre class="code">
#!/usr/bin/env python

import argparse
from pathlib import Path


parser = argparse.ArgumentParser()

parser.add_argument('f', type=str, help='file name')
parser.add_argument('n', type=int, help='show n lines from the top')

args = parser.parse_args()

filename = args.f

lines = Path(filename).read_text().splitlines()

for line in lines[:args.n]:
print(line)
</pre>

<p>
The example has two options: <code>f</code> for a file name and
<code>-n</code> for the number of lines to show.
</p>

<pre class="compact">
$ head.py words.txt 3
sky
top
forest
</pre>



</div> <!-- content -->

<div class="rtow">


</div>

</div> <!-- container -->



</body>
</html>

