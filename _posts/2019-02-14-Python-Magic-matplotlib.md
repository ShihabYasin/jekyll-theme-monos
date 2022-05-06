---
layout: post
title: Python-matplotlib
date: 2019-02-14 16:20:23 +0900
category: Python
tag: Python
---

<html lang="en">
<title>Python Matplotlib  - creating charts in Python with Matplotlib</title>
<head>


</head>

<body>

<header>

</header>


<div class="container">


<div class="content">

<h1>Python Matplotlib</h1>


<p>
Create different charts in Python with Matplotlib.
</p>



<h2>Matplotlib</h2>

<p>
<em>Matplotlib</em> is a Python library for creating charts. Matplotlib can be
used in Python scripts, the Python and IPython shell, the jupyter notebook, web
application servers, and four graphical user interface toolkits.
</p>



<h2>Matplotlib Installation</h2>

<p>
Matplotlib is an external Python library that needs to be installed.
</p>

<pre class="compact">
$ sudo pip install matplotlib
</pre>

<p>
We can use the <code>pip</code> tool to install the library.
</p>


<h2>Matplotlib scatter chart</h2>

<p>
A <em>scatter chart</em> is a type of plot or mathematical diagram using Cartesian coordinates 
to display values for typically two variables for a set of data.
</p>

<div class="codehead">scatter.py</div>
<pre class="code">
#!/usr/bin/python3

import matplotlib.pyplot as plt

x_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y_axis = [5, 16, 34, 56, 32, 56, 32, 12, 76, 89]

plt.title("Prices over 10 years")
plt.scatter(x_axis, y_axis, color='darkblue', marker='x', label="item 1")

plt.xlabel("Time (years)")
plt.ylabel("Price (dollars)")

plt.grid(True)
plt.legend()

plt.show()
</pre>

<p>
The example draws a scatter chart. The chart displays the prices of some item
over the period of ten years.
</p>

<pre class="explanation">
import matplotlib.pyplot as plt
</pre>

<p>
We import the <code>pyplot</code> from the <code>matplotlib</code> module.
It is a collection of command style functions that create charts. It is similar
in operation to MATLAB.
</p>

<pre class="explanation">
x_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y_axis = [5, 16, 34, 56, 32, 56, 32, 12, 76, 89]
</pre>

<p>
We have data for x and y axes.
</p>

<pre class="explanation">
plt.title("Prices over 10 years")
</pre>

<p>
With the <code>title</code> function, we set a title for the chart.
</p>

<pre class="explanation">
plt.scatter(x_axis, y_axis, color='darkblue', marker='x', label="item 1")
</pre>

<p>
The <code>scatter</code> function draws the scatter chart. It accepts 
the data for the x and y axes, the color of the marker, the shape of the 
marker, and the label.
</p>

<pre class="explanation">
plt.xlabel("Time (years)")
plt.ylabel("Price (dollars)")
</pre>

<p>
We set the labels for the axes. 
</p>

<pre class="explanation">
plt.grid(True)
</pre>

<p>
We show the grid with the <code>grid</code> function. The grid consists of
a number of vertical and horizontal lines.
</p>

<pre class="explanation">
plt.legend()
</pre>

<p>
The <code>legend</code> function places a legend on the axes.
</p>

<pre class="explanation">
plt.show()
</pre>

<p>
The <code>show</code> function displays the chart.
</p>




<h2>Mathplotlib two datasets</h2>

<p>
In the next example, we add another data set to the chart.
</p>

<div class="codehead">scatter2.py</div>
<pre class="code">
#!/usr/bin/python3

import matplotlib.pyplot as plt

x_axis1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y_axis1 = [5, 16, 34, 56, 32, 56, 32, 12, 76, 89]

x_axis2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y_axis2 = [53, 6, 46, 36, 15, 64, 73, 25, 82, 9] 

plt.title("Prices over 10 years")

plt.scatter(x_axis1, y_axis1, color='darkblue', marker='x', label="item 1")
plt.scatter(x_axis2, y_axis2, color='darkred', marker='x', label="item 2")

plt.xlabel("Time (years)")
plt.ylabel("Price (dollars)")

plt.grid(True)
plt.legend()

plt.show()
</pre>

<p>
The chart displays two data sets. We distinguish between them by the colour of 
the marker. 
</p>

<pre class="explanation">
x_axis1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y_axis1 = [5, 16, 34, 56, 32, 56, 32, 12, 76, 89]

x_axis2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y_axis2 = [53, 6, 46, 36, 15, 64, 73, 25, 82, 9] 
</pre>

<p>
We have two data sets.
</p>

<pre class="explanation">
plt.scatter(x_axis1, y_axis1, color='darkblue', marker='x', label="item 1")
plt.scatter(x_axis2, y_axis2, color='darkred', marker='x', label="item 2")
</pre>

<p>
We call the <code>scatter</code> function for each of the sets.
</p>




<h2>Matplotlib line chart</h2>

<p>
A <em>line chart</em> is a type of chart which displays information as a series
of data points called <em>markers</em> connected by straight line segments.
</p>

<div class="codehead">linechart.py</div>
<pre class="code">
#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0.0, 3.0, 0.01)
s = np.sin(2.5 * np.pi * t)
plt.plot(t, s)
 
plt.xlabel('time (s)')
plt.ylabel('voltage (mV)')

plt.title('Sine Wave')
plt.grid(True)

plt.show()
</pre>

<p>
The example displays a sine wave line chart.
</p>

<pre class="explanation">
import numpy as np
</pre>

<p>
In the example, we also need the <code>numpy</code> module.
</p>

<pre class="explanation">
t = np.arange(0.0, 3.0, 0.01)
</pre>

<p>
The <code>arange</code> function returns an evenly spaced list
of values within the given interval.
</p>

<pre class="explanation">
s = np.sin(2.5 * np.pi * t)
</pre>

<p>
We get the <code>sin</code> values of the data.
</p>

<pre class="explanation">
plt.plot(t, s)
</pre>

<p>
We draw the line chart with the <code>plot</code> function.
</p>


<h2>Matplotlib bar chart</h2>

<p>
A <em>bar chart</em> presents grouped data with rectangular bars with lengths proportional 
to the values that they represent. The bars can be plotted vertically or horizontally.
</p>

<div class="codehead">barchart.py</div>
<pre class="code">
#!/usr/bin/python3

from matplotlib import pyplot as plt
from matplotlib import style

style.use('ggplot')

x = [0, 1, 2, 3, 4, 5]
y = [46, 38, 29, 22, 13, 11]

fig, ax = plt.subplots()

ax.bar(x, y, align='center')

ax.set_title('Olympic Gold medals in London')
ax.set_ylabel('Gold medals')
ax.set_xlabel('Countries')

ax.set_xticks(x)
ax.set_xticklabels(("USA", "China", "UK", "Russia", 
    "South Korea", "Germany"))

plt.show()
</pre>

<p>
The example draws a bar chart. It shows the number of Olympic gold medals 
per country in London 2012.
</p>

<pre class="explanation">
style.use('ggplot')
</pre>

<p>
It is possible to use predefined styles.
</p>

<pre class="explanation">
fig, ax = plt.subplots()
</pre>

<p>
The <code>subplots</code> function returns a figure and an axes object.
</p>

<pre class="explanation">
ax.bar(x, y, align='center')
</pre>

<p>
A bar chart is generated with the <code>bar</code> function.
</p>

<pre class="explanation">
ax.set_xticks(x)
ax.set_xticklabels(("USA", "China", "UK", "Russia", 
    "South Korea", "Germany"))
</pre>

<p>
We set the country names for the x axis.
</p>


<h2>Matplotlib pie chart</h2>

<p>
A <em>pie chart</em> is a circular chart which is divided into slices 
to illustrate numerical proportion.
</p>

<div class="codehead">piechart.py</div>
<pre class="code">
#!/usr/bin/python3

import matplotlib.pyplot as plt
 
labels = ['Oranges', 'Pears', 'Plums', 'Blueberries']
quantity = [38, 45, 24, 10]

colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

plt.pie(quantity, labels=labels, colors=colors, autopct='%1.1f%%', 
    shadow=True, startangle=90)

plt.axis('equal')

plt.show()
</pre>

<p>
The example creates a pie chart.
</p>

<pre class="explanation">
labels = ['Oranges', 'Pears', 'Plums', 'Blueberries']
quantity = [38, 45, 24, 10]
</pre>

<p>
We have labels and corresponding quantities.
</p>

<pre class="explanation">
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
</pre>

<p>
We define colours for the pie chart's slices.
</p>

<pre class="explanation">
plt.pie(quantity, labels=labels, colors=colors, autopct='%1.1f%%', 
    shadow=True, startangle=90)
</pre>

<p>
The pie chart is generated with the <code>pie</code> function. The <code>autopct</code>
is responsible for displaying percentages in the chart's wedges.
</p>

<pre class="explanation">
plt.axis('equal')
</pre>

<p>
We set an equal aspect ratio so that the pie is drawn as a circle.
</p>







</div> <!-- content -->

<div class="rtow">





</div>

</div> <!-- container -->



</body>
</html>
