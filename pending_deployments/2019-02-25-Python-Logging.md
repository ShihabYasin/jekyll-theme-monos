---
layout: post
title: Python-Logging
date: 2019-02-25 16:20:23 +0900
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

<h1>Python Logging</h1>

<p>
<dfn>Logging</dfn> is the process of writing information into log files. Log files
contain information about various events that happened in operating system, software, or
in communication.
</p>




<h2>Purpose of logging</h2>

<p>
Logging is done for the following purposes:
</p>

<ul>
<li>Information gathering</li>
<li>Troubleshooting</li>
<li>Generating statistics</li>
<li>Auditing</li>
<li>Profiling</li>
</ul>

<p>
Logging is not limited to identifying errors in software development. It is also used
in detecting security incidents, monitoring policy violations, providing information in case
of problems, finding application bottlenecks, or generating usage data.
</p>


<h2>Which events to log</h2>

<p>
Events that should be logged include input validation failures, authentication and authorization
failures, application errors, configuration changes, and application start-ups and shut-downs.
</p>

<h2>Which events not to log</h2>

<p>
Events that should not be logged include application source code, session identification values,
access tokens, sensitive personal data, passwords, database connection strings, encryption keys,
bank account and card holder data.
</p>


<h2>Logging best practices</h2>

<p>
The following are some best practices for doing logging:
</p>

<ul>
<li>Logging should be meaningful.</li>
<li>Logging should contain context.</li>
<li>Logging should structured and done at different levels.</li>
<li>Logging should be balanced; it should not include too little or too much information.</li>
<li>Logging messages should be understandable to humans and parseable by machines.</li>
<li>Logging in more complex applications should be done into several log files.</li>
<li>Logging should be adapted to development and to production.</li>
</ul>


<h2>The logging module</h2>

<p>
Python <dfn>logging</dfn> module defines functions and classes which
implement a flexible event logging system for applications and libraries.
</p>


<h2>The logging module components</h2>

<p>
The logging module has four main components: loggers, handlers, filters,
and formatters. Loggers expose the interface that application code directly uses.
Handlers send the log records (created by loggers) to the appropriate destination.
Filters provide a finer grained facility for determining which log records to output.
Formatters specify the layout of log records in the final output.
</p>

<h2>Python logging hierarchy</h2>

<p>
Python loggers form a hierarchy. A logger named <code>main</code> is a parent
of <code>main.new</code>.
</p>

<p>
Child loggers propagate messages up to the handlers associated with
their ancestor loggers. Because of this, it is unnecessary to define and
configure handlers for all the loggers in the application. It is
sufficient to configure handlers for a top-level logger and create child
loggers as needed.
</p>

<h2>Python logging levels</h2>

<p>
Levels are used for identifying the severity of an event. There are six
logging levels:
</p>

<ul>
    <li>CRITICAL</li>
    <li>ERROR</li>
    <li>WARNING</li>
    <li>INFO</li>
    <li>DEBUG</li>
    <li>NOTSET</li>
</ul>

<p>
If the logging level is set to <code>WARNING</code>, all <code>WARNING</code>,
<code>ERROR</code>, and <code>CRITICAL</code> messages are written to the log file
or console. If it is set to <code>ERROR</code>, only <code>ERROR</code> and
<code>CRITICAL</code> messages are logged.
</p>

<p>
Loggers have a concept of <em>effective level</em>. If a level is not explicitly
set on a logger, the level of its parent is used instead as its
effective level. If the parent has no explicit level set, its parent is
examined, and so on - all ancestors are searched until an explicitly set
level is found.
</p>

<p>
When the logger is created with <code>getLogger</code>, the level is set to
<code>NOTSET</code>. If the logging level is not set explicitly with <code>setLevel</code>,
the messages are propagated to the logger parents. The logger's chain of ancestor loggers
is traversed until either an ancestor with a level other than <code>NOTSET</code> is found,
or the root is reached. The root logger has a default <code>WARNING</code> level set.
</p>

<h2>Root logger</h2>

<p>
All loggers are descendants of the root logger. Each logger passes log messages
on to its parent. New loggers are created with the <code>getLogger(name)</code>
method. Calling the function  without a name (<code>getLogger</code>) returns
the root logger.
</p>

<p>
The root logger always has an explicit level set, which is <code>WARNING</code>
by default.
</p>

<p>
The root looger sits at the top of the hierarchy and is always present, even if
not configured. In general, the program or library should not log directly
against the root logger. Instead a specific logger for the program should be
configured. Root logger can be used to easily turn all loggers from all
libraries on and off.
</p>

<h2>Python logging simple example</h2>

<p>
The <code>logging</code> module has simple methods that can be used right
away without any configuration. This can be used for simple logging.
</p>

<div class="codehead">simple.py</div>
<pre class="code">
#!/usr/bin/env python

import logging

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
</pre>

<p>
The example calls five methods of the <code>logging</code> module.
The messages are written to the console.
</p>

<pre class="compact">
$ simple.py
WARNING:root:This is a warning message
ERROR:root:This is an error message
CRITICAL:root:This is a critical message
</pre>

<p>
Notice that root logger is used and only three messages were written.
This is because by default, only messages with level warning and up are
written.
</p>

<h2>Python set logging level</h2>

<p>
The logging level is set with <code>setLevel</code>.
It sets the threshold for this logger to <code>lvl</code>.
Logging messages which are less severe than <code>lvl</code> will be ignored.
</p>

<div class="codehead">set_level.py</div>
<pre class="code">
#!/usr/bin/env python

import logging

logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)

logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
</pre>

<p>
In the example, we change the logging level to <code>DEBUG</code>.
</p>

<pre class="explanation">
logger = logging.getLogger('dev')
</pre>

<p>
The <code>getLogger</code> returns a logger with the specified name.
If name is <code>None</code>, it returns the root logger. The name can
be a dot separated string defining logging hierarchy; for instance
'a', 'a.b', or 'a.b.c'. Note that there is an implicit root name, which
is not shown.
</p>

<pre class="compact">
$ set_level.py
This is a warning message
This is an error message
This is a critical message
</pre>

<p>
Now all the messages were written.
</p>

<h2>Python effective logging level</h2>

<p>
The effective logging level is the level set explicitly or
determined from the logger parents.
</p>

<div class="codehead">effective_level.py</div>
<pre class="code">
#!/usr/bin/env python

import logging

main_logger = logging.getLogger('main')
main_logger.setLevel(5)

dev_logger = logging.getLogger('main.dev')

print(main_logger.getEffectiveLevel())
print(dev_logger.getEffectiveLevel())
</pre>

<p>
In the example, we examine the effective logging level of two loggers.
</p>

<pre class="explanation">
dev_logger = logging.getLogger('main.dev')
</pre>

<p>
The level of the <code>dev_logger</code> is not set; the level of
its parent is then used.
</p>

<pre class="compact">
$ effective_level.py
5
5
</pre>


<h2>Python logging handlers</h2>

<p>
Handler is an object responsible for dispatching the appropriate log
messages (based on the log messages' severity) to the handler's
specified destination.
</p>

<p>
Handlers are propagated like levels. If the logger has no
handler set, its chain of ancestors is search for a handler.
</p>

<div class="codehead">handlers.py</div>
<pre class="code">
#!/usr/bin/env python

import logging

logger = logging.getLogger('dev')
logger.setLevel(logging.INFO)

fileHandler = logging.FileHandler('test.log')
fileHandler.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

logger.info('information message')
</pre>

<p>
The example creates two handlers for a logger: a file handler and
a console handler.
</p>

<pre class="explanation">
fileHandler = logging.FileHandler('test.log')
</pre>

<p>
<code>FileHandler</code> sends log records to the <code>test.log</code>
file.
</p>

<pre class="explanation">
consoleHandler = logging.StreamHandler()
</pre>

<p>
<code>StreamHandler</code> sends log records to a stream.
If the stream is not specified, the <code>sys.stderr</code> is used.
</p>

<pre class="explanation">
logger.addHandler(fileHandler)
</pre>

<p>
The handler is added to the logger with <code>addHandler</code>.
</p>

<h2>Python logging formatters</h2>

<p>
Formatter is an object which configures the final order,
structure, and contents of the log record. In addition to
the message string, log records also include date and time,
log names, and log level severity.
</p>

<div class="codehead">formatter.py</div>
<pre class="code">
#!/usr/bin/env python

import logging

logger = logging.getLogger('dev')
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)

formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
consoleHandler.setFormatter(formatter)

logger.info('information message')
</pre>

<p>
The example creates a console logger and adds a formatter to its
handler.
</p>

<pre class="explanation">
formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
</pre>

<p>
The formatter is created. It includes the date time, logger name, logging level name,
and log message.
</p>

<pre class="explanation">
consoleHandler.setFormatter(formatter)
</pre>

<p>
The formatter is set to the handler with <code>setFormatter</code>.
</p>

<pre class="compact">
$ formatter.py
2019-03-28 14:53:27,446  dev  INFO: information message
</pre>

<p>
The message with the defined format is shown in the console.
</p>





<h2>Python logging basicConfig</h2>

<p>
The <code>basicConfig</code> configures the root logger. It does basic
configuration for the logging system by creating a stream handler with a default
formatter. The <code>debug</code>, <code>info</code>,
<code>warning</code>, <code>error</code> and <code>critical</code> call
<code>basicConfig</code> automatically if no handlers are defined for the root logger.
</p>

<div class="codehead">basic_config.py</div>
<pre class="code">
#!/usr/bin/env python

import logging

logging.basicConfig(filename='test.log', format='%(filename)s: %(message)s',
                    level=logging.DEBUG)

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
</pre>

<p>
The example configures the root logger with <code>basicConfig</code>.
</p>

<pre class="explanation">
logging.basicConfig(filename='test.log', format='%(filename)s: %(message)s',
    level=logging.DEBUG)
</pre>

<p>
With <code>filename</code>, we set the file to which we write the log messages.
The <code>format</code> determines what is logged into the file; we have
the filename and the message. With <code>level</code>, we set the logging treshold.
</p>

<pre class="compact">
$ basic_config.py
$ cat test.log
basic_config.py: This is a debug message
basic_config.py: This is an info message
basic_config.py: This is a warning message
basic_config.py: This is an error message
basic_config.py: This is a critical message
</pre>

<p>
After running the program, we have five messages written into the
<code>test.log</code> file.
</p>

<h2>Python logging fileConfig</h2>

<p>
The <code>fileConfig</code> reads the logging configuration from
a configparser format file.
</p>

<div class="codehead">log.conf</div>
<pre class="code">
[loggers]
keys=root,dev

[handlers]
keys=consoleHandler

[formatters]
keys=extend,simple

[logger_root]
level=INFO
handlers=consoleHandler

[logger_dev]
level=INFO
handlers=consoleHandler
qualname=dev
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=extend
args=(sys.stdout,)

[formatter_extend]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s

[formatter_simple]
format=%(asctime)s - %(message)s
</pre>

<p>
The <code>log.conf</code> defines a logger, handler, and formatter.
</p>

<div class="codehead">file_config.py</div>
<pre class="code">
#!/usr/bin/env python

import logging
import logging.config

logging.config.fileConfig(fname='log.conf')

logger = logging.getLogger('dev')
logger.info('This is an information message')
</pre>

<p>
The example reads the logging configuration file from
the <code>log.conf</code>.
</p>

<pre class="compact">
$ file_config.py
2019-03-28 15:26:31,137 - dev - INFO - This is an information message
</pre>


<h2>Python logging variable</h2>

<p>
Dynamic data is logged by using string formatting.
</p>

<div class="codehead">log_variable.py</div>
<pre class="code">
#!/usr/bin/env python

import logging

root = logging.getLogger()
root.setLevel(logging.INFO)

log_format = '%(asctime)s %(filename)s: %(message)s'
logging.basicConfig(filename="test.log", format=log_format)

# incident happens

error_message = 'authentication failed'

root.error(f'error: {error_message}')
</pre>

<p>
The example writes custom data to the log message.
</p>

<pre class="compact">
2019-03-21 14:17:23,196 log_variable.py: error: authentication failed
</pre>

<p>
This is the log message.
</p>

<h2>Python logging format datetime</h2>

<p>
The datetime is included in the log message with the <code>asctime</code>
log record. With the <code>datefmt</code> configuration option, we can format
the datetime string.
</p>

<div class="codehead">date_time.py</div>
<pre class="code">
#!/usr/bin/env python

import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

log_format = '%(asctime)s %(filename)s: %(message)s'
logging.basicConfig(filename="test.log", format=log_format,
                    datefmt='%Y-%m-%d %H:%M:%S')

logger.info("information message")
</pre>

<p>
The example formats the datetime of the log message.
</p>

<pre class="explanation">
log_format = '%(asctime)s %(filename)s: %(message)s'
</pre>

<p>
We include the datetime string into the log with <code>asctime</code>.
</p>

<pre class="explanation">
logging.basicConfig(filename="test.log", format=log_format,
                    datefmt='%Y-%m-%d %H:%M:%S')
</pre>

<p>
The <code>datefmt</code> option formats the datetime string.
</p>

<pre class="compact">
2019-03-21 14:17:23,196 log_variable.py: error: authentication failed
2019-03-21 14:23:33 date_time.py: information message
</pre>

<p>
Notice the difference in the datetime string format.
</p>

<h2>Python logging stack trace</h2>

<p>
The stack trace is a call stack of functions that were run
up to the point of a thrown exceptions. The stack trace is
included with the <code>exc_info</code> option.
</p>

<div class="codehead">stack_trace.py</div>
<pre class="code">
#!/usr/bin/env python

import logging

log_format = '%(asctime)s %(filename)s: %(message)s'
logging.basicConfig(filename="test.log", format=log_format)

vals = [1, 2]

try:
    print(vals[4])

except Exception as e:
    logging.error("exception occurred", exc_info=True)
</pre>

<p>
In the example, we log the exception that is thrown when we
try to access a non-existing list index.
</p>

<pre class="explanation">
logging.error("exception occurred", exc_info=True)
</pre>

<p>
The stack trace is included in the log by setting the <code>exc_info</code>
to <code>True</code>.
</p>

<pre class="compact">
2019-03-21 14:56:21,313 stack_trace.py: exception occurred
Traceback (most recent call last):
  File "C:\Users\Jano\Documents\pyprogs\pylog\stack_trace.py", line 11, in &lt;module&gt;
    print(vals[4])
IndexError: list index out of range
</pre>

<p>
The stack trace is included in the log.
</p>

<h2>Python logging getLogger</h2>

<p>
The <code>getLogger</code> returns a logger with the specified name.
If no name is specified, it returns the root logger. It is a common practice
to put the module name there with <code>__name__</code>.
</p>

<p>
All calls to this function with a given name return the same logger instance.
This means that logger instances never need to be passed between different parts
of an application.
</p>

<div class="codehead">get_logger.py</div>
<pre class="code">
#!/usr/bin/env python

import logging
import sys

main = logging.getLogger('main')
main.setLevel(logging.DEBUG)

handler = logging.FileHandler('my.log')

format = logging.Formatter('%(asctime)s  %(name)s
    %(levelname)s: %(message)s')
handler.setFormatter(format)

main.addHandler(handler)

main.info('info message')
main.critical('critical message')
main.debug('debug message')
main.warning('warning message')
main.error('error message')
</pre>

<p>
The example creates a new logger with <code>getLogger</code>.
It is given a file handler and a formatter.
</p>

<pre class="explanation">
main = logging.getLogger('main')
main.setLevel(logging.DEBUG)
</pre>

<p>
A logger named <code>main</code> is created; we set the
logging level to <code>DEBUG</code>.
</p>

<pre class="explanation">
handler = logging.FileHandler('my.log')
</pre>

<p>
A file handler is created. The messages will be written to the
<code>my.log</code> file.
</p>

<pre class="explanation">
format = logging.Formatter('%(asctime)s  %(name)s
    %(levelname)s: %(message)s')
handler.setFormatter(format)
</pre>

<p>
A formatter is created. It includes the time, the logger name,
the logging level, and the message in to log. The formatter is
set to the handler with <code>setFormatter</code>.
</p>

<pre class="explanation">
main.addHandler(handler)
</pre>

<p>
The handler is added to the logger with <code>addHandler</code>.
</p>

<pre class="compact">
$ cat my.log
2019-03-21 14:15:45,439  main  INFO: info message
2019-03-21 14:15:45,439  main  CRITICAL: critical message
2019-03-21 14:15:45,439  main  DEBUG: debug message
2019-03-21 14:15:45,439  main  WARNING: warning message
2019-03-21 14:15:45,439  main  ERROR: error message
</pre>

<p>
These are the written log messages.
</p>

<h2>Python logging YAML configuration</h2>

<p>
Logging details can be defined in a YAML configuration file.
YAML is a human-readable data serialization language. It is commonly
used for configuration files.
</p>

<pre class="compact">
$ pip install pyyaml
</pre>

<p>
We need to install <code>pyyaml</code> module.
</p>

<div class="codehead">config.yaml</div>
<pre class="code">
version: 1

formatters:
  simple:
    format: "%(asctime)s %(name)s: %(message)s"
  extended:
    format: "%(asctime)s %(name)s %(levelname)s: %(message)s"

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: simple

  file_handler:
    class: logging.FileHandler
    level: INFO
    filename: test.log
    formatter: extended
    propagate: false

loggers:
  dev:
    handlers: [console, file_handler]
  test:
    handlers: [file_handler]
root:
  handlers: [file_handler]
</pre>

<p>
In the configuration file, we have defined various formatters, handlers, and
loggers. The <code>propagate</code> option prevents from propagating
log messages to the parent loggers; in our case, to the root logger.
Otherwise, the messages would be duplicated.
</p>

<div class="codehead">log_yaml.py</div>
<pre class="code">
#!/usr/bin/env python

import logging
import logging.config
import yaml

with open('config.yaml', 'r') as f:

    log_cfg = yaml.safe_load(f.read())

logging.config.dictConfig(log_cfg)

logger = logging.getLogger('dev')
logger.setLevel(logging.INFO)

logger.info('This is an info message')
logger.error('This is an error message')
</pre>

<p>
In the example, we read the configuration file and use
the <code>dev</code> logger.
</p>

<pre class="compact">
$ log_yaml.py
2019-03-28 11:36:54,854 dev: This is an info message
2019-03-28 11:36:54,855 dev: This is an error message
</pre>

<p>
When we run the program, there are two messages on the console.
The console handlers use the simple formatter with less information.
</p>

<pre class="compact">
...
2019-03-28 11:36:54,854 dev INFO: This is an info message
2019-03-28 11:36:54,855 dev ERROR: This is an error message
</pre>

<p>
There are log messages inside the <code>test.log</code> file.
They are produced by the extended formatter with more information.
</p>


</div> <!-- content -->

<div class="rtow">




</div>

</div> <!-- container -->

</body>
</html>
