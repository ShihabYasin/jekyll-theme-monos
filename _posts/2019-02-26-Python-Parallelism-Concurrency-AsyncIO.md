---
layout: post
title: Python-Parallelism-Concurrency-AsyncIO
date: 2019-02-26 16:20:23 +0900
category: Python
tag: Python
---

## Parallelism, Concurrency and AsyncIO in Python

<header class="hero blog-hero blog-detail-hero">

</header>



<div class="container blog-container" style="padding-top: 0;">
    <div class="row">
      <div class="col col-12 col-lg-8">

</div>
<h2 id="concurrency-vs-parallelism">Concurrency vs Parallelism</h2>
<p> Concurrency and parallelism are similar terms, but they are not the same thing.</p>
<p>Concurrency is the ability to run multiple tasks on the CPU at the same time. Tasks can start, run, and complete in overlapping time periods. In the case of a single CPU, multiple tasks are run with the help of <a href="https://en.wikipedia.org/wiki/Context_switch">context switching</a>, where the state of a process is stored so that it can be called and executed later.</p>
<p>Parallelism, meanwhile, is the ability to run multiple tasks at the same time across multiple CPU cores.</p>
<p>Though they can increase the speed of your application, concurrency and parallelism should not be used everywhere. The use case depends on whether the task is CPU-bound or IO-bound.</p>
<p>Tasks that are limited by the CPU are CPU-bound. For example, mathematical computations are CPU-bound since computational power increases as the number of computer processors increases. Parallelism is for CPU-bound tasks. In theory, If a task is divided into n-subtasks, each of these n-tasks can run in parallel to effectively reduce the time to 1/n of the original non-parallel task. Concurrency is preferred for IO-bound tasks, as you can do something else while the IO resources are being fetched.</p>
<p>The best example of CPU-bound tasks is in data science. Data Scientists deal with huge chunks of data. For data preprocessing, they can split the data into multiple batches and run them in parallel, effectively decreasing the total time to process. Increasing the number of cores results in faster processing.</p>
<p>Web scraping is IO-bound. Because the task has little effect on the CPU since most of the time is spent on reading from and writing to the network. Other common IO-bound tasks include database calls and reading and writing files to disk. Web applications, like Django and Flask, are IO-bound applications.</p>
<h2 id="scenario">Scenario</h2>
<p>With that, let's take a look at how to speed up the following tasks:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># tasks.py</span>

<span class="kn">import</span> <span class="nn">os</span>
<span class="kn">from</span> <span class="nn">multiprocessing</span> <span class="kn">import</span> <span class="n">current_process</span>
<span class="kn">from</span> <span class="nn">threading</span> <span class="kn">import</span> <span class="n">current_thread</span>

<span class="kn">import</span> <span class="nn">requests</span>

<span class="k">def</span> <span class="nf">make_request</span><span class="p">(</span><span class="n">num</span><span class="p">):</span>
<span class="c1"># io-bound</span>

<span class="n">pid</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getpid</span><span class="p">()</span>
<span class="n">thread_name</span> <span class="o">=</span> <span class="n">current_thread</span><span class="p">()</span><span class="o">.</span><span class="n">name</span>
<span class="n">process_name</span> <span class="o">=</span> <span class="n">current_process</span><span class="p">()</span><span class="o">.</span><span class="n">name</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">pid</span><span class="si">}</span><span class="s2"> - </span><span class="si">{</span><span class="n">process_name</span><span class="si">}</span><span class="s2"> - </span><span class="si">{</span><span class="n">thread_name</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>

<span class="n">requests</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;https://httpbin.org/ip&quot;</span><span class="p">)</span>

<span class="k">async</span> <span class="k">def</span> <span class="nf">make_request_async</span><span class="p">(</span><span class="n">num</span><span class="p">,</span> <span class="n">client</span><span class="p">):</span>
<span class="c1"># io-bound</span>

<span class="n">pid</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getpid</span><span class="p">()</span>
<span class="n">thread_name</span> <span class="o">=</span> <span class="n">current_thread</span><span class="p">()</span><span class="o">.</span><span class="n">name</span>
<span class="n">process_name</span> <span class="o">=</span> <span class="n">current_process</span><span class="p">()</span><span class="o">.</span><span class="n">name</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">pid</span><span class="si">}</span><span class="s2"> - </span><span class="si">{</span><span class="n">process_name</span><span class="si">}</span><span class="s2"> - </span><span class="si">{</span><span class="n">thread_name</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>

<span class="k">await</span> <span class="n">client</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;https://httpbin.org/ip&quot;</span><span class="p">)</span>

<span class="k">def</span> <span class="nf">get_prime_numbers</span><span class="p">(</span><span class="n">num</span><span class="p">):</span>
<span class="c1"># cpu-bound</span>

<span class="n">pid</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getpid</span><span class="p">()</span>
<span class="n">thread_name</span> <span class="o">=</span> <span class="n">current_thread</span><span class="p">()</span><span class="o">.</span><span class="n">name</span>
<span class="n">process_name</span> <span class="o">=</span> <span class="n">current_process</span><span class="p">()</span><span class="o">.</span><span class="n">name</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">pid</span><span class="si">}</span><span class="s2"> - </span><span class="si">{</span><span class="n">process_name</span><span class="si">}</span><span class="s2"> - </span><span class="si">{</span><span class="n">thread_name</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>

<span class="n">numbers</span> <span class="o">=</span> <span class="p">[]</span>

<span class="n">prime</span> <span class="o">=</span> <span class="p">[</span><span class="kc">True</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">num</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)]</span>
<span class="n">p</span> <span class="o">=</span> <span class="mi">2</span>

<span class="k">while</span> <span class="n">p</span> <span class="o">*</span> <span class="n">p</span> <span class="o">&lt;=</span> <span class="n">num</span><span class="p">:</span>
    <span class="k">if</span> <span class="n">prime</span><span class="p">[</span><span class="n">p</span><span class="p">]:</span>
        <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">p</span> <span class="o">*</span> <span class="mi">2</span><span class="p">,</span> <span class="n">num</span> <span class="o">+</span> <span class="mi">1</span><span class="p">,</span> <span class="n">p</span><span class="p">):</span>
            <span class="n">prime</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
    <span class="n">p</span> <span class="o">+=</span> <span class="mi">1</span>

<span class="n">prime</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>
<span class="n">prime</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="o">=</span> <span class="kc">False</span>

<span class="k">for</span> <span class="n">p</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">num</span> <span class="o">+</span> <span class="mi">1</span><span class="p">):</span>
    <span class="k">if</span> <span class="n">prime</span><span class="p"> [ </span> <span class="n">p</span><span class="p">]:</span>
        <span class="n">numbers</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">p</span><span class="p">)</span>

<span class="k">return</span> <span class="n">numbers</span>

</code>
</pre>


<p>Notes:</p>
<ul>
<li><code>make_request</code> makes an HTTP request to <a href="https://httpbin.org/ip">https://httpbin.org/ip</a> X number of times.</li>
<li><code>make_request_async</code> makes the same HTTP request asynchronously with <a href="https://www.python-httpx.org/">HTTPX</a>.</li>
<li><code>get_prime_numbers</code> calculates the prime numbers, via the <a href="https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes">Sieve of Eratosthenes</a> method, from two to the provided limit.</li>
</ul>
<p>We'll be using the following libraries from the standard library to speed up the above tasks:</p>
<ul>
<li><a href="https://docs.python.org/3/library/threading.html">threading</a> for running tasks concurrently</li>
<li><a href="https://docs.python.org/3/library/multiprocessing.html">multiprocessing</a> for running tasks in parallel</li>
<li><a href="https://docs.python.org/3/library/concurrent.futures.html">concurrent.futures</a> for running tasks concurrently and in parallel from a single interface</li>
<li><a href="https://docs.python.org/3/library/asyncio.html">asyncio</a> for running tasks concurrency with <a href="https://en.wikipedia.org/wiki/Coroutine">coroutines</a> managed by the Python interpreter</li>
</ul>
<table>
<thead>
<tr>
<th>Library</th>
<th>Class/Method</th>
<th>Processing Type</th>
</tr>
</thead>
<tbody>
<tr>
<td>threading</td>
<td><a href="https://docs.python.org/3/library/threading.html#threading.Thread">Thread</a></td>
<td>concurrent</td>
</tr>
<tr>
<td>concurrent.futures</td>
<td><a href="https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor">ThreadPoolExecutor</a></td>
<td>concurrent</td>
</tr>
<tr>
<td>asyncio</td>
<td><a href="https://docs.python.org/3/library/asyncio-task.html#asyncio.gather">gather</a></td>
<td>concurrent (via coroutines)</td>
</tr>
<tr>
<td>multiprocessing</td>
<td><a href="https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool">Pool</a></td>
<td>parallel</td>
</tr>
<tr>
<td>concurrent.futures</td>
<td><a href="https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor">ProcessPoolExecutor</a></td>
<td>parallel</td>
</tr>
</tbody>
</table>
<h2 id="io-bound-operation">IO-bound Operation</h2>
<p>Again, IO-bound tasks spend more time on IO than on the CPU.</p>
<p>Since web scraping is IO bound, we should use threading to speed up the processing as the retrieving of the HTML (IO) is slower than parsing it (CPU).</p>
<p>Scenario: <em>How to speed up a Python-based web scraping and crawling script?</em></p>
<h3 id="sync-example">Sync Example</h3>
<p>Let's start with a benchmark.</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># io-bound_sync.py</span>

<span class="kn">import</span> <span class="nn">time</span>

<span class="kn">from</span> <span class="nn">tasks</span> <span class="kn">import</span> <span class="n">make_request</span>

<span class="k">def</span> <span class="nf">main</span><span class="p">():</span>
<span class="k">for</span> <span class="n">num</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">101</span><span class="p">):</span>
<span class="n">make_request</span><span class="p">(</span><span class="n">num</span><span class="p">)</span>

<span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&quot;__main__&quot;</span><span class="p">:</span>
<span class="n">start_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>

<span class="n">main</span><span class="p">()</span>

<span class="n">end_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;Elapsed run time: </span><span class="si">{</span><span class="n">end_time</span> <span class="o">-</span> <span class="n">start_time</span><span class="si">}</span><span class="s2"> seconds.&quot;</span><span class="p">)</span>

</code></pre></div>

<p>Here, we made 100 HTTP requests using the <code>make_request</code> function. Since requests happen synchronously, each task is executed sequentially.</p>
<div class="codehilite"><pre><span></span><code>Elapsed run time: 15.710984757 seconds.
</code></pre></div>

<p>So, that's roughly 0.16 seconds per request.</p>
<h3 id="threading-example">Threading Example</h3>
<div class="codehilite"><pre><span></span><code><span class="c1"># io-bound_concurrent_1.py</span>

<span class="kn">import</span> <span class="nn">threading</span>
<span class="kn">import</span> <span class="nn">time</span>

<span class="kn">from</span> <span class="nn">tasks</span> <span class="kn">import</span> <span class="n">make_request</span>

<span class="k">def</span> <span class="nf">main</span><span class="p">():</span>
<span class="n">tasks</span> <span class="o">=</span> <span class="p">[]</span>

<span class="k">for</span> <span class="n">num</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">101</span><span class="p">):</span>
    <span class="n">tasks</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">threading</span><span class="o">.</span><span class="n">Thread</span><span class="p">(</span><span class="n">target</span><span class="o">=</span><span class="n">make_request</span><span class="p">,</span> <span class="n">args</span><span class="o">=</span><span class="p">(</span><span class="n">num</span><span class="p">,)))</span>
    <span class="n">tasks</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span><span class="o">.</span><span class="n">start</span><span class="p">()</span>

<span class="k">for</span> <span class="n">task</span> <span class="ow">in</span> <span class="n">tasks</span><span class="p">:</span>
    <span class="n">task</span><span class="o">.</span><span class="n">join</span><span class="p">()</span>

<span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&quot;__main__&quot;</span><span class="p">:</span>
<span class="n">start_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>

<span class="n">main</span><span class="p">()</span>

<span class="n">end_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;Elapsed run time: </span><span class="si">{</span><span class="n">end_time</span> <span class="o">-</span> <span class="n">start_time</span><span class="si">}</span><span class="s2"> seconds.&quot;</span><span class="p">)</span>

</code></pre></div>

<p>Here, the same <code>make_request</code> function is called 100 times. This time the <code>threading</code> library is used to create a thread for each request.</p>
<div class="codehilite"><pre><span></span><code>Elapsed run time: 1.020112515 seconds.
</code></pre></div>

<p>The total time decreases from ~16s to ~1s.</p>
<p>Since we're using separate threads for each request, you might be wondering why the whole thing didn't take ~0.16s to finish. This extra time is the overhead for managing threads. The <a href="https://wiki.python.org/moin/GlobalInterpreterLock">Global Interpreter Lock</a> (GIL) in Python makes sure that only one thread uses the Python bytecode at a time.</p>
<h3 id="concurrentfutures-example">concurrent.futures Example</h3>
<div class="codehilite"><pre><span></span><code><span class="c1"># io-bound_concurrent_2.py</span>

<span class="kn">import</span> <span class="nn">time</span>
<span class="kn">from</span> <span class="nn">concurrent.futures</span> <span class="kn">import</span> <span class="n">ThreadPoolExecutor</span><span class="p">,</span> <span class="n">wait</span>

<span class="kn">from</span> <span class="nn">tasks</span> <span class="kn">import</span> <span class="n">make_request</span>

<span class="k">def</span> <span class="nf">main</span><span class="p">():</span>
<span class="n">futures</span> <span class="o">=</span> <span class="p">[]</span>

<span class="k">with</span> <span class="n">ThreadPoolExecutor</span><span class="p">()</span> <span class="k">as</span> <span class="n">executor</span><span class="p">:</span>
    <span class="k">for</span> <span class="n">num</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">101</span><span class="p">):</span>
        <span class="n">futures</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">executor</span><span class="o">.</span><span class="n">submit</span><span class="p">(</span><span class="n">make_request</span><span class="p">,</span> <span class="n">num</span><span class="p">))</span>

<span class="n">wait</span><span class="p">(</span><span class="n">futures</span><span class="p">)</span>

<span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&quot;__main__&quot;</span><span class="p">:</span>
<span class="n">start_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>

<span class="n">main</span><span class="p">()</span>

<span class="n">end_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;Elapsed run time: </span><span class="si">{</span><span class="n">end_time</span> <span class="o">-</span> <span class="n">start_time</span><span class="si">}</span><span class="s2"> seconds.&quot;</span><span class="p">)</span>

</code></pre></div>

<p>Here we used <code>concurrent.futures.ThreadPoolExecutor</code> to achieve multithreading. After all the futures/promises are created, we used <code>wait</code> to wait for all of them to complete.</p>
<div class="codehilite"><pre><span></span><code>Elapsed run time: 1.340592231 seconds
</code></pre></div>

<p><code>concurrent.futures.ThreadPoolExecutor</code> is actually an abstraction around the <code>multithreading</code> library, which makes it easier to use. In the previous example, we assigned each request to a thread and in total 100 threads were used. But <code>ThreadPoolExecutor</code> defaults the number of worker threads to <code>min(32, os.cpu_count() + 4)</code>. ThreadPoolExecutor exists to ease the process of achieving multithreading. If you want more control over multithreading, use the <code>multithreading</code> library instead.</p>
<h3 id="asyncio-example">AsyncIO Example</h3>
<div class="codehilite"><pre><span></span><code><span class="c1"># io-bound_concurrent_3.py</span>

<span class="kn">import</span> <span class="nn">asyncio</span>
<span class="kn">import</span> <span class="nn">time</span>

<span class="kn">import</span> <span class="nn">httpx</span>

<span class="kn">from</span> <span class="nn">tasks</span> <span class="kn">import</span> <span class="n">make_request_async</span>

<span class="k">async</span> <span class="k">def</span> <span class="nf">main</span><span class="p">():</span>
<span class="k">async</span> <span class="k">with</span> <span class="n">httpx</span><span class="o">.</span><span class="n">AsyncClient</span><span class="p">()</span> <span class="k">as</span> <span class="n">client</span><span class="p">:</span>
<span class="k">return</span> <span class="k">await</span> <span class="n">asyncio</span><span class="o">.</span><span class="n">gather</span><span class="p">(</span>
<span class="o">*</span><span class="p">[</span><span class="n">make_request_async</span><span class="p">(</span><span class="n">num</span><span class="p">,</span> <span class="n">client</span><span class="p">)</span> <span class="k">for</span> <span class="n">num</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">101</span><span class="p">)]</span>
<span class="p">)</span>

<span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&quot;__main__&quot;</span><span class="p">:</span>
<span class="n">start_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>

<span class="n">loop</span> <span class="o">=</span> <span class="n">asyncio</span><span class="o">.</span><span class="n">get_event_loop</span><span class="p">()</span>
<span class="n">loop</span><span class="o">.</span><span class="n">run_until_complete</span><span class="p">(</span><span class="n">main</span><span class="p">())</span>

<span class="n">end_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>
<span class="n">elapsed_time</span> <span class="o">=</span> <span class="n">end_time</span> <span class="o">-</span> <span class="n">start_time</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;Elapsed run time: </span><span class="si">{</span><span class="n">elapsed_time</span><span class="si">}</span><span class="s2"> seconds&quot;</span><span class="p">)</span>

</code></pre></div>

<p>Here, we used <code>asyncio</code> to achieve concurrency.</p>
<div class="codehilite"><pre><span></span><code>Elapsed run time: 0.553961068 seconds
</code></pre></div>

<p><code>asyncio</code> is faster than the other methods, because <code>threading</code> makes use of OS (Operating System) threads. So the threads are managed by the OS, where thread switching is preempted by the OS. <code>asyncio</code> uses coroutines, which are defined by the Python interpreter. With coroutines, the program decides when to switch tasks in an optimal way. This is handled by the <code>even_loop</code> in asyncio.</p>
<h2 id="cpu-bound-operation">CPU-bound Operation</h2>
<p>Scenario: <em>How to speed up a simple data processing script?</em></p>
<h3 id="sync-example_1">Sync Example</h3>
<p>Again, let's start with a benchmark.</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># cpu-bound_sync.py</span>

<span class="kn">import</span> <span class="nn">time</span>

<span class="kn">from</span> <span class="nn">tasks</span> <span class="kn">import</span> <span class="n">get_prime_numbers</span>

<span class="k">def</span> <span class="nf">main</span><span class="p">():</span>
<span class="k">for</span> <span class="n">num</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1000</span><span class="p">,</span> <span class="mi">16000</span><span class="p">):</span>
<span class="n">get_prime_numbers</span><span class="p">(</span><span class="n">num</span><span class="p">)</span>

<span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&quot;__main__&quot;</span><span class="p">:</span>
<span class="n">start_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>

<span class="n">main</span><span class="p">()</span>

<span class="n">end_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;Elapsed run time: </span><span class="si">{</span><span class="n">end_time</span> <span class="o">-</span> <span class="n">start_time</span><span class="si">}</span><span class="s2"> seconds.&quot;</span><span class="p">)</span>

</code></pre></div>

<p>Here, we executed the <code>get_prime_numbers</code> function for numbers from 1000 to 16000.</p>
<div class="codehilite"><pre><span></span><code>Elapsed run time: 17.863046316 seconds.
</code></pre></div>

<h3 id="multiprocessing-example">Multiprocessing Example</h3>
<div class="codehilite"><pre><span></span><code><span class="c1"># cpu-bound_parallel_1.py</span>

<span class="kn">import</span> <span class="nn">time</span>
<span class="kn">from</span> <span class="nn">multiprocessing</span> <span class="kn">import</span> <span class="n">Pool</span><span class="p">,</span> <span class="n">cpu_count</span>

<span class="kn">from</span> <span class="nn">tasks</span> <span class="kn">import</span> <span class="n">get_prime_numbers</span>

<span class="k">def</span> <span class="nf">main</span><span class="p">():</span>
<span class="k">with</span> <span class="n">Pool</span><span class="p">(</span><span class="n">cpu_count</span><span class="p">()</span> <span class="o">-</span> <span class="mi">1</span><span class="p">)</span> <span class="k">as</span> <span class="n">p</span><span class="p">:</span>
<span class="n">p</span><span class="o">.</span><span class="n">starmap</span><span class="p">(</span><span class="n">get_prime_numbers</span><span class="p">,</span> <span class="nb">zip</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="mi">1000</span><span class="p">,</span> <span class="mi">16000</span><span class="p">)))</span>
<span class="n">p</span><span class="o">.</span><span class="n">close</span><span class="p">()</span>
<span class="n">p</span><span class="o">.</span><span class="n">join</span><span class="p">()</span>

<span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&quot;__main__&quot;</span><span class="p">:</span>
<span class="n">start_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>

<span class="n">main</span><span class="p">()</span>

<span class="n">end_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;Elapsed run time: </span><span class="si">{</span><span class="n">end_time</span> <span class="o">-</span> <span class="n">start_time</span><span class="si">}</span><span class="s2"> seconds.&quot;</span><span class="p">)</span>

</code></pre></div>

<p>Here, we used <code>multiprocessing</code> to calculate the prime numbers.</p>
<div class="codehilite"><pre><span></span><code>Elapsed run time: 2.9848740599999997 seconds.
</code></pre></div>

<h3 id="concurrentfutures-example_1">concurrent.futures Example</h3>
<div class="codehilite"><pre><span></span><code><span class="c1"># cpu-bound_parallel_2.py</span>

<span class="kn">import</span> <span class="nn">time</span>
<span class="kn">from</span> <span class="nn">concurrent.futures</span> <span class="kn">import</span> <span class="n">ProcessPoolExecutor</span><span class="p">,</span> <span class="n">wait</span>
<span class="kn">from</span> <span class="nn">multiprocessing</span> <span class="kn">import</span> <span class="n">cpu_count</span>

<span class="kn">from</span> <span class="nn">tasks</span> <span class="kn">import</span> <span class="n">get_prime_numbers</span>

<span class="k">def</span> <span class="nf">main</span><span class="p">():</span>
<span class="n">futures</span> <span class="o">=</span> <span class="p">[]</span>

<span class="k">with</span> <span class="n">ProcessPoolExecutor</span><span class="p">(</span><span class="n">cpu_count</span><span class="p">()</span> <span class="o">-</span> <span class="mi">1</span><span class="p">)</span> <span class="k">as</span> <span class="n">executor</span><span class="p">:</span>
    <span class="k">for</span> <span class="n">num</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1000</span><span class="p">,</span> <span class="mi">16000</span><span class="p">):</span>
        <span class="n">futures</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">executor</span><span class="o">.</span><span class="n">submit</span><span class="p">(</span><span class="n">get_prime_numbers</span><span class="p">,</span> <span class="n">num</span><span class="p">))</span>

<span class="n">wait</span><span class="p">(</span><span class="n">futures</span><span class="p">)</span>

<span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&quot;__main__&quot;</span><span class="p">:</span>
<span class="n">start_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>

<span class="n">main</span><span class="p">()</span>

<span class="n">end_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;Elapsed run time: </span><span class="si">{</span><span class="n">end_time</span> <span class="o">-</span> <span class="n">start_time</span><span class="si">}</span><span class="s2"> seconds.&quot;</span><span class="p">)</span>

</code></pre></div>

<p>Here, we achieved multiprocessing using <code>concurrent.futures.ProcessPoolExecutor</code>. Once the jobs are added to futures, <code>wait(futures)</code> waits for them to finish.</p>
<div class="codehilite"><pre><span></span><code>Elapsed run time: 4.452427557 seconds.
</code></pre></div>

<p><code>concurrent.futures.ProcessPoolExecutor</code> is a wrapper around <code>multiprocessing.Pool</code>. It has the same limitations as the <code>ThreadPoolExecutor</code>. If you want more control over multiprocessing, use <code>multiprocessing.Pool</code>. <code>concurrent.futures</code> provides an abstraction over both multiprocessing and threading, making it easy to switch between the two.</p>
<h2 id="conclusion">Conclusion</h2>
<p>It's worth noting that using multiprocessing to execute the <code>make_request</code> function will be much slower than the threading flavor since the processes will be need to wait for the IO. The multiprocessing approach will be faster then the sync approach, though.</p>
<p>Similarly, using concurrency for CPU-bound tasks is not worth the effort when compared to parallelism.</p>
<p>That being said, using concurrency or parallelism to execute your scripts adds complexity. Your code will generally be harder to read, test, and debug, so only use them when absolutely necessary for long-running scripts.</p>
<p><code>concurrent.futures</code> is where I generally start since-</p>
<ol>
<li>It's easy to switch back and forth between concurrency and parallelism</li>
<li>The dependent libraries don't need to support asyncio (<code>requests</code> vs <code>httpx</code>)</li>
<li>It's cleaner and easier to read over the other approaches</li>
</ol>
