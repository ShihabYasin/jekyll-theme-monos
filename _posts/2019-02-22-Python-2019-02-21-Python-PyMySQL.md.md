---
layout: post
title: Python-2019-02-21-Python-PyMySQL.md
date: 2019-02-22 16:20:23 +0900
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

<h1>PyMongo</h1>


<p>
<dfn>MongoDB</dfn> is a NoSQL cross-platform document-oriented database. It is one of the most
popular databases available. MongoDB is developed by MongoDB Inc. and is published as free 
and open-source software.
</p>


<p>
A <dfn>record</dfn> in MongoDB is a document, which is a data structure composed of field and value 
pairs. MongoDB <dfn>documents</dfn> are similar to JSON objects. The values of fields may include 
other documents, arrays, and arrays of documents. MongoDB stores documents in collections. 
<dfn>Collections</dfn> are analogous to tables in relational databases and documents to rows.
</p>

<p>
A <dfn>cursor</dfn> is a reference to the result set of a query. Clients 
can iterate through a cursor to retrieve results. By default, cursors 
timeout after ten minutes of inactivity.
</p>


<h2>PyMongo</h2>

<p>
<dfn>PyMongo</dfn> is a Python module for working with MongoDB in Python.
</p>

<h2>Installing PyMongo</h2>

<p>
The following command is used to install PyMongo.
</p>

<pre class="compact">
$ sudo pip install pymongo
</pre>

<p>
We install PyMongo with <code>pip</code>.
</p>


<h2>Creating a MongoDB database</h2>

<p>
The <code>mongo</code> tool is an interactive JavaScript shell interface to 
MongoDB, which provides an interface for systems administrators as well as 
a way for developers to test queries and operations directly with the database. 
</p>

<pre class="compact">
$ mongo testdb
MongoDB shell version: 2.6.10
connecting to: testdb
&gt; show dbs
admin   (empty)
local   0.078GB
test    0.078GB
testdb  0.078GB
</pre>

<p>
We create a <code>testdb</code> database.
</p>


<h2>PyMongo create collection</h2>

<p>
In the first example, we create a new collection. MongoDB stores 
documents in collections. Collections are analogous to tables in 
relational databases.
</p>

<div class="codehead">create_collection.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient

cars = [ {'name': 'Audi', 'price': 52642},
    {'name': 'Mercedes', 'price': 57127},
    {'name': 'Skoda', 'price': 9000},
    {'name': 'Volvo', 'price': 29000},
    {'name': 'Bentley', 'price': 350000},
    {'name': 'Citroen', 'price': 21000},
    {'name': 'Hummer', 'price': 41400},
    {'name': 'Volkswagen', 'price': 21600} ]

client = MongoClient('mongodb://localhost:27017/')

with client:

    db = client.testdb
    
    db.cars.insert_many(cars)
</pre>

<p>
The example creates a new <code>cars</code> collection. It contains
eight documents.
</p>

<pre class="explanation">
cars = [ {'name': 'Audi', 'price': 52642},
    {'name': 'Mercedes', 'price': 57127},
    {'name': 'Skoda', 'price': 9000},
    {'name': 'Volvo', 'price': 29000},
    {'name': 'Bentley', 'price': 350000},
    {'name': 'Citroen', 'price': 21000},
    {'name': 'Hummer', 'price': 41400},
    {'name': 'Volkswagen', 'price': 21600} ]
</pre>

<p>
This Python dictionary stores eight records to be inserted into 
the MongoDB collection.
</p>

<pre class="explanation">
client = MongoClient('mongodb://localhost:27017/')
</pre>

<p>
<code>MongoClient</code> is used to communicate with MongoDB. We
pass <code>MongoClient</code> a host name and a port number.
</p>

<pre class="explanation">
db = client.testdb
</pre>

<p>
We get a reference to the <code>testdb</code> database.
</p>

<pre class="explanation">
db.cars.insert_many(cars)
</pre>

<p>
With <code>insert_many</code> method, we insert eight documents
into the <code>cars</code> collection, which is automatically created
as well.
</p>

<pre class="compact">
&gt; db.cars.find()
{ "_id" : ObjectId("5b41eb21b9c5d915989d48a8"), "price" : 52642, "name" : "Audi" }
{ "_id" : ObjectId("5b41eb21b9c5d915989d48a9"), "price" : 57127, "name" : "Mercedes" }
{ "_id" : ObjectId("5b41eb21b9c5d915989d48aa"), "price" : 9000, "name" : "Skoda" }
{ "_id" : ObjectId("5b41eb21b9c5d915989d48ab"), "price" : 29000, "name" : "Volvo" }
{ "_id" : ObjectId("5b41eb21b9c5d915989d48ac"), "price" : 350000, "name" : "Bentley" }
{ "_id" : ObjectId("5b41eb21b9c5d915989d48ad"), "price" : 21000, "name" : "Citroen" }
{ "_id" : ObjectId("5b41eb21b9c5d915989d48ae"), "price" : 41400, "name" : "Hummer" }
{ "_id" : ObjectId("5b41eb21b9c5d915989d48af"), "price" : 21600, "name" : "Volkswagen" }
</pre>

<p>
We verify the data with <code>mongo</code> tool.
</p>

<h2>PyMongo list collections</h2>

<p>
With <code>collection_names</code>, we get list available collections
in the database.
</p>

<div class="codehead">list_collections.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

with client:
    
    db = client.testdb
    print(db.collection_names())
</pre>

<p>
The example prints collections in the <code>testdb</code> database.
</p>


<h2>PyMongo drop collection</h2>

<p>
The <code>drop</code> method removes a collection from the database.
</p>

<div class="codehead">drop_collection.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

with client:

    db = client.testdb

    db.cars.drop()
</pre>

<p>
The example removes the <code>cars</code> collection from the <code>testdb</code>
database.
</p>


<h2>PyMongo running commands</h2>

<p>
We can issue commnads to MongoDB with <code>command</code>. The
<code>serverStatus</code> command returns the status of the MongoDB 
server.
</p>

<div class="codehead">server_status.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017/')

with client:
    
    db = client.testdb

    status = db.command("serverStatus")
    pprint(status)
</pre>

<p>
The example prints a lengthy servers status.
</p>

<p>
The <code>dbstats</code> command returns statistics that reflect the 
use state of a single database.
</p>

<div class="codehead">db_stats.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017/')

with client:
    
    db = client.testdb
    print(db.collection_names())

    status = db.command("dbstats")
    pprint(status)
</pre>

<p>
The example prints the database statistics of <code>testdb</code>.
</p>


<h2>PyMongo cursor</h2>

<p>
The find methods return a PyMongo cursor, which is a reference to the 
result set of a query.
</p>

<div class="codehead">cursor.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

with client:
    
    db = client.testdb

    cars = db.cars.find()

    print(cars.next())
    print(cars.next())
    print(cars.next())
    
    cars.rewind()

    print(cars.next())
    print(cars.next())
    print(cars.next())    

    print(list(cars))
</pre>

<p>
In the example, we work with a cursor.
</p>

<pre class="explanation">
cars = db.cars.find()
</pre>

<p>
The <code>find</code> method returns a PyMongo cursor.
</p>

<pre class="explanation">
print(cars.next())
</pre>

<p>
With the <code>next</code> method, we get the next document from 
the result set.
</p>

<pre class="explanation">
cars.rewind()
</pre>

<p>
The <code>rewind</code> method rewinds the cursor to its 
unevaluated state.
</p>

<pre class="explanation">
print(list(cars))
</pre>

<p>
With the <code>list</code> method, we can transform the cursor to 
a Python list. It loads all data into the memory.
</p>

<div class="ad-mid square-fix-ad">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- square-fixed-2020 -->
<ins class="adsbygoogle"
     style="display:inline-block;width:300px;height:250px"
     data-ad-client="ca-pub-9706709751191532"
     data-ad-slot="6775384732"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
</div>


<h2>PyMongo read all data</h2>

<p>
In the following example, we read all records from the collection.
We use Python for loop to traverse the returned cursor.
</p>

<div class="codehead">all_cars.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

with client:

    db = client.testdb

    cars = db.cars.find()

    for car in cars:
        print('{0} {1}'.format(car['name'], 
            car['price']))
</pre>

<p>
The example prints all car names and their prices from the collection.
</p>

<pre class="explanation">
cars = db.cars.find()
</pre>

<p>
The <code>find</code> method selects documents in a collection or 
view and returns a cursor to the selected documents. A cursor is
a reference to the result set of a query. 
</p>

<pre class="explanation">
for car in cars:
    print('{0} {1}'.format(car['name'], 
        car['price']))
</pre>

<p>
With the Python for loop, we iterate over the result set.
</p>

<pre class="compact">
$ ./all_cars.py 
Audi 52642
Mercedes 57127
Skoda 9000
Volvo 29000
Bentley 350000
Citroen 21000
Hummer 41400
Volkswagen 21600
</pre>



<h2>PyMongo count documents</h2>

<p>
The number of documents is retrieved with the <code>count</code> method.
</p>

<div class="codehead">count_cars.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

with client:

    db = client.testdb

    n_cars = db.cars.find().count()

    print("There are {} cars".format(n_cars))
</pre>

<p>
The example counts the number of cars in the collection with 
<code>count</code>.
</p>

<pre class="compact">
$ ./count_cars.py 
There are 8 cars
</pre>

<p>
There are eight cars in the collection.
</p>


<h2>PyMongo filters</h2>

<p>
The first parameter of <code>find</code> and <code>find_one</code>
is a filter. The filter is a condition that all documents must match.
</p>

<div class="codehead">filtering.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

with client:
    
    db = client.testdb

    expensive_cars = db.cars.find({'price': {'$gt': 50000}})

    for ecar in expensive_cars:
        print(ecar['name'])
</pre>

<p>
The example prints the names of cars whose price is greater than 50000. 
</p>

<pre class="explanation">
expensive_cars = db.cars.find({'price': {'$gt': 50000}})
</pre>

<p>
The first parameter of the <code>find</code> method is the filter
that all returned records must match. The filter uses the <code>$gt</code>
operator to return only expensive cars.
</p>

<pre class="compact">
$ ./filtering.py 
Audi
Mercedes
Bentley
</pre>


<h2>PyMongo projections</h2>

<p>
With projections, we can select specific fields from the returned
documents. The projections are passed in the second argument of
the <code>find</code> method.
</p>

<div class="codehead">projection.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

with client:
    
    db = client.testdb

    cars = db.cars.find({}, {'_id': 1, 'name':1})

    for car in cars:
        print(car)
</pre>

<p>
The example prints the <code>_id</code> and <code>name</code> fields of 
the documents. 
</p>

<pre class="explanation">
cars = db.cars.find({}, {'_id': 1, 'name':1})
</pre>

<p>
We can specify either including or excluding projections, not both at
the same time.
</p>

<pre class="compact">
$ ./projection.py 
{'name': 'Audi', '_id': ObjectId('5b41eb21b9c5d915989d48a8')}
{'name': 'Mercedes', '_id': ObjectId('5b41eb21b9c5d915989d48a9')}
{'name': 'Skoda', '_id': ObjectId('5b41eb21b9c5d915989d48aa')}
{'name': 'Volvo', '_id': ObjectId('5b41eb21b9c5d915989d48ab')}
{'name': 'Bentley', '_id': ObjectId('5b41eb21b9c5d915989d48ac')}
{'name': 'Citroen', '_id': ObjectId('5b41eb21b9c5d915989d48ad')}
{'name': 'Hummer', '_id': ObjectId('5b41eb21b9c5d915989d48ae')}
{'name': 'Volkswagen', '_id': ObjectId('5b41eb21b9c5d915989d48af')}
</pre>



<h2>PyMongo sorting documents</h2>

<p>
We can sort documents with <code>sort</code>.
</p>

<div class="codehead">sorting.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient, DESCENDING

client = MongoClient('mongodb://localhost:27017/')

with client:

    db = client.testdb

    cars = db.cars.find().sort("price", DESCENDING)

    for car in cars:
        print('{0} {1}'.format(car['name'], 
            car['price']))
</pre>

<p>
The example sorts records by price in descending order.
</p>

<pre class="compact">
$ ./sorting.py 
Bentley 350000
Mercedes 57127
Audi 52642
Hummer 41400
Volvo 29000
Volkswagen 21600
Citroen 21000
Skoda 9000
</pre>



<h2>PyMongo aggregations</h2>

<p>
Aggregations calculate aggregate values for the data in a collection. 
</p>

<div class="codehead">aggregate_sum.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

with client:
    
    db = client.testdb

    agr = [ {'$group': {'_id': 1, 'all': { '$sum': '$price' } } } ]

    val = list(db.cars.aggregate(agr))

    print('The sum of prices is {}'.format(val[0]['all']))
</pre>

<p>
The example calculates the sum of all car prices.
</p>

<pre class="explanation">
agr = [ {'$group': {'_id': 1, 'all': { '$sum': '$price' } } } ]
</pre>

<p>
The <code>$sum</code> operator calculates and returns the sum of 
numeric values. The <code>$group</code> operator groups input documents 
by a specified identifier expression and applies the accumulator 
expression(s), if specified, to each group. 
</p>

<pre class="explanation">
val = list(db.cars.aggregate(agr))
</pre>

<p>
The <code>aggregate</code> method applies the aggregation operation on 
the <code>cars</code> collection. 
</p>

<pre class="compact">
$ ./aggregate_sum.py 
The sum of prices is 581769
</pre>

<p>
The sum of all values is 581769.
</p>

<p>
We can use the <code>$match</code> operator to select specific cars to 
aggregate. 
</p>

<div class="codehead">sum_two_cars.py</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

with client:
    
    db = client.testdb

    agr = [{ '$match': {'$or': [ { 'name': "Audi" }, { 'name': "Volvo" }] }}, 
        { '$group': {'_id': 1, 'sum2cars': { '$sum': "$price" } }}]

    val = list(db.cars.aggregate(agr))

    print('The sum of prices of two cars is {}'.format(val[0]['sum2cars']))
</pre>

<p>
The example calculates the sum of prices of Audi and Volvo cars. 
</p>

<pre class="explanation">
agr = [{ '$match': {'$or': [ { 'name': "Audi" }, { 'name': "Volvo" }] }}, 
    { '$group': {'_id': 1, 'sum2cars': { '$sum': "$price" } }}]
</pre>

<p>
The expression uses <code>$match</code>, <code>$or</code>, <code>$group</code>,
and <code>$sum</code> operators to do the task.
</p>

<pre class="compact">
$ ./sum_two_cars.py 
The sum of prices of two cars is 81642
</pre>

<p>
The sum of prices of two cars is 81642.
</p>


<h2>PyMongo limit data output</h2>

<p>
The <code>limit</code> query option specifies the number of documents 
to be returned and the <code>skip</code> option some documents.
</p>

<div class="codehead">MongoSkipLimit.java</div>
<pre class="code">
#!/usr/bin/python3

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

with client:
    
    db = client.testdb

    cars = db.cars.find().skip(2).limit(3)

    for car in cars:
        print('{0}: {1}'.format(car['name'], car['price']))
</pre>

<p>
The example reads from the <code>cars</code> collection, skips the first 
two documents, and limits the output to three documents.
</p>

<pre class="explanation">
cars = db.cars.find().skip(2).limit(3)
</pre>

<p>
The <code>skip</code> method skips the first two documents
and the <code>limit</code> method limits the output to three documents. 
</p>

<pre class="compact">
$ ./limit_documents.py 
Skoda: 9000
Volvo: 29000
Bentley: 350000
</pre>

<p>
This is the output of the example.
</p>

<!-- 
TODO modify documents, query operators, projections
authentication
-->



</div> <!-- content -->

<div class="rtow">



</div>

</div> <!-- container -->



</body>
</html>
