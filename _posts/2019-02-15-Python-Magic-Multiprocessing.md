---
layout: post
title: Python-Multiprocessing
date: 2019-02-15 16:20:23 +0900
category: Python
tag: Python
---



<html lang="en">

<head>

</head>

<body>


<div class="container">


<div class="content">

<h1>Python Multiprocessing</h1>

<p>
The <code>multiprocessing</code> module allows the programmer to fully
leverage multiple processors on a given machine. The API used is similar
to the classic <code>threading</code> module. It offers both local and remote
concurrency.
</p>



<p>
The multiprocesing module avoids the limitations of the Global Interpreter Lock
(GIL) by using subprocesses instead of threads. The multiprocessed code does not
execute in the same order as serial code. There is no guarantee that the
first process to be created will be the first to complete.
</p>

<h2>Python GIL</h2>

<p>
A global interpreter lock (GIL) is a mechanism used in Python interpreter to
synchronize the execution of threads so that only one native thread can execute
at a time, even if run on a multi-core processor.
</p>

<p>
The C extensions, such as numpy, can manually release the GIL to speed up
computations. Also, the GIL released before potentionally blocking I/O
operations.
</p>

<p>
Note that both Jython and IronPython do not have the GIL.
</p>


<h2>Concurrency and parallelism</h2>

<p>
Concurrency means that two or more calculations happen within the same time
frame. Parallelism means that two or more calculations happen at the same
moment. Parallelism is therefore a specific case of concurrency. It requires
multiple CPU units or cores.
</p>

<p>
True parallelism in Python is achieved by creating multiple processes, each
having a Python interpreter with its own separate GIL.
</p>

<p>
Python has three modules for concurrency: <code>multiprocessing</code>,
<code>threading</code>, and <code>asyncio</code>. When the tasks are CPU
intensive, we should consider the <code>multiprocessing</code> module. When
the tasks are I/O bound and require lots of connections, the <code>asyncio</code>
module is recommended. For other types of tasks and when libraries cannot
cooperate with <code>asyncio</code>, the <code>threading</code> module can be
considered.
</p>


<h2>Embarrassinbly parallel</h2>

<p>
The term <em>embarrassinbly parallel</em> is used to describe a problem or workload
that can be easily run in parallel. It is important to realize that not all workloads
can be divided into subtasks and run parallelly. For instance those, who need lots
of communication among subtasks.
</p>

<p>
The examples of perfectly parallel computations include:
</p>

<ul>
  <li>Monte Carlo analysis</li>
  <li>numerical integration</li>
  <li>rendering of computer graphics</li>
  <li>brute force searches in cryptography</li>
  <li>genetic algorithms</li>
</ul>

<p>
Another situation where parallel computations can be applied is when we run
several different computations, that is, we don't divide a problem into subtasks.
For instance, we could run calculations of &pi; using different algorithms in
parallel.
</p>

<h2>Process vs thread</h2>

<p>
Both processes and threads are independent sequences of execution. The following
table summarizes the differences between a process and a thread:
</p>

<table>
<thead>
<tr>
<th>Process</th>
<th>Thread</th>
</tr>
</thead>
<tbody>
<tr>
<td>processes run in separate memory (process isolation)</td>
<td>threads share memory</td>
</tr>
<tr>
<td>uses more memory</td>
<td>uses less memory</td>
</tr>
<tr>
<td>children can become zombies</td>
<td>no zombies possible</td>
</tr>
<tr>
<td>more overhead</td>
<td>less overhead</td>
</tr>
<tr>
<td>slower to create and destroy</td>
<td>faster to create and destroy</td>
</tr>
<tr>
<td>easier to code and debug</td>
<td>can become harder to code and debug</td>
</tr>
</tbody>
</table>

<div class="figure">Table: Process vs thread</div>


<h2>Process</h2>

<p>
The <code>Process</code> object represents an activity that is run in a
separate process. The <code>multiprocessing.Process</code> class has equivalents
of all the methods of <code>threading.Thread</code>. The <code>Process</code>
constructor should always be called with keyword arguments.
</p>

<p>
The <code>target</code> argument of the constructor is the callable
object to be invoked by the <code>run</code> method.
The <code>name</code> is the process name. The <code>start</code> method
starts the process's activity. The <code>join</code> method blocks until the
process whose <code>join</code> method is called terminates. If the
<code>timeout</code> option is provided, it blocks at most timeout seconds.
The <code>is_alive</code> method returns a boolean value indicationg whether the
process is alive. The <code>terminate</code> method terminates the process.
</p>

<h2>The __main__ guard</h2>

<p>
The Python multiprocessing style guide recommends to place the multiprocessing
code inside the <code>__name__ == '__main__'</code> idiom. This is due to the
way the processes are created on Windows. The guard is to prevent the endless
loop of process generations.
</p>


<h2>Simple process example</h2>

<p>
The following is a simple program that uses <code>multiprocessing</code>.
</p>

<div class="codehead">simple.py</div>
<pre class="code">
#!/usr/bin/python

from multiprocessing import Process


def fun(name):
    print(f'hello {name}')

def main():

    p = Process(target=fun, args=('Peter',))
    p.start()


if __name__ == '__main__':
    main()
</pre>

<p>
We create a new process and pass a value to it.
</p>

<pre class="explanation">
def fun(name):
    print(f'hello {name}')
</pre>

<p>
The function prints the passed parameter.
</p>

<pre class="explanation">
def main():

    p = Process(target=fun, args=('Peter',))
    p.start()
</pre>

<p>
A new process is created. The <code>target</code> option provides the callable
that is run in the new process. The <code>args</code> provides the data to
be passed. The multiprocessing code is placed inside the main guard.
The process is started with the <code>start</code> method.
</p>

<pre class="explanation">
if __name__ == '__main__':
    main()
</pre>

<p>
The code is placed inside the <code>__name__ == '__main__'</code> idiom.
</p>


<h2>Python multiprocessing join</h2>

<p>
The <code>join</code> method blocks the execution of the main process until the
process whose <code>join</code> method is called terminates. Without the
<code>join</code> method, the main process won't wait until the process gets
terminated.
</p>

<div class="codehead">joining.py</div>
<pre class="code">
#!/usr/bin/python

from multiprocessing import Process
import time

def fun():

    print('starting fun')
    time.sleep(2)
    print('finishing fun')

def main():

    p = Process(target=fun)
    p.start()
    p.join()


if __name__ == '__main__':

    print('starting main')
    main()
    print('finishing main')
</pre>

<p>
The example calls the <code>join</code> on the newly created process.
</p>

<pre class="compact">
$ ./joining.py
starting main
starting fun
finishing fun
finishing main
</pre>

<p>
The <em>finishing main</em> message is printed after the child process has
finished.
</p>

<pre class="compact">
$ ./joining.py
starting main
finishing main
starting fun
finishing fun
</pre>

<p>
When we comment out the <code>join</code> method, the main process finishes
before the child process.
</p>

<p>
It is important to call the <code>join</code> methods after the <code>start</code>
methods.
</p>

<div class="codehead">join_order.py</div>
<pre class="code">
#!/usr/bin/python

from multiprocessing import Process
import time

def fun(val):

    print(f'starting fun with {val} s')
    time.sleep(val)
    print(f'finishing fun with {val} s')


def main():

    p1 = Process(target=fun, args=(3, ))
    p1.start()
    # p1.join()

    p2 = Process(target=fun, args=(2, ))
    p2.start()
    # p2.join()

    p3 = Process(target=fun, args=(1, ))
    p3.start()
    # p3.join()

    p1.join()
    p2.join()
    p3.join()

    print('finished main')

if __name__ == '__main__':

    main()
</pre>

<p>
If we call the <code>join</code> methods incorrectly, then we in fact run
the processes sequentially. (The incorrect way is commented out.)
</p>


<h2>Python multiprocessing is_alive</h2>

<p>
The <code>is_alive</code> method determines if the process is running.
</p>

<div class="codehead">alive.py</div>
<pre class="code">
#!/usr/bin/python

from multiprocessing import Process
import time

def fun():

    print('calling fun')
    time.sleep(2)

def main():

    print('main fun')

    p = Process(target=fun)
    p.start()
    p.join()

    print(f'Process p is alive: {p.is_alive()}')


if __name__ == '__main__':
    main()
</pre>

<p>
When we wait for the child process to finish with the <code>join</code> method,
the process is already dead when we check it. If we comment out the <code>join</code>,
the process is still alive.
</p>



<h2>Python multiprocessing Process Id</h2>

<p>
The <code>os.getpid</code> returns the current process Id, while the
<code>os.getppid</code> returns the parent's process Id.
</p>

<div class="codehead">process_id.py</div>
<pre class="code">
#!/usr/bin/python

from multiprocessing import Process
import os

def fun():

    print('--------------------------')

    print('calling fun')
    print('parent process id:', os.getppid())
    print('process id:', os.getpid())

def main():

    print('main fun')
    print('process id:', os.getpid())

    p1 = Process(target=fun)
    p1.start()
    p1.join()

    p2 = Process(target=fun)
    p2.start()
    p2.join()


if __name__ == '__main__':
    main()
</pre>

<p>
The example runs two child processes. It prints their Id and their parent's Id.
</p>

<pre class="compact">
$ ./parent_id.py
main fun
process id: 7605
--------------------------
calling fun
parent process id: 7605
process id: 7606
--------------------------
calling fun
parent process id: 7605
process id: 7607
</pre>

<p>
The parent Id is the same, the process Ids are different for each child process.
</p>


<h2>Naming processes</h2>

<p>
With the <code>name</code> property of the <code>Process</code>, we can
give the worker a specific name. Otherwise, the module creates its own name.
</p>

<div class="codehead">naming_workers.py</div>
<pre class="code">
#!/usr/bin/python

from multiprocessing import Process, current_process
import time

def worker():

    name = current_process().name
    print(name, 'Starting')
    time.sleep(2)
    print(name, 'Exiting')

def service():

    name = current_process().name
    print(name, 'Starting')
    time.sleep(3)
    print(name, 'Exiting')

if __name__ == '__main__':

    service = Process(name='Service 1', target=service)
    worker1 = Process(name='Worker 1', target=worker)
    worker2 = Process(target=worker) # use default name

    worker1.start()
    worker2.start()
    service.start()
</pre>

<p>
In the example, we create three processes; two of them are given a custom name.
</p>

<pre class="compact">
$ ./naming_workers.py
Worker 1 Starting
Process-3 Starting
Service 1 Starting
Worker 1 Exiting
Process-3 Exiting
Service 1 Exiting
</pre>



<h2>Subclassing Process</h2>

<p>
When we subclass the <code>Process</code>, we override the <code>run</code>
method.
</p>

<div class="codehead">subclass.py</div>
<pre class="code">
#!/usr/bin/python

import time
from multiprocessing import Process


class Worker(Process):

    def run(self):

        print(f'In {self.name}')
        time.sleep(2)

def main():

    worker = Worker()
    worker.start()

    worker2 = Worker()
    worker2.start()

    worker.join()
    worker2.join()

if __name__ == '__main__':
    main()
</pre>

<p>
We create a <code>Worker</code> class which inherits from the <code>Process</code>.
In the <code>run</code> method, we write the worker's code.
</p>


<h2>Python multiprocessing Pool</h2>

<p>
The management of the worker processes can be simplified with the <code>Pool</code>
object. It controls a pool of worker processes to which jobs can be submitted.
The pool's <code>map</code> method chops the given iterable into a number of
chunks which it submits to the process pool as separate tasks. The pool's
<code>map</code> is a parallel equivalent of the built-in <code>map</code> method.
The <code>map</code> blocks the main execution until all computations finish.
</p>

<p>
The <code>Pool</code> can take the number of processes as a parameter.
It is a value with which we can experiment. If we do not provide any value,
then the number returned by <code>os.cpu_count</code> is used.
</p>

<div class="codehead">worker_pool.py</div>
<pre class="code">
#!/usr/bin/python

import time
from timeit import default_timer as timer
from multiprocessing import Pool, cpu_count


def square(n):

    time.sleep(2)

    return n * n


def main():

    start = timer()

    print(f'starting computations on {cpu_count()} cores')

    values = (2, 4, 6, 8)

    with Pool() as pool:
        res = pool.map(square, values)
        print(res)

    end = timer()
    print(f'elapsed time: {end - start}')

if __name__ == '__main__':
    main()
</pre>

<p>
In the example, we create a pool of processes and apply values on the
<code>square</code> function. The number of cores is determined with the
<code>cpu_unit</code> function.
</p>

<pre class="compact">
$ ./worker_pool.py
starting computations on 4 cores
[4, 16, 36, 64]
elapsed time: 2.0256662130013865
</pre>

<p>
On a computer with four cores it took slightly more than 2 seconds to finish
four computations, each lasting two seconds.
</p>

<pre class="compact">
$ ./worker_pool.py
starting computations on 4 cores
[4, 16, 36, 64, 100]
elapsed time: 4.029600699999719
</pre>

<p>
When we add additional value to be computed, the time increased to over four
seconds.
</p>


<h2>Multiple arguments</h2>

<p>
To pass multiple arguments to a worker function, we can use the <code>starmap</code>
method. The elements of the iterable are expected to be iterables that are
unpacked as arguments.
</p>

<div class="codehead">multi_args.py.py</div>
<pre class="code">
#!/usr/bin/python

import time
from timeit import default_timer as timer
from multiprocessing import Pool, cpu_count


def power(x, n):

    time.sleep(1)

    return x ** n


def main():

    start = timer()

    print(f'starting computations on {cpu_count()} cores')

    values = ((2, 2), (4, 3), (5, 5))

    with Pool() as pool:
        res = pool.starmap(power, values)
        print(res)

    end = timer()
    print(f'elapsed time: {end - start}')


if __name__ == '__main__':
    main()
</pre>

<p>
In this example, we pass two values to the <code>power</code> function: the
value and the exponent.
</p>

<pre class="compact">
$ ./multi_args.py
starting computations on 4 cores
[4, 64, 3125]
elapsed time: 1.0230950259974634
</pre>





<h2>Multiple functions</h2>

<p>
The following example shows how to run multiple functions
in a pool.
</p>

<div class="codehead">multiple_functions.py</div>
<pre class="code">
#!/usr/bin/python

from multiprocessing import Pool
import functools


def inc(x):
    return x + 1

def dec(x):
    return x - 1

def add(x, y):
    return x + y

def smap(f):
    return f()


def main():

    f_inc = functools.partial(inc, 4)
    f_dec = functools.partial(dec, 2)
    f_add = functools.partial(add, 3, 4)

    with Pool() as pool:
        res = pool.map(smap, [f_inc, f_dec, f_add])

        print(res)


if __name__ == '__main__':
    main()
</pre>

<p>
We have three functions, which are run independently in a pool. We use the
<code>functools.partial</code> to prepare the functions and their parameters
before they are executed.
</p>

<pre class="compact">
$ ./multiple_functions.py
[5, 1, 7]
</pre>




<h2>Python multiprocessing &pi; calculation</h2>

<p>
The &pi; is the ratio of the circumference of any circle to the diameter of the
circle. The &pi; is an irrational number whose decimal form neither ends
nor becomes repetitive. It is approximately equal to 3.14159. There are several
formulas to calculate &pi;.
</p>

<p>
Calculating approximations of &pi; can take a long time, so we can leverage the
parallel computations. We use the Bailey–Borwein–Plouffe formula to calculate &pi;.
</p>

<div class="codehead">calc_pi.py</div>
<pre class="code">
#!/usr/bin/python

from decimal import Decimal, getcontext
from timeit import default_timer as timer

def pi(precision):

    getcontext().prec = precision

    return sum(1/Decimal(16)**k *
        (Decimal(4)/(8*k+1) -
         Decimal(2)/(8*k+4) -
         Decimal(1)/(8*k+5) -
         Decimal(1)/(8*k+6)) for k in range (precision))


start = timer()
values = (1000, 1500, 2000)
data = list(map(pi, values))
print(data)

end = timer()
print(f'sequentially: {end - start}')
</pre>

<p>
First, we calculate three approximations sequentially. The precision is the number
of digits of the computed &pi;.
</p>

<pre class="compact">
$ ./calc_pi.py
...
sequentially: 0.5738053179993585
</pre>

<p>
On our machine, it took 0.57381 seconds to compute the three approximations.
</p>

<p>
In the following example, we use a pool of processes to calculate the three
approximations.
</p>

<div class="codehead">calc_pi2.py</div>
<pre class="code">
#!/usr/bin/python

from decimal import Decimal, getcontext
from timeit import default_timer as timer
from multiprocessing import Pool, current_process
import time


def pi(precision):

    getcontext().prec=precision

    return sum(1/Decimal(16)**k *
        (Decimal(4)/(8*k+1) -
         Decimal(2)/(8*k+4) -
         Decimal(1)/(8*k+5) -
         Decimal(1)/(8*k+6)) for k in range (precision))

def main():

    start = timer()

    with Pool(3) as pool:

        values = (1000, 1500, 2000)
        data = pool.map(pi, values)
        print(data)

    end = timer()
    print(f'paralelly: {end - start}')


if __name__ == '__main__':
    main()
</pre>

<p>
We run the calculations in a pool of three processes and we gain some small
increase in efficiency.
</p>

<pre class="compact">
./calc_pi2.py
...
paralelly: 0.38216479000038817
</pre>

<p>
When we run the calculations in parallel, it took 0.38216479 seconds.
</p>


<h2>Separate memory in a process</h2>

<p>
In multiprocessing, each worker has its own memory. The memory is not shared
like in threading.
</p>

<div class="codehead">own_memory_space.py</div>
<pre class="code">
#!/usr/bin/python

from multiprocessing import Process, current_process

data = [1, 2]

def fun():

    global data

    data.extend((3, 4, 5))
    print(f'Result in {current_process().name}: {data}')

def main():

    worker = Process(target=fun)
    worker.start()
    worker.join()

    print(f'Result in main: {data}')


if __name__ == '__main__':

    main()
</pre>

<p>
We create a worker to which we pass the global <code>data</code> list.
We add additional values to the list in the worker but the original list in the
main process is not modified.
</p>

<pre class="compact">
$ ./own_memory_space.py
Result in Process-1: [1, 2, 3, 4, 5]
Result in main: [1, 2]
</pre>

<p>
As we can see from the output, the two lists are separate.
</p>


<h2>Sharing state between processes</h2>

<p>
Data can be stored in a shared memory using <code>Value</code> or
<code>Array</code>.
</p>

<div class="note">
<strong>Note:</strong> It is best to avoid sharing data between processes.
Message passing is preferred.
</div>

<br>

<div class="codehead">counter.py</div>
<pre class="code">
#!/usr/bin/python

from multiprocessing import Process, Value
from time import sleep


def f(counter):

    sleep(1)

    with counter.get_lock():
        counter.value += 1

    print(f'Counter: {counter.value}')

def main():

    counter = Value('i', 0)

    processes = [Process(target=f, args=(counter, )) for _ in range(30)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

if __name__ == '__main__':
    main()
</pre>

<p>
The example creates a counter object which is shared among processes.
Each of the processes increases the counter.
</p>

<pre class="explanation">
with counter.get_lock():
    counter.value += 1
</pre>

<p>
Each process must acquire a lock for itself.
</p>


<h2>Message passing with queues</h2>

<p>
The message passing is the preferred way of communication among processes.
Message passing avoids having to use synchronization primitives such as
locks, which are difficult to use and error prone in complex situations.
</p>

<p>
To pass messages, we can utilize the pipe for the connection between two
processes. The queue allows multiple producers and consumers.
</p>

<div class="codehead">simple_queue.py</div>
<pre class="code">
#!/usr/bin/python

from multiprocessing import Process, Queue
import random

def rand_val(queue):

    num = random.random()
    queue.put(num)


def main():

    queue = Queue()

    processes = [Process(target=rand_val, args=(queue,)) for _ in range(4)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    results = [queue.get() for _ in processes]
    print(results)

if __name__ == "__main__":
    main()
</pre>

<p>
In the example, we create four processes. Each process generates a random value
and puts it into the queue. After all processes finish, we get all values from
the queue.
</p>

<pre class="explanation">
processes = [Process(target=rand_val, args=(queue,)) for _ in range(4)]
</pre>

<p>
The queue is passed as an argument to the process.
</p>

<pre class="explanation">
results = [queue.get() for _ in processes]
</pre>

<p>
The <code>get</code> method removes and returns the item from the queue.
</p>

<pre class="compact">
$ ./simple_queue.py
[0.7829025790441544, 0.46465345633928223, 0.4804438310782676, 0.7146952404346074]
</pre>

<p>
The example generates a list of four random values.
</p>

<p>
In the following example, we put words in a queue. The created processes
read the words from the queue.
</p>

<div class="codehead">simple_queue2.py</div>
<pre class="code">
#!/usr/bin/python

from multiprocessing import Queue, Process, current_process


def worker(queue):
    name = current_process().name
    print(f'{name} data received: {queue.get()}')


def main():

    queue = Queue()
    queue.put("wood")
    queue.put("sky")
    queue.put("cloud")
    queue.put("ocean")

    processes = [Process(target=worker, args=(queue,)) for _ in range(4)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
</pre>

<p>
Four processes are created; each of them reads a word from the queue and prints
it.
</p>

<pre class="compact">
$ ./simple_queue2.py
Process-1 data received: wood
Process-2 data received: sky
Process-3 data received: cloud
Process-4 data received: ocean
</pre>


<div class="note">
<strong>Note: </strong> Read the <a href="/articles/tkinterlongruntask/">Long-running task in Tkinter</a>
to learn how to use a queue in a Tkinter GUI application.
</div>


<h2>Queue order</h2>

<p>
In multiprocessing, there is no guarantee that the processes finish in a certain
order.
</p>

<div class="codehead">queue_order.py</div>
<pre class="code">
#!/usr/bin/python

from multiprocessing import Process, Queue
import time
import random

def square(idx, x, queue):

    time.sleep(random.randint(1, 3))
    queue.put((idx, x * x))


def main():

    data = [2, 4, 6, 3, 5, 8, 9, 7]
    queue = Queue()
    processes = [Process(target=square, args=(idx, val, queue))
                 for idx, val in enumerate(data)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    unsorted_result = [queue.get() for _ in processes]

    result = [val[1] for val in sorted(unsorted_result)]
    print(result)


if __name__ == '__main__':
    main()
</pre>

<p>
We have processes that calculate the square of a value. The input data is
in certain order and we need to maintain this order. To deal with this,
we keep an extra index for each input value.
</p>

<pre class="explanation">
def square(idx, x, queue):

    time.sleep(random.randint(1, 3))
    queue.put((idx, x * x))
</pre>

<p>
To illustrate variation, we randomly slow down the calculation with the <code>sleep</code>
method. We place an index into the queue with the calculated square.
</p>

<pre class="explanation">
unsorted_result = [queue.get() for _ in processes]
</pre>

<p>
We get the results. At this moment, the tuples are in random order.
</p>

<pre class="explanation">
result = [val[1] for val in sorted(unsorted_result)]
</pre>

<p>
We sort the result data by their index values.
</p>

<pre class="compact">
$ ./queue_order.py
[4, 16, 36, 9, 25, 64, 81, 49]
</pre>

<p>
We get the square values that correspond to the initial data.
</p>


<h2>Calculating &pi; with Monte Carlo method</h2>

<p>
Monte Carlo methods  are a broad class of computational algorithms that rely on
repeated random sampling to obtain numerical results. The underlying concept is
to use randomness to solve problems that might be deterministic in principle.
</p>

<p>
The following formula is used to calculate the approximation of &pi;:
</p>

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mfrac>
    <mi>&#x03C0;</mi>
    <mn>4</mn>
  </mfrac>
  <mo>&#x2248;</mo>
  <mfrac>
    <mi>M</mi>
    <mi>N</mi>
  </mfrac>
</math>

<p>
The <em>M</em> is the number of generated points in the square and <em>N</em>
is the total number of points.
</p>

<p>
While this method of &pi; calculation is interesting and perfect for school
examples, it is not very accurate. There are far better algorithms to get &pi;.
</p>

<div class="codehead">monte_carlo_pi.py</div>
<pre class="code">
#!/usr/bin/python

from random import random
from math import sqrt
from timeit import default_timer as timer


def pi(n):

    count = 0

    for i in range(n):

        x, y = random(), random()

        r = sqrt(pow(x, 2) + pow(y, 2))

        if r &lt; 1:
            count += 1

    return 4 * count / n


start = timer()
pi_est = pi(100_000_000)
end = timer()

print(f'elapsed time: {end - start}')
print(f'π estimate: {pi_est}')
</pre>

<p>
In the example, we calculate the approximation of the &pi; value using
one hundred million generated random points.
</p>

<pre class="compact">
$ ./monte_carlo_pi.py
elapsed time: 44.7768127549989
π estimate: 3.14136588

</pre>

<p>
It took 44.78 seconds to calculate the approximation of &pi;
</p>

<p>
Now we divide the whole task of &pi; computation into subtasks.
</p>

<div class="codehead">monte_carlo_pi_mul.py</div>
<pre class="code">
#!/usr/bin/python

import random
from multiprocessing import Pool, cpu_count
from math import sqrt
from timeit import default_timer as timer


def pi_part(n):
    print(n)

    count = 0

    for i in range(int(n)):

        x, y = random.random(), random.random()

        r = sqrt(pow(x, 2) + pow(y, 2))

        if r &lt; 1:
            count += 1

    return count


def main():

    start = timer()

    np = cpu_count()
    print(f'You have {np} cores')

    n = 100_000_000

    part_count = [n/np for i in range(np)]

    with Pool(processes=np) as pool:

        count = pool.map(pi_part, part_count)
        pi_est = sum(count) / (n * 1.0) * 4

        end = timer()

        print(f'elapsed time: {end - start}')
        print(f'π estimate: {pi_est}')

if __name__=='__main__':
    main()
</pre>

<p>
In the example, we find out the number of cores and divide the random sampling
into subtasks. Each task will compute the random values independently.
</p>

<pre class="explanation">
n = 100_000_000

part_count = [n/np for i in range(np)]
</pre>

<p>
Instead of calculating 100_000_000 in one go, each subtask will calculate a
portion of it.
</p>

<pre class="explanation">
count = pool.map(pi_part, part_count)
pi_est = sum(count) / (n * 1.0) * 4
</pre>

<p>
The partial calculations are passed to the <code>count</code> variable and
the sum is then used in the final formula.
</p>

<pre class="compact">
$ ./monte_carlo_pi_mul.py
You have 4 cores
25000000.0
25000000.0
25000000.0
25000000.0
elapsed time: 29.45832426099878
π estimate: 3.1414868
</pre>

<p>
When running the example in parallel with four cores, the calculations took
29.46 seconds.
</p>

<!-- events, password cracking, image resizing, apply_async -->


</div> <!-- content -->

<div class="rtow">


</div>

</div> <!-- container -->



</body>
</html>
