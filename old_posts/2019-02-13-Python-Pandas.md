---
layout: post
title: Python-Pandas
date: 2019-02-13 16:20:23 +0900
category: Python
tag: Python
---

<head>


</head>

<body>

<header>

</header>

<div class="container">



<div class="content">

<h1>Pandas</h1>


<p>
Basic data analysis in Python with Pandas
library. 
</p>


<h2>Pandas</h2>

<p>
<dfn>Pandas</dfn> is an open source, BSD-licensed library providing
high-performance, easy-to-use data structures and data analysis tools for the
Python programming language.
</p>

<p>
The name of the library comes from the term "panel data", which is an econometrics term
for data sets that include observations over multiple time periods for the
same individuals.
</p>



<p>
It offers data structures and operations for manipulating
numerical tables and time series. The main two data types are: <code>Series</code>
and <code>DataFrame</code>.
</p>

<p>
<code>DataFrame</code> is a two-dimensional size-mutable, potentially
heterogeneous tabular data structure with labeled axes (rows and columns).
It is a spreadsheet-like data structure. <code>Series</code> is a single
column of the <code>DataFrame</code>. A <code>DataFrame</code> can be
thought of as a dictionary of <code>Series</code> objects.
</p>


<h2>Python Pandas installation</h2>

<p>
Pandas is installed with the following command:
</p>

<pre class="compact">
$ pip3 install pandas
</pre>

<p>
We use the <code>pip3</code> command to install <code>pandas</code> module.
</p>

<pre class="compact">
$ pip3 install numpy
</pre>

<p>
Some examples also use <code>numpy</code>.
</p>


<h2>Pandas simple example</h2>

<p>
The following is a simple Pandas example.
</p>

<div class="codehead">simple.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

data = [['Alex', 10], ['Ronald', 18], ['Jane', 33]]
df = pd.DataFrame(data, columns=['Name', 'Age'])

print(df)
</pre>

<p>
In the program, we create a simple <code>DataFrame</code> and
print it to the console.
</p>

<pre class="explanation">
import pandas as pd
</pre>

<p>
We import the Pandas library.
</p>

<pre class="explanation">
data = [['Alex', 10], ['Ronald', 18], ['Jane', 33]]
</pre>

<p>
This is the data to be displayed in the frame. Each nested list is
a row in the table. Note that there are many ways how to initialize
a Pandas <code>DataFrame</code>.
</p>

<pre class="explanation">
df = pd.DataFrame(data, columns=['Name', 'Age'])
</pre>

<p>
A <code>DataFrame</code> is created from the data. We give the frame column
names with <code>columns</code> property.
</p>

<pre class="compact">
$ python simple.py
    Name  Age
0    Alex   10
1  Ronald   18
2    Jane   33
</pre>

<p>
This is the output. The first column are row indexes.
</p>


<h2>Pandas changing index</h2>

<p>
We can update the index so that it does not start from 0.
</p>

<div class="codehead">change_index.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

data = [['Alex', 10], ['Ronald', 18], ['Jane', 33]]
df = pd.DataFrame(data, columns=['Name', 'Age'])
df.index = df.index + 1

print(df)
</pre>

<p>
In the example, we add 1 to the index.
</p>

<pre class="compact">
$ python change_index.py
    Name  Age
1    Alex   10
2  Ronald   18
3    Jane   33
</pre>



<h2>Pandas scalar series</h2>

<p>
The following example creates a series of a scalar value.
</p>

<div class="codehead">series_scalar.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

s = pd.Series(5, index=[0, 1, 2, 3])
print(s)
</pre>

<p>
We have a column containing fives.
</p>

<pre class="compact">
$ python series_scalar.py
0    5
1    5
2    5
3    5
dtype: int64
</pre>

<p>
The left column is the index.
</p>


<h2>Pandas series ndarray</h2>

<p>
We can create a series object from a numpy <code>ndarray </code>.
</p>

<div class="codehead">series_numpy.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd
import numpy as np

data = np.array(['a', 'b', 'c', 'd'])
s = pd.Series(data)

print(s)
</pre>

<p>
The example creates a column of letters from an <code>ndarray</code>.
</p>

<pre class="compact">
$ python series_numpy.py
0    a
1    b
2    c
3    d
dtype: object
</pre>



<h2>Pandas series dict</h2>

<p>
A series can be created from a Python dictionary.
</p>

<div class="codehead">series_dict.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd
import numpy as np

data = {'coins' : 22, 'pens' : 3, 'books' : 28}
s = pd.Series(data)

print(s)
</pre>

<p>
The example creates a series object from a dicionary of items.
</p>

<pre class="compact">
$ python series_dict.py
coins    22
pens      3
books    28
dtype: int64
</pre>

<p>
The index consits of the names of the items.
</p>

<h2>Pandas series retrieve</h2>

<p>
The following example retrieves values form a series object.
</p>

<div class="codehead">series_retrieve.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

s = pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])

print(s[0])
print('-----------------------')

print(s[1:4])
print('-----------------------')

print(s[['a','c','d']])
</pre>

<p>
The example retrieves values from a series object.
</p>

<pre class="explanation">
print(s[0])
</pre>

<p>
Here we get a single value.
</p>

<pre class="explanation">
print(s[1:4])
</pre>

<p>
We retrieve rows by their indexes.
</p>

<pre class="explanation">
print(s[['a','c','d']])
</pre>

<p>
Here we get the values by the index labels.
</p>

<pre class="compact">
$ python series_retrieve.py
1
-----------------------
b    2
c    3
d    4
dtype: int64
-----------------------
a    1
c    3
d    4
dtype: int64
</pre>



<h2>Pandas custom index</h2>

<p>
The index column does not have to be numerical. We can create our own custom
index.
</p>

<div class="codehead">custom_index.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

data = {"country": ["Brazil", "Russia", "India", "China", "South Africa"],
        "capital": ["Brasilia", "Moscow", "New Dehli", "Beijing", "Pretoria"],
        "area": [8.516, 17.10, 3.286, 9.597, 1.221],
        "population": [200.4, 143.5, 1252, 1357, 52.98]}

frame = pd.DataFrame(data)
print(frame)

print('------------------------------')

frame.index = ["BR", "RU", "IN", "CH", "SA"]
print(frame)
</pre>

<p>
In the example, we create a data frame from a data dictionary.
We print the data frame and then we change the index column with
<code>index</code> property.
</p>

<pre class="compact">
$ python custom_index.py
        country    capital    area  population
0        Brazil   Brasilia   8.516      200.40
1        Russia     Moscow  17.100      143.50
2         India  New Dehli   3.286     1252.00
3         China    Beijing   9.597     1357.00
4  South Africa   Pretoria   1.221       52.98
------------------------------
         country    capital    area  population
BR        Brazil   Brasilia   8.516      200.40
RU        Russia     Moscow  17.100      143.50
IN         India  New Dehli   3.286     1252.00
CH         China    Beijing   9.597     1357.00
SA  South Africa   Pretoria   1.221       52.98
</pre>



<h2>Pandas index, columns &amp; values</h2>

<p>
Pandas <code>DataFrame</code> has three basic parts: index, columns, and
values.
</p>

<div class="codehead">index_vals_cols.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

data = [['Alex', 10], ['Ronald', 18], ['Jane', 33]]
df = pd.DataFrame(data, columns=['Name', 'Age'])

print(f'Index: {df.index}')
print(f'Columns: {df.columns}')
print(f'Values: {df.values}')
</pre>

<p>
The example prints the index, columns, and values of a data frame.
</p>

<pre class="compact">
$ python index_vals_cols.py
Index: RangeIndex(start=0, stop=3, step=1)
Columns: Index(['Name', 'Age'], dtype='object')
Values: [['Alex' 10]
    ['Ronald' 18]
    ['Jane' 33]]
</pre>


<h2>Pandas sum and max value</h2>

<p>
The following example calculates the sum and the maximum
of values in a data frame column. It uses also <code>numpy</code>
library.
</p>


<div class="codehead">sum_max.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd
import numpy as np

df = pd.DataFrame(np.arange(0, 1200, 2), columns=['A'])
# df.index = df.index + 1

print(sum(df['A']))
print(max(df['A']))

# print(df)
</pre>

<p>
The example calculates the maximum and the sum of values.
It uses <code>numpy's</code> <code>arange</code> fuction to
generate an array of values.
</p>

<pre class="explanation">
print(sum(df['A']))
</pre>

<p>
When we compute the sum value, we refer to the column by
its name.
</p>

<pre class="compact">
$ sum_max.py
359400
1198
</pre>




<h2>Pandas read CSV</h2>

<p>
Pandas reads data from a CSV file with <code>read_csv</code>.
</p>

<div class="codehead">military_spending.csv</div>
<pre class="code">
Pos, Country, Amount (Bn. $), GDP
1, United States, 610.0, 3.1
2, China, 228.0, 1.9
3, Saudi Arabia, 69.4, 10.0
4, Russia, 66.3, 4.3
5, India, 63.9, 2.5
6, France, 57.8, 2.3
7, United Kingdom, 47.2, 1.8
8, Japan, 45.4, 0.9
9, Germany, 44.3, 1.2
10, South Korea, 39.2, 2.6
11, Brazil, 29.3, 1.4
12, Italy Italy, 29.2, 1.5
13, Australia Australia, 27.5, 2.0
14, Canada Canada, 20.6, 1.3
15, Turkey Turkey, 18.2, 2.2
</pre>

<p>
This is a simple CSV file containing data about military spending
of countries.
</p>

<div class="note">
<strong>Note:</strong> CSV files may have optional column names in the first
row.
</div>

<br>

<div class="codehead">read_from_csv.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

df = pd.read_csv("military_spending.csv")

print(df.to_string(index=False))
</pre>

<p>
The example reads all data from the <code>military_spending.csv</code> file
and prints it in tabular format to the console. It uses <code>read_csv</code> method.
</p>

<pre class="explanation">
print(df.to_string(index=False))
</pre>

<p>
Since we have positions column, we hide the index from the output.
</p>

<pre class="compact">
$ python read_from_csv.py
Pos               Country   Amount (Bn. $)   GDP
  1         United States            610.0   3.1
  2                 China            228.0   1.9
  3          Saudi Arabia             69.4  10.0
  4                Russia             66.3   4.3
  5                 India             63.9   2.5
  6                France             57.8   2.3
  7        United Kingdom             47.2   1.8
  8                 Japan             45.4   0.9
  9               Germany             44.3   1.2
 10           South Korea             39.2   2.6
 11                Brazil             29.3   1.4
 12           Italy Italy             29.2   1.5
 13   Australia Australia             27.5   2.0
 14         Canada Canada             20.6   1.3
 15         Turkey Turkey             18.2   2.2
</pre>


<h2>Pandas write CSV</h2>

<p>
A <code>DataFrame</code> is written to a CSV file with <code>to_csv</code>.
</p>

<div class="codehead">write_csv.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

data = [['Alex', 10], ['Ronald', 18], ['Jane', 33]]
df = pd.DataFrame(data, columns=['Name', 'Age'])

df.to_csv("users.csv", index=False)
</pre>

<p>
The example writes data to the <code>users.csv</code> file.
</p>

<h2>Pandas random rows</h2>

<p>
Random rows from the data frame can be selected with <code>sample</code>.
</p>

<div class="codehead">random_sample.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

df = pd.read_csv("military_spending.csv")

print(df.sample(3))
</pre>

<p>
In the example, we print three random rows from the data frame.
</p>

<h2>Pandas data orientation</h2>

<p>
The <code>to_dict</code> transforms a data frame to a Python dictionary.
The dictionary can be shown in different data outputs.
</p>

<div class="codehead">data_orient.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

data = [['Alex', 10], ['Ronald', 18], ['Jane', 33]]
df = pd.DataFrame(data, columns=['Name', 'Age'])

print('list')
print(df.to_dict(orient='list'))

print('************************************')

print('series')
print(df.to_dict(orient='series'))

print('************************************')

print('dict')
print(df.to_dict(orient='dict'))

print('************************************')

print('split')
print(df.to_dict(orient='split'))

print('************************************')

print('records')
print(df.to_dict(orient='records'))

print('************************************')

print('index')
print(df.to_dict(orient='index'))
</pre>

<p>
The example prints a data frame to the console in six
different formats.
</p>

<h2>Pandas describe</h2>

<p>
The <code>describe</code> method generates descriptive statistics that
summarize the central tendency, dispersion and shape of a dataset's
distribution, excluding <code>NaN</code> values.
</p>

<div class="codehead">describing.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

s1 = pd.Series([1, 2, 3, 4, 5, 6, 7, 8])
s2 = pd.Series([12, 23, 31, 14, 11, 61, 17, 18])

data = {'Vals 1': s1, 'Vals 2': s2}
df = pd.DataFrame(data)

print(df.describe())
</pre>

<p>
The example prints descriptive statistics from a data frame.
</p>

<pre class="compact">
$ python describe.py
        Vals 1     Vals 2
count  8.00000   8.000000
mean   4.50000  23.375000
std    2.44949  16.535136
min    1.00000  11.000000
25%    2.75000  13.500000
50%    4.50000  17.500000
75%    6.25000  25.000000
max    8.00000  61.000000
</pre>


<h2>Pandas counting</h2>

<p>
The next example counts values. You can find the <code>employees.csv</code>
file in the Github repository.
</p>

<div class="codehead">counting.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

df = pd.read_csv("employees.csv")

print(df.count())

print(f'Number of columns: {len(df.columns)}')

print(df.shape)
</pre>

<p>
The <code>count</code> method calculates the number of values
for each column. The number of columns is retrieved with
<code>len(df.columns)</code>. The <code>shape</code> returns a
tuple representing the dimensionality of the data frame.
</p>

<pre class="compact">
$ python counting.py
First Name            933
Gender                855
Start Date           1000
Last Login Time      1000
Salary               1000
Bonus %              1000
Senior Management     933
Team                  957
dtype: int64
Number of columns: 8
(1000, 8)
</pre>

<p>
Note that the columns have different number of values, because some
values are missing.
</p>

<h2>Pandas head and tail</h2>

<p>
With the <code>head</code> and <code>tail</code> methods, we can
display the first and last n rows from the data frame.
</p>

<div class="codehead">head_tail.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

df = pd.read_csv("military_spending.csv")

print(df.head(4))

print('*******************************************')

print(df.tail(4))
</pre>

<p>
The example displays the first and last four rows from the data frame.
</p>

<pre class="compact">
$ python head_tail.py
Pos         Country   Amount (Bn. $)   GDP
0    1   United States            610.0   3.1
1    2           China            228.0   1.9
2    3    Saudi Arabia             69.4  10.0
3    4          Russia             66.3   4.3
*******************************************
 Pos               Country   Amount (Bn. $)   GDP
11   12           Italy Italy             29.2   1.5
12   13   Australia Australia             27.5   2.0
13   14         Canada Canada             20.6   1.3
14   15         Turkey Turkey             18.2   2.2
</pre>


<h2>Pandas no header and index</h2>

<p>
We can hide the header and the index when we display the data frame.
</p>

<div class="codehead">no_header_index.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

df = pd.read_csv("military_spending.csv")

print(df.head(4).to_string(header=False, index=False))
</pre>

<p>
By setting the <code>header</code> and <code>index</code> attributes
to <code>False</code>, we output the data frame without the header and index.
</p>

<pre class="compact">
$ python no_header.py
1   United States  610.0   3.1
2           China  228.0   1.9
3    Saudi Arabia   69.4  10.0
4          Russia   66.3   4.3
</pre>

<p>
This is the output. (The values 1 through 4 are from the pos column.)
</p>

<h2>Pandas loc</h2>

<p>
The <code>loc</code> method allows to access a group of rows and
columns by label(s) or a boolean array.
</p>

<div class="codehead">select_loc.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

data = {'Items': ['coins', 'pens', 'books'], 'Quantity': [22, 28, 3]}

df = pd.DataFrame(data, index=['A', 'B', 'C'])

print(df.loc['A'])

print('-------------------------------')

print(df.loc[['A', 'B'], ['Items']])
</pre>

<p>
The example uses the <code>loc</code> function.
</p>

<pre class="explanation">
print(df.loc['A'])
</pre>

<p>
Here we get the first row. We access the row by its index label.
</p>

<pre class="explanation">
print(df.loc[['A', 'B'], ['Items']])
</pre>

<p>
Here we get the first two rows of the Items column.
</p>

<pre class="compact">
$ python select_loc.py
Items       coins
Quantity       22
Name: A, dtype: object
-------------------------------
    Items
A  coins
B   pens
</pre>


<p>
The second example shows how to select by a boolean array.
</p>

<div class="codehead">select_loc2.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

data = {'Items': ['coins', 'pens', 'books'], 'Quantity': [22, 28, 3]}

df = pd.DataFrame(data, index=['A', 'B', 'C'])

print(df.loc[[True, False, True], ['Items', 'Quantity']])
</pre>

<p>
The example selects rows by a boolean array.
</p>

<pre class="compact">
$ select_loc2.py
    Items  Quantity
 A  coins        22
 C  books         3
</pre>


<p>
In the third example, we apply a condition when selecting.
</p>

<div class="codehead">select_loc3.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

df = pd.read_csv("employees.csv")

data = df.loc[(df['Salary'] &gt; 10000) &amp; (df['Salary'] &lt; 50000)]
print(data.head(5))
</pre>

<p>
The example prints first five rows from the <code>employees.csv</code> file
that match the criteria: the salary is between 10000 and 50000.
</p>

<h2>Pandas iloc</h2>

<p>
The <code>iloc</code> function allows for a integer-location
based indexing for selection by position.
</p>

<div class="codehead">select_iloc.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

df = pd.read_csv("employees.csv")

# integer-location based indexing for selection by position.
# Multiple row and column selections using iloc and DataFrame

print(df.iloc[0:6])  # first six rows of dataframe
print('--------------------------------------')

print(df.iloc[:, 0:2])  # first two columns of data frame with all rows
print('--------------------------------------')

# 1st, 4th, 7th, 25th row + 1st 6th 8th column
print(df.iloc[[0, 3, 6, 24], [0, 5, 7]])
print('--------------------------------------')

# first 5 rows and 5th, 6th, 7th columns of data frame
print(df.iloc[:5, 5:8])
print('--------------------------------------')
</pre>

<p>
The example shows how to select various combinations of rows and columns
with <code>iloc</code>.
</p>

<h2>Pandas sorting</h2>

<p>
The <code>sort_values</code> sorts a series in ascending or descending order.
</p>

<div class="codehead">sorting.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

s1 = pd.Series([2, 1, 4, 5, 3, 8, 7, 6])
s2 = pd.Series([12, 23, 31, 14, 11, 61, 17, 18])

data = {'Col 1': s1, 'Col 2': s2}
df = pd.DataFrame(data)

print(df.sort_values('Col 1', ascending=True))
print('------------------------------------')
print('Sorted')

print(df.sort_values('Col 2', ascending=False))
</pre>

<p>
The example sorts columns in in ascending or descending order.
</p>

<pre class="compact">
$ python sorting.py
    Col 1  Col 2
 1      1     23
 0      2     12
 4      3     11
 2      4     31
 3      5     14
 7      6     18
 6      7     17
 5      8     61
 ------------------------------------
 Sorted
    Col 1  Col 2
 5      8     61
 2      4     31
 1      1     23
 7      6     18
 6      7     17
 3      5     14
 0      2     12
 4      3     11
</pre>


<p>
In the next example, we sort by multiple columns.
</p>

<div class="codehead">sorting2.py</div>
<pre class="code">
#!/usr/bin/env python

import pandas as pd

s1 = pd.Series([1, 2, 1, 2, 2, 1, 2, 2])
s2 = pd.Series(['A', 'A', 'B', 'A', 'C', 'C', 'C', 'B'])

data = {'Col 1': s1, 'Col 2': s2}
df = pd.DataFrame(data)

print(df.sort_values(['Col 1', 'Col 2'], ascending=[True, False]))
</pre>

<p>
The example sorts by the first column containing the integers.
Then the second column is sorted taken the results of the first sort
into account.
</p>

<pre class="compact">
$ python sorting2.py
    Col 1 Col 2
 5      1     C
 2      1     B
 0      1     A
 4      2     C
 6      2     C
 7      2     B
 1      2     A
 3      2     A
</pre>



<!-- eq(), children(), find() -->


</div> <!-- content -->

<div class="rtow">


</div>

</div> <!-- container -->

<footer>



</footer>

</body>
</html>
