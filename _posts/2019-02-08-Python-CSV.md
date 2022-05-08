---
layout: post
title: Python-CSV
date: 2019-02-08 16:20:23 +0900
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

<div class="ltow">



<div class="content">

<h1>Python CSV  - read write </h1>



<h2>CSV</h2>

<p>
<dfn>CSV (Comma Separated Values)</dfn> is a very popular import
and export data format used in spreadsheets and databases. Each line in a
CSV file is a data record. Each record consists of one or more fields,
separated by commas. While CSV is a very simple data format,
there can be many differences, such as different delimiters,
new lines, or quoting characters.
</p>

<h2>Python csv module</h2>

<p>
The <code>csv</code> module implements classes to read and write tabular data in CSV format.
The <code>csv</code> module's <code>reader</code> and <code>writer</code> objects read and
write sequences. Programmers can also read and write data in dictionary form using the
<code>DictReader</code> and <code>DictWriter</code> classes.
</p>



<h2>Python CSV methods</h2>

<p>
The following table shows Python csv methods:
</p>

<table>
<thead>
<tr><th>Method</th><th>Description</th></tr>
</thead>

<tbody>
<tr><td>csv.reader</td><td>returns a reader object which iterates over lines of a CSV file</td></tr>
<tr><td>csv.writer</td><td>returns a writer object which writes data into CSV file</td></tr>
<tr><td>csv.register_dialect</td><td>registers a CSV dialect</td></tr>
<tr><td>csv.unregister_dialect</td><td>unregisters a CSV dialect</td></tr>
<tr><td>csv.get_dialect</td><td>returns a dialect with the given name</td></tr>
<tr><td>csv.list_dialects</td><td>returns all registered dialects</td></tr>
<tr><td>csv.field_size_limit</td><td>returns the current maximum field size allowed by the parser</td></tr>
</tbody>

</table>


<h2>Using Python csv module</h2>

<pre class="compact">
import csv
</pre>

<p>
To use Python CSV module, we import <code>csv</code>.
</p>

<h2>Python CSV reader</h2>

<p>
The <code>csv.reader</code> method returns a reader object which iterates
over lines in the given CSV file.
</p>

<pre class="compact">
$ cat numbers.csv
16,6,4,12,81,6,71,6
</pre>

<p>
The <code>numbers.csv</code> file contains numbers.
</p>

<div class="codehead">read_csv.py</div>
<pre class="code">
#!/usr/bin/python3

import csv

f = open('numbers.csv', 'r')

with f:

reader = csv.reader(f)

for row in reader:
for e in row:
print(e)

</pre>

<p>
In the code example, we open the <code>numbers.csv</code> for reading
and read its contents.
</p>

<pre class="explanation">
reader = csv.reader(f)
</pre>

<p>
We get the <code>reader</code> object.
</p>

<pre class="explanation">
for row in reader:
for e in row:
print(e)
</pre>

<p>
With two for loops, we iterate over the data.
</p>

<pre class="compact">
$ ./read_csv.py
16
6
4
12
81
6
71
6
</pre>

<p>
This is the output of the example.
</p>



<h2>Python CSV reader with different delimiter</h2>

<p>
The <code>csv.reader</code> method allows to use a different
delimiter with its <code>delimiter</code> attribute.
</p>


<pre class="compact">
$ cat items.csv
pen|cup|bottle
chair|book|tablet
</pre>

<p>
The <code>items.csv</code> contains values separated with '|' character.
</p>

<div class="codehead">read_csv.py</div>
<pre class="code">
#!/usr/bin/python3

import csv

f = open('items.csv', 'r')

with f:

reader = csv.reader(f, delimiter="|")

for row in reader:

for e in row:
print(e)

</pre>

<p>
The code example reads and displays data from a CSV file that
uses a '|' delimiter.
</p>

<pre class="compact">
$ ./read_csv2.py
pen
cup
bottle
chair
book
tablet
</pre>

<p>
This is the output of the example.
</p>


<h2>Python CSV DictReader</h2>

<p>
The <code>csv.DictReader</code> class operates like a regular reader
but maps the information read into a dictionary. The keys for the dictionary
can be passed in with the <code>fieldnames</code> parameter or inferred from
the first row of the CSV file.
</p>

<pre class="compact">
$ cat values.csv
min,avg,max
1, 5.5, 10
2, 3.5, 5
</pre>

<p>
The first line of the file consists of dictionary keys.
</p>

<div class="codehead">read_csv_dictionary.py</div>
<pre class="code">
#!/usr/bin/python3

# read_csv3.py

import csv

f = open('values.csv', 'r')

with f:

reader = csv.DictReader(f)

for row in reader:
print(row['min'], row['avg'], row['max'])

</pre>

<p>
The example reads the values from the <code>values.csv</code> file
using the <code>csv.DictReader</code>.
</p>

<pre class="explanation">
for row in reader:
print(row['min'], row['avg'], row['max'] )
</pre>

<p>
The row is a Python dictionary and we reference the data
with the keys.
</p>


<h2>Python CSV writer</h2>

<p>
The <code>csv.writer</code> method returns a writer object which
converts the user's data into delimited strings on the given file-like object.
</p>

<div class="codehead">write_csv.py</div>
<pre class="code">
#!/usr/bin/python3

import csv

nms = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]

f = open('numbers2.csv', 'w')

with f:

writer = csv.writer(f)

for row in nms:
writer.writerow(row)

</pre>

<p>
The script writes numbers into the <code>numbers2.csv</code> file.
The <code>writerow</code> method writes a row of data into the
specified file.
</p>

<pre class="compact">
$ cat numbers2.csv
1,2,3,4,5,6
7,8,9,10,11,12
</pre>

<p>
It is possible to write all data in one shot. The <code>writerows</code>
method writes all given rows to the CSV file.
</p>

<div class="codehead">write_csv2.py</div>
<pre class="code">
#!/usr/bin/python3

import csv

nms = [[1, 2, 3], [7, 8, 9], [10, 11, 12]]

f = open('numbers3.csv', 'w')

with f:

writer = csv.writer(f)
writer.writerows(nms)

</pre>

<p>
The code example writes three rows of numbers into the file
using the <code>writerows</code> method.
</p>


<h2>Python CSV DictWriter</h2>

<p>
The <code>csv.DictWriter</code> class operates like a regular writer
but maps Python dictionaries into CSV rows. The <code>fieldnames</code> parameter
is a sequence of keys that identify the order in which values in
the dictionary passed to the <code>writerow</code> method are written to the CSV
file.
</p>

<div class="codehead">write_csv_dictionary.py</div>
<pre class="code">
#!/usr/bin/python3

import csv

f = open('names.csv', 'w')

with f:

fnames = ['first_name', 'last_name']
writer = csv.DictWriter(f, fieldnames=fnames)

writer.writeheader()
writer.writerow({'first_name' : 'John', 'last_name': 'Smith'})
writer.writerow({'first_name' : 'Robert', 'last_name': 'Brown'})
writer.writerow({'first_name' : 'Julia', 'last_name': 'Griffin'})

</pre>

<p>
The example writes the values from Python dictionaries into the CSV file
using the <code>csv.DictWriter</code>.
</p>

<pre class="explanation">
writer = csv.DictWriter(f, fieldnames=fnames)
</pre>

<p>
New <code>csv.DictWriter</code> is created. The header names are passed
to the <code>fieldnames</code> parameter.
</p>

<pre class="explanation">
writer.writeheader()
</pre>

<p>
The <code>writeheader</code> method writes the headers to the CSV file.
</p>

<pre class="explanation">
writer.writerow({'first_name' : 'John', 'last_name': 'Smith'})
</pre>

<p>
The Python dictionary is written to a row in a CSV file.
</p>

<pre class="compact">
$ cat names.csv
first_name,last_name
John,Smith
Robert,Brown
Julia,Griffin
</pre>



<h2>Python CSV custom dialect</h2>

<p>
A custom dialect is created with the <code>csv.register_dialect</code>
method.
</p>

<div class="codehead">custom_dialect.py</div>
<pre class="code">
#!/usr/bin/python3

import csv

csv.register_dialect("hashes", delimiter="#")

f = open('items3.csv', 'w')

with f:

writer = csv.writer(f, dialect="hashes")
writer.writerow(("pens", 4))
writer.writerow(("plates", 2))
writer.writerow(("bottles", 4))
writer.writerow(("cups", 1))

</pre>

<p>
The program uses a (#) character as a delimiter. The dialect
is specified with the <code>dialect</code> option in
the <code>csv.writer</code> method.
</p>

<pre class="compact">
$ cat items3.csv
pens#4
plates#2
bottles#4
cups#1
</pre>



</div> <!-- content -->

<div class="rtow">




</div>

</div>
</div>


</body>
</html>


