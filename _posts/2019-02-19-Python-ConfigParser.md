---
layout: post
title: Python-ConfigParser
date: 2019-02-19 16:20:23 +0900
category: Python
tag: Python
---
   



<html lang="en">
<title>Python ConfigParser  - working with configuration files in Python with ConfigParser</title>
<head>


</head>

<body>

<header>


</header>

<div class="container">




<div class="content">

<h1>Python ConfigParser</h1>


<p>
<code>ConfigParser</code> is a Python class which implements a basic
configuration language for Python programs. It provides a structure similar to
Microsoft Windows INI files. <code>ConfigParser</code> allows to write Python
programs which can be customized by end users easily.
</p>



<p>
The configuration file consists of sections followed by key/value pairs of options.
The section names are delimited with <code>[]</code> characters. The pairs are separated
either with <code>:</code> or <code>=</code>. Comments start either with <code>#</code>
or with <code>;</code>.
</p>

<h2>Python ConfigParser read file</h2>

<p>
In the first example, we read configuration data from a file.
</p>

<div class="codehead">db.ini</div>
<pre class="code">
[mysql]
host = localhost
user = user7
passwd = s$cret
db = ydb

[postgresql]
host = localhost
user = user8
passwd = mypwd$7
db = testdb
</pre>

<p>
We have two sections of configuration data.
</p>

<div class="codehead">reading_from_file.py</div>
<pre class="code">
#!/usr/bin/env python

import configparser

config = configparser.ConfigParser()
config.read('db.ini')

host = config['mysql']['host']
user = config['mysql']['user']
passwd = config['mysql']['passwd']
db = config['mysql']['db']

print('MySQL configuration:')

print(f'Host: {host}')
print(f'User: {user}')
print(f'Password: {passwd}')
print(f'Database: {db}')

host2 = config['postgresql']['host']
user2 = config['postgresql']['user']
passwd2 = config['postgresql']['passwd']
db2 = config['postgresql']['db']

print('PostgreSQL configuration:')

print(f'Host: {host2}')
print(f'User: {user2}')
print(f'Password: {passwd2}')
print(f'Database: {db2}')
</pre>

<p>
The example reads configuration data for MySQL and PostgreSQL.
</p>

<pre class="explanation">
config = configparser.ConfigParser()
config.read('db.ini')
</pre>

<p>
We initiate the <code>ConfigParser</code> and read the file with <code>read</code>.
</p>

<pre class="explanation">
host = config['mysql']['host']
user = config['mysql']['user']
passwd = config['mysql']['passwd']
db = config['mysql']['db']
</pre>

<p>
We access the options from the mysql section.
</p>

<pre class="explanation">
host2 = config['postgresql']['host']
user2 = config['postgresql']['user']
passwd2 = config['postgresql']['passwd']
db2 = config['postgresql']['db']
</pre>

<p>
We access the options from the postgresql section.
</p>

<pre class="compact">
$ python reading_from_file.py
MySQL configuration:
Host: localhost
User: user7
Password: s$cret
Database: ydb
PostgreSQL configuration:
Host: localhost
User: user8
Password: mypwd$7
Database: testdb
</pre>


<h2>Python ConfigParser sections</h2>

<p>
The configuration data is organized into sections. The <code>sections</code>
reads all sections and the <code>has_section</code> checks if there is the
specified section.
</p>

<div class="codehead">sections.py</div>
<pre class="code">
#!/usr/bin/env python

import configparser

config = configparser.ConfigParser()
config.read('db.ini')

sections = config.sections()
print(f'Sections: {sections}')

sections.append('sqlite')

for section in sections:

    if config.has_section(section):
      print(f'Config file has section {section}')
    else:
      print(f'Config file does not have section {section}')
</pre>

<p>
The example works with sections.
</p>

<pre class="compact">
$ python sections.py
Sections: ['mysql', 'postgresql']
Config file has section mysql
Config file has section postgresql
Config file does not have section sqlite
</pre>




<h2>Python ConfigParser read from string</h2>

<p>
Since Python 3.2, we can read configuration data from a string with the
<code>read_string</code> method.
</p>

<div class="codehead">read_from_string.py</div>
<pre class="code">
#!/usr/bin/env python

import configparser

cfg_data = '''
[mysql]
host = localhost
user = user7
passwd = s$cret
db = ydb
'''

config = configparser.ConfigParser()
config.read_string(cfg_data)

host = config['mysql']['host']
user = config['mysql']['user']
passwd = config['mysql']['passwd']
db = config['mysql']['db']

print(f'Host: {host}')
print(f'User: {user}')
print(f'Password: {passwd}')
print(f'Database: {db}')
</pre>

<p>
The example reads configuration from a string.
</p>

<h2>Python ConfigParser read from dictionary</h2>

<p>
Since Python 3.2, we can read configuration data from a dictionary with
the <code>read_dict</code> method.
</p>

<div class="codehead">read_from_dict.py</div>
<pre class="code">
#!/usr/bin/env python

import configparser

cfg_data = {
    'mysql': {'host': 'localhost', 'user': 'user7',
              'passwd': 's$cret', 'db': 'ydb'}
}

config = configparser.ConfigParser()
config.read_dict(cfg_data)

host = config['mysql']['host']
user = config['mysql']['user']
passwd = config['mysql']['passwd']
db = config['mysql']['db']

print(f'Host: {host}')
print(f'User: {user}')
print(f'Password: {passwd}')
print(f'Database: {db}')
</pre>

<p>
The example reads configuration from a Python dictionary.
</p>

<pre class="explanation">
cfg_data = {
    'mysql': {'host': 'localhost', 'user': 'user7',
                'passwd': 's$cret', 'db': 'ydb'}
}
</pre>

<p>
Keys are section names, values are dictionaries with keys and values that are
present in the section.
</p>

<h2>Python ConfigParser write</h2>

<p>
The <code>write</code> method writes configuration data.
</p>

<div class="codehead">writing.py</div>
<pre class="code">
#!/usr/bin/env python

import configparser

config = configparser.ConfigParser()

config.add_section('mysql')

config['mysql']['host'] = 'localhost'
config['mysql']['user'] = 'user7'
config['mysql']['passwd'] = 's$cret'
config['mysql']['db'] = 'ydb'

with open('db3.ini', 'w') as configfile:
    config.write(configfile)
</pre>

<p>
The example writes config data into the <code>db3.ini</code> file.
</p>

<pre class="explanation">
config.add_section('mysql')
</pre>

<p>
First, we add a section with <code>add_section</code>.
</p>

<pre class="explanation">
config['mysql']['host'] = 'localhost'
config['mysql']['user'] = 'user7'
config['mysql']['passwd'] = 's$cret'
config['mysql']['db'] = 'ydb'
</pre>

<p>
Then we set the options.
</p>

<pre class="explanation">
with open('db3.ini', 'w') as configfile:
    config.write(configfile)
</pre>

<p>
Finally, we write the data with <code>write</code>.
</p>

<h2>Python ConfigParser interpolation</h2>

<p>
<code>ConfigParser</code> allows to use interpolation in the configuration file.
It uses the <code>%</code> syntax.
</p>

<div class="codehead">cfg.ini</div>
<pre class="code">
[info]
users_dir= C:\Users
name= Jano
home_dir= %(users_dir)s\%(name)s
</pre>

<p>
We build the <code>home_dir</code> with interpolation. Note that the 's'
character is part of the syntax.
</p>

<div class="codehead">interpolation.py</div>
<pre class="code">
#!/usr/bin/env python

import configparser

config = configparser.ConfigParser()
config.read('cfg.ini')

users_dir = config['info']['users_dir']
name = config['info']['name']
home_dir = config['info']['home_dir']

print(f'Users directory: {users_dir}')
print(f'Name: {name}')
print(f'Home directory: {home_dir}')
</pre>

<p>
The example reads the values and prints them.
</p>

<pre class="compact">
$ python interpolation.py
Users directory: C:\Users
Name: Jano
Home directory: C:\Users\Jano
</pre> </div></div>






</body>
</html>
