---
layout: post
title: Python-pyDAL
date: 2019-02-20 16:20:23 +0900
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

<h1>pyDAL</h1>

<p>
<em>pyDAL</em> is a pure Python Database Abstraction Layer. The pyDAL
module dynamically generates the SQL in the specified dialect for the
database back end. The resulting code will be portable among
different types of databases.
</p>



<h2>pyDAL installation</h2>

<pre class="compact">
$ sudo pip3 install pyDAL
</pre>

<p>
We use the <code>pip3</code> tool to install pyDAL.
</p>


<h2>pyDAL create database table</h2>

<p>
In the following example, we create a database table.
</p>

<div class="codehead">create_table.py</div>
<pre class="code">
#!/usr/bin/env python

from pydal import DAL, Field

db = DAL('sqlite://test.db', folder='dbs')

try:
db.define_table('cars', Field('name'), Field('price', type='integer'))
db.cars.insert(name='Audi', price=52642)
db.cars.insert(name='Skoda', price=9000)
db.cars.insert(name='Volvo', price=29000)
db.cars.insert(name='Bentley', price=350000)
db.cars.insert(name='Citroen', price=21000)
db.cars.insert(name='Hummer', price=41400)
db.cars.insert(name='Volkswagen', price=21600)

finally:

if db:
db.close()
</pre>

<p>
The example creates a <code>cars</code> table with seven rows.
</p>

<pre class="explanation">
db = DAL('sqlite://test.db', folder='dbs')
</pre>

<p>
<code>DAL</code> represents a database connection. It takes a database
connection string as the first parameter. We connect to an SQLite database.

</p>

<pre class="explanation">
db.define_table('cars', Field('name'), Field('price', type='integer'))
</pre>

<p>
A database table is defined with <code>define_table</code>. It is
created if it does not exist. It has two fields: name and price. An id
field is automatically generated.
</p>

<pre class="explanation">
db.cars.insert(name='Audi', price=52642)
</pre>

<p>
We insert a new row into the table with <code>insert</code>. The method
is called on the <code>cars</code> table of a <code>db</code> connection.
</p>

<pre class="compact">
$ ls dbs
c95cf9bab36fcb04c2424cdf9be0f6e3_cars.table  sql.log  test.db
</pre>

<p>
In addition to the <code>test.db</code> database, we have a migration
file with the <code>.table</code> extension and a log file.
</p>


<h2>pyDAL drop table</h2>

<p>
A database table is removed with <code>drop</code>.
</p>

<div class="codehead">drop_table.py</div>
<pre class="code">
#!/usr/bin/env python

from pydal import DAL, Field

try:

db = DAL('sqlite://test.db', folder='dbs')
cars = db.define_table('cars', Field('name'), Field('price', 'integer'))

cars.drop()

finally:

if db:
db.close()
</pre>

<p>
In the example, we delete the <code>cars</code> table using the <code>drop</code>
method.
</p>


<h2>pyDAL select rows</h2>

<p>
Table rows are selected with <code>select</code>.
</p>

<div class="codehead">select_all_rows.py</div>
<pre class="code">
#!/usr/bin/env python

from pydal import DAL, Field

try:

db = DAL('sqlite://test.db', folder='dbs')
db.define_table('cars', Field('name'), Field('price'))

rows = db().select(db.cars.ALL)

for row in rows:
print("{} {} {}".format(row['id'], row['name'], row['price']))

finally:

if db:
db.close()
</pre>

<p>
In the example, we retrieve all rows from the <code>cars</code> table.
</p>

<pre class="explanation">
rows = db().select(db.cars.ALL)
</pre>

<p>
We fetch all rows with the <code>select</code> method.
The <code>db.cars.ALL</code> tells to select all columns from the table.
</p>

<pre class="explanation">
for row in rows:
print("{} {} {}".format(row['id'], row['name'], row['price']))
</pre>

<p>
We go throught each of the rows and print its fields.
</p>

<pre class="compact">
$ ./select_all_cars.py
1 Audi 52642
2 Skoda 9000
3 Volvo 29000
4 Bentley 350000
5 Citroen 21000
6 Hummer 41400
7 Volkswagen 21600
</pre>



<h2>pyDAL ordering</h2>

<p>
The following example shows how to order data with <code>pyDAL</code>.
</p>

<div class="codehead">order_by.py</div>
<pre class="code">
#!/usr/bin/env python

from pydal import DAL, Field

try:

db = DAL('sqlite://test.db')
db.define_table('cars', Field('name'), Field('price', 'integer'))

rows = db(db.cars).select(orderby=db.cars.price)

for row in rows:
print("{} {} {}".format(row['id'], row['name'], row['price']))

print("**************************************")

rows = db(db.cars).select(orderby=~db.cars.price)

for row in rows:
print("{} {} {}".format(row['id'], row['name'], row['price']))

finally:

if db:
db.close()
</pre>

<p>
The example prints all rows from the table and orders them by price
in ascending and descending order.
</p>

<pre class="explanation">
rows = db(db.cars).select(orderby=db.cars.price)
</pre>

<p>
Ordering is done with the <code>orderby</code> parameter of the
<code>select</code> method.
</p>

<pre class="explanation">
rows = db(db.cars).select(orderby=~db.cars.price)
</pre>

<p>
To order by descending order, we use the tilda character.
</p>

<pre class="compact">
$ ./order_by.py
5 Citroen 21000
7 Volkswagen 21600
3 Volvo 29000
4 Bentley 350000
6 Hummer 41400
1 Audi 52642
2 Skoda 9000
**************************************
2 Skoda 9000
1 Audi 52642
6 Hummer 41400
4 Bentley 350000
3 Volvo 29000
7 Volkswagen 21600
5 Citroen 21000
</pre>






<h2>pyDAL limit data output</h2>

<p>
The data output can be limited with <code>limitby</code> parameter
of the <code>select</code> method.
</p>


<div class="codehead">limit_by.py</div>
<pre class="code">
#!/usr/bin/env python

from pydal import DAL, Field

try:

db = DAL('sqlite://test.db', folder='dbs')
db.define_table('cars', Field('name'), Field('price', 'integer'))

rows = db(db.cars).select(limitby=(2, 5))

for row in rows:
print("{} {} {}".format(row['id'], row['name'], row['price']))


finally:

if db:
db.close()
</pre>

<p>
In the code example, we limit the output to three rows with offset 2.
</p>

<pre class="compact">
$ ./limit_by.py
3 Volvo 29000
4 Bentley 350000
5 Citroen 21000
</pre>




<h2>pyDAL count rows</h2>

<p>
With <code>count</code>, we can get the number of rows in the table.
</p>

<div class="codehead">count_rows.py</div>
<pre class="code">
#!/usr/bin/env python

from pydal import DAL, Field

try:

db = DAL('sqlite://test.db', folder='dbs')
db.define_table('cars', Field('name'), Field('price', 'integer'))

n = db(db.cars.id).count()

print("There are {} rows in the table".format(n))

finally:

if db:
db.close()
</pre>

<p>
In the example, we print the number of rows in the <code>cars</code>
table.
</p>

<pre class="compact">
$ ./count_rows.py
There are 7 rows in the table
</pre>

<p>
We have seven rows in the table.
</p>


<h2>pyDAL JSON output</h2>

<p>
We can get the data in JSON format with <code>as_json</code>.
</p>

<div class="codehead">json_output.py</div>
<pre class="code">
#!/usr/bin/env python

from pydal import DAL, Field

try:

db = DAL('sqlite://test.db', folder='dbs')
db.define_table('cars', Field('name'), Field('price', 'integer'))

rows = db(db.cars).select()
print(rows.as_json())

finally:

if db:
db.close()
</pre>

<p>
The example shows all rows in JSON format.
</p>

<pre class="compact">
$ ./json_output.py
[{"id": 1, "price": 52642, "name": "Audi"},
{"id": 2, "price": 9000, "name": "Skoda"},
{"id": 3, "price": 29000, "name": "Volvo"},
{"id": 4, "price": 350000, "name": "Bentley"},
{"id": 5, "price": 21000, "name": "Citroen"},
{"id": 6, "price": 41400, "name": "Hummer"},
{"id": 7, "price": 21600, "name": "Volkswagen"}]
</pre>



<h2>pyDAL last SQL</h2>

<p>
The SQL that was last executed by pyDAL can be found with
<code>_lastsql</code>.
</p>

<div class="codehead">lastsql.py</div>
<pre class="code">
#!/usr/bin/env python

from pydal import DAL, Field

try:

db = DAL('sqlite://test.db', folder='dbs')
db.define_table('cars', Field('name'), Field('price', 'integer'))

# we ignore the result
db(db.cars.id).select(db.cars.name, db.cars.price)

print(db._lastsql)

finally:

if db:
db.close()
</pre>

<p>
In the example, we print the SQL executed by pyDAL when doing a select
statement.
</p>

<pre class="compact">
$ ./lastsql.py
('SELECT "cars"."name", "cars"."price" FROM "cars" WHERE ("cars"."id" IS NOT NULL);', 0.0005686283111572266)
</pre>

<p>
This SQL was generated by pyDAL.
</p>


<h2>pyDAL execute raw SQL</h2>

<p>
We can execute raw SQL with the <code>executesql</code> method.
</p>

<div class="codehead">raw_sql.py</div>
<pre class="code">
#!/usr/bin/env python

from pydal import DAL, Field

try:

db = DAL('sqlite://test.db', folder='dbs')
db.define_table('cars', Field('name'), Field('price', 'integer'))

data = db.executesql('SELECT * FROM cars WHERE id=6')[0]

print(data)

finally:

if db:
db.close()
</pre>

<p>
In the example, we execute an SQL SELECT statement with <code>executesql</code>.
</p>

<pre class="compact">
$ ./raw_sql.py
(6, 'Hummer', '41400')
</pre>




</div> <!-- content -->

<div class="rtow">


</div>

</div> <!-- container -->


</body>
</html>
