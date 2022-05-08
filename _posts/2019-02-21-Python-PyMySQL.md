---
layout: post
title: Python-PyMySQL
date: 2019-02-21 16:20:23 +0900
category: Python
tag: Python
---



<!DOCTYPE html>
<html lang="en">

<head>

</head>

<body>

<header>

</header>

<div class="container">


<div class="content">

<h1>PyMySQL</h1>

<p>
<em>PyMySQL</em> is a pure-Python MySQL client library, based on PEP 249. Most
public APIs are compatible with mysqlclient and MySQLdb. PyMySQL works with
MySQL 5.5+ and MariaDB 5.5+.
</p>



<p>
MySQL is a leading open source database management system. It is a
multiuser, multithreaded database management system. MySQL is especially
popular on the web.
</p>

<div class="codehead">cities_mysql.sql</div>
<pre class="code">
USE testdb;
DROP TABLE IF EXISTS cities;
CREATE TABLE cities(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), population INT);
INSERT INTO cities(name, population) VALUES('Bratislava', 432000);
INSERT INTO cities(name, population) VALUES('Budapest', 1759000);
INSERT INTO cities(name, population) VALUES('Prague', 1280000);
INSERT INTO cities(name, population) VALUES('Warsaw', 1748000);
INSERT INTO cities(name, population) VALUES('Los Angeles', 3971000);
INSERT INTO cities(name, population) VALUES('New York', 8550000);
INSERT INTO cities(name, population) VALUES('Edinburgh', 464000);
INSERT INTO cities(name, population) VALUES('Berlin', 3671000);
</pre>

<p>
In the tutorial, we use the <code>cities</code> table.
</p>


<h2>PyMySQL installation</h2>

<pre class="compact">
$ sudo pip3 install pymysql
</pre>

<p>
We use the <code>pip3</code> tool to install PyMySQL.
</p>


<h2>PyMySQL version example</h2>

<p>
In the following example, we get the version of MySQL.
</p>

<div class="codehead">version.py</div>
<pre class="code">
#!/usr/bin/python

import pymysql

con = pymysql.connect('localhost', 'user7',
's$cret', 'testdb')

try:

with con.cursor() as cur:

cur.execute('SELECT VERSION()')

version = cur.fetchone()

print(f'Database version: {version[0]}')

finally:

con.close()
</pre>

<p>
In MySQL, we can use <code>SELECT VERSION</code> to get the version of MySQL.
</p>

<pre class="explanation">
import pymysql
</pre>

<p>
We import the <code>pymysql</code> module.
</p>

<pre class="explanation">
con = pymysql.connect('localhost', 'user7',
's$cret', 'testdb')
</pre>

<p>
We connect to the database with <code>connect</code>. We pass four parameters:
the hostname, the MySQL user name, the password, and the database name.
</p>

<pre class="explanation">
with con.cursor() as cur:
</pre>

<p>
Using the <code>with</code> keyword, the Python interpreter automatically
releases the resources. It also provides error handling. We get a cursor
object, which is used to traverse records from the result set.
</p>

<pre class="explanation">
cur.execute('SELECT VERSION()')
</pre>

<p>
We call the <code>execute</code> function of the cursor and execute the SQL
statement.
</p>

<pre class="explanation">
version = cur.fetchone()
</pre>

<p>
The <code>fetchone</code> function fetches the next row of a query
result set, returning a single sequence, or <code>None</code> when no
more data is available.
</p>

<pre class="explanation">
print(f'Database version: {version[0]}')
</pre>

<p>
We print the version of the database.
</p>

<pre class="explanation">
finally:

con.close()
</pre>

<p>
The <code>pymysql</code> module does not implement the automatic handling of the
connection resource; we need to explicitly close the connection with
<code>close</code> in the finally clause.
</p>

<pre class="compact">
$ ./version.py
Database version: 10.3.23-MariaDB-1
</pre>


<h2>PyMySQL fetchAll</h2>

<p>
The <code>fetchAll</code> method retrieves all (remaining) rows of a query
result, returning them as a sequence of sequences.
</p>

<div class="codehead">fetch_all.py</div>
<pre class="code">
#!/usr/bin/python

import pymysql

con = pymysql.connect('localhost', 'user7',
's$cret', 'testdb')

try:

with con.cursor() as cur:

cur.execute('SELECT * FROM cities')

rows = cur.fetchall()

for row in rows:
print(f'{row[0]} {row[1]} {row[2]}')

finally:

con.close()
</pre>

<p>
In the example, we retrieve all cities from the database table.
</p>

<pre class="explanation">
cur.execute('SELECT * FROM cities')
</pre>

<p>
This SQL statement selects all data from the cities table.
</p>

<pre class="explanation">
rows = cur.fetchall()
</pre>

<p>
The <code>fetchall</code> function gets all records. It returns a result set.
Technically, it is a tuple of tuples. Each of the inner tuples represent a row
in the table.
</p>

<pre class="explanation">
for row in rows:
print(f'{row[0]} {row[1]} {row[2]}')
</pre>

<p>
We print the data to the console, row by row.
</p>

<pre class="compact">
$ ./fetch_all.py
1 Bratislava 432000
2 Budapest 1759000
3 Prague 1280000
4 Warsaw 1748000
5 Los Angeles 3971000
6 New York 8550000
7 Edinburgh 464000
8 Berlin 3671000
</pre>




<h2>PyMySQL dictionary cursor</h2>

<p>
The default cursor returns the data in a tuple of tuples. When we use a
dictionary cursor, the data is sent in a form of Python dictionaries. This way
we can refer to the data by their column names.
</p>


<div class="codehead">dictionary_cursor.py</div>
<pre class="code">
#!/usr/bin/python

import pymysql
import pymysql.cursors

con = pymysql.connect(host='localhost',
user='user7',
password='s$cret',
db='testdb',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)

try:

with con.cursor() as cur:

cur.execute('SELECT * FROM cities')

rows = cur.fetchall()

for row in rows:
print(row['id'], row['name'])

finally:

con.close()
</pre>

<p>
In this example, we get the first rows of the cities table using the dictionary
cursor.
</p>

<pre class="explanation">
con = pymysql.connect(host='localhost',
user='user7',
password='s$cret',
db='testdb',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)
</pre>

<p>
In the <code>connect</code> function, we pass the
<code>pymysql.cursors.DictCursor</code> value to the <code>cursorclass</code>
parameter.
</p>

<pre class="explanation">
for row in rows:
print(row['id'], row['name'])
</pre>

<p>
We refer to the data by column names of the cities table.
</p>


<h2>PyMySQL column headers</h2>

<p>
Next we will show how to print column headers with the data from the database
table.
</p>

<div class="codehead">column_headers.py</div>
<pre class="code">
#!/usr/bin/python

import pymysql

con = pymysql.connect('localhost', 'user7',
's$cret', 'testdb')

try:

with con.cursor() as cur:

cur.execute('SELECT * FROM cities')

rows = cur.fetchall()

desc = cur.description

print(f'{desc[0][0]:&lt;8} {desc[1][0]:&lt;15} {desc[2][0]:&gt;10}')

for row in rows:
print(f'{row[0]:&lt;8} {row[1]:&lt;15} {row[2]:&gt;10}')

finally:

con.close()
</pre>

<p>
The column names are considered to be the metadata. They are obtained from the
cursor object.
</p>

<pre class="explanation">
desc = cur.description
</pre>

<p>
The <code>description</code> attribute of the cursor returns information about
each of the result columns of a query.
</p>

<pre class="explanation">
print(f'{desc[0][0]:&lt;8} {desc[1][0]:&lt;15} {desc[2][0]:&gt;10}')
</pre>

<p>
Here we print and format the table column names.
</p>

<pre class="explanation">
for row in rows:
print(f'{row[0]:&lt;8} {row[1]:&lt;15} {row[2]:&gt;10}')
</pre>

<p>
We traverse and print the data.
</p>

<pre class="compact">
$ ./column_headers.py
id       name            population
1        Bratislava          432000
2        Budapest           1759000
3        Prague             1280000
4        Warsaw             1748000
5        Los Angeles        3971000
6        New York           8550000
7        Edinburgh           464000
8        Berlin             3671000
</pre>


<h2>PyMySQL escaping parameters</h2>

<p>
The parameters passed to the <code>execute</code> method are escaped for
security reasons; this is to prevent SQL injection attacks.
</p>

<div class="codehead">escaped.py</div>
<pre class="code">
#!/usr/bin/python

import pymysql

con = pymysql.connect('localhost', 'user7',
's$cret', 'testdb')

# user input
myid = 4

try:

with con.cursor() as cur:


cur.execute('SELECT * FROM cities WHERE id=%s', myid)

cid, name, population  = cur.fetchone()
print(cid, name, population)

finally:

con.close()
</pre>

<p>
In the example, we get the row with the specified Id.
</p>

<pre class="explanation">
cur.execute('SELECT * FROM cities WHERE id=%s', myid)
</pre>

<p>
We use a placeholder identified by the <code>%s</code> marker.
Before the SQL statement is executed, the values are bound to their
placeholders.
</p>

<pre class="compact">
$ ./escaped.py
4 Warsaw 1748000
</pre>



<h2>PyMySQL affected rows</h2>

<p>
The <code>rowcount</code> is a read-only cursor attribute which specifies the
number of rows that was produced by the the last  SELECT, UPDATE, or
INSERT statement.
</p>

<div class="codehead">affected_rows.py</div>
<pre class="code">
#!/usr/bin/python

import pymysql

con = pymysql.connect('localhost', 'user7',
's$cret', 'testdb')

try:

with con.cursor() as cur:

cur.execute('SELECT * FROM cities WHERE id IN (1, 2, 3)')

print(f'The query affected {cur.rowcount} rows')

finally:

con.close()
</pre>

<p>
In the example, we have a SELECT statement that selects three rows.
</p>

<pre class="explanation">
print(f'The query affected {cur.rowcount} rows')
</pre>

<p>
We build a message that shows the number of affected rows.
</p>

<pre class="compact">
$ ./affected_rows.py
The query affected 3 rows
</pre>


<h2>PyMySQL insert row</h2>

<p>
A new row is inserted with the <code>INSERT INTO</code> SQL statement.
</p>

<div class="codehead">insert_row.py</div>
<pre class="code">
#!/usr/bin/python

import pymysql

con = pymysql.connect('localhost', 'user7',
's$cret', 'testdb')

city = (9, 'Kiev', 2887000)

try:

with con.cursor() as cur:

cur.execute('INSERT INTO cities VALUES(%s, %s, %s)',
(city[0], city[1], city[2]))
con.commit()

print('new city inserted')

finally:

con.close()
</pre>

<p>
In the example, we insert a new city into the table.
</p>

<pre class="explanation">
cur.execute('INSERT INTO cities VALUES(%s, %s, %s)',
(city[0], city[1], city[2]))
con.commit()
</pre>

<p>
In <code>pymysql</code>, the autocommit is off by default. We need to call
<code>commit</code> to execute the changes.
</p>



</div> <!-- content -->

<div class="rtow">

<!-- container -->



</body>
</html>
