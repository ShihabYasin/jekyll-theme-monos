---
layout: post
title: Django Caching
date: 2019-03-16 16:20:23 +0900
category: Django
tag: Django
---


<h2 id="django-caching-types">Django Caching Types</h2>
<p> Check codebase  <a href="https://github.com/ShihabYasin/simple-django-view-caching">here</a></p>
<p>Django comes with several <a href="https://docs.djangoproject.com/en/3.2/topics/cache/">built-in caching</a> backends, as well as support for a <a href="https://docs.djangoproject.com/en/3.2/topics/cache/#using-a-custom-cache-backend">custom</a> backend.</p>
<p>The built-in options are:</p>
<ol>
<li><strong>Memcached</strong>: <a href="https://memcached.org/">Memcached</a> is a memory-based, key-value store for small chunks of data. It supports distributed caching across multiple servers.</li>
<li><strong>Database</strong>: Here, the cache fragments are stored in a database. A table for that purpose can be created with one of the Django's admin commands. This isn't the most performant caching type, but it can be useful for storing complex database queries.</li>
<li><strong>File system</strong>: The cache is saved on the file system, in separate files for each cache value. This is the slowest of all the caching types, but it's the easiest to set up in a production environment.</li>
<li><strong>Local memory</strong>: Local memory cache, which is best-suited for your local development or testing environments. While it's almost as fast as Memcached, it cannot scale beyond a single server, so it's not appropriate to use as a data cache for any app that uses more than one web server.</li>
<li><strong>Dummy</strong>: A "dummy" cache that doesn't actually cache anything but still implements the cache interface. It's meant to be used in development or testing when you don't want caching, but do not wish to change your code.</li>
</ol>
<li><strong>Memcached</strong>: <a href="https://memcached.org/">Memcached</a> is a memory-based, key-value store for small chunks of data. It supports distributed caching across multiple servers.</li>
<li><strong>Database</strong>: Here, the cache fragments are stored in a database. A table for that purpose can be created with one of the Django's admin commands. This isn't the most performant caching type, but it can be useful for storing complex database queries.</li>
<li><strong>File system</strong>: The cache is saved on the file system, in separate files for each cache value. This is the slowest of all the caching types, but it's the easiest to set up in a production environment.</li>
<li><strong>Local memory</strong>: Local memory cache, which is best-suited for your local development or testing environments. While it's almost as fast as Memcached, it cannot scale beyond a single server, so it's not appropriate to use as a data cache for any app that uses more than one web server.</li>
<li><strong>Dummy</strong>: A "dummy" cache that doesn't actually cache anything but still implements the cache interface. It's meant to be used in development or testing when you don't want caching, but do not wish to change your code.</li>
<h2 id="django-caching-levels">Django Caching Levels</h2>
<p>Caching in Django can be implemented on different levels (or parts of the site). You can cache the entire site or specific parts with various levels of granularity (listed in descending order of granularity):</p>
<li><a href="https://docs.djangoproject.com/en/3.2/topics/cache/#the-per-site-cache">Per-site</a> cache</li>
<li><a href="https://docs.djangoproject.com/en/3.2/topics/cache/#the-per-view-cache">Per-view</a> cache</li>
<li><a href="https://docs.djangoproject.com/en/3.2/topics/cache/#template-fragment-caching">Template fragment</a> cache</li>
<li><a href="https://docs.djangoproject.com/en/3.2/topics/cache/#the-low-level-cache-api">Low-level</a> cache API</li>
<h3 id="per-site-cache">Per-site cache</h3>
<p>This is the easiest way to implement caching in Django. To do this, all you'll have to do is add two middleware classes to your <em>settings.py</em> file:</p>
<pre><span></span><code><span class="n">MIDDLEWARE</span> <span class="o">=</span> <span class="p">[</span>
<span class="s1">'django.middleware.cache.UpdateCacheMiddleware'</span><span class="p">,</span>     <span class="c1"># NEW</span>
<span class="s1">'django.middleware.common.CommonMiddleware'</span><span class="p">,</span>
<span class="s1">'django.middleware.cache.FetchFromCacheMiddleware'</span><span class="p">,</span>  <span class="c1"># NEW</span>
<span class="p">]</span>
</code></pre>
<p>The order of the middleware is important here. <code>UpdateCacheMiddleware</code> must come before <code>FetchFromCacheMiddleware</code>. For more information take a look at <a href="https://docs.djangoproject.com/en/3.2/topics/cache/#order-of-middleware">Order of MIDDLEWARE</a> from the Django docs.</p>
<p>You then need to add the following settings:</p>
<pre><span></span><code><span class="n">CACHE_MIDDLEWARE_ALIAS</span> <span class="o">=</span> <span class="s1">'default'</span>  <span class="c1"># which cache alias to use</span>
<span class="n">CACHE_MIDDLEWARE_SECONDS</span> <span class="o">=</span> <span class="s1">'600'</span>    <span class="c1"># number of seconds to cache a page for (TTL)</span>
<span class="n">CACHE_MIDDLEWARE_KEY_PREFIX</span> <span class="o">=</span> <span class="s1">''</span>    <span class="c1"># should be used if the cache is shared across multiple sites that use the same Django instance</span>
</code></pre>
<p>Although caching the entire site could be a good option if your site has little or no dynamic content, it may not be appropriate to use for large sites with a memory-based cache backend since RAM is, well, expensive.</p>
<h3 id="per-view-cache">Per-view cache</h3>
<p>Rather than wasting precious memory space on caching static pages or dynamic pages that source data from a rapidly changing API, you can cache specific views. This is the approach that we'll use in this article. <strong>It's also the caching level that you should almost always start with when looking to implement caching in your Django app.</strong></p>
<p>You can implement this type of cache with the <a href="https://docs.djangoproject.com/en/3.2/topics/cache/#django.views.decorators.cache.cache_page">cache_page</a> decorator either on the view function directly or in the path within <code>URLConf</code>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.views.decorators.cache</span> <span class="kn">import</span> <span class="n">cache_page</span>

<span class="nd">@cache_page</span><span class="p">(</span><span class="mi">60</span> <span class="o">*</span> <span class="mi">15</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">your_view</span><span class="p">(</span><span class="n">request</span><span class="p">):</span>
<span class="o">...</span>

<span class="c1"># or</span>

<span class="kn">from</span> <span class="nn">django.views.decorators.cache</span> <span class="kn">import</span> <span class="n">cache_page</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">path</span><span class="p">(</span><span class="s1">'object/&lt;int:object_id&gt;/'</span><span class="p">,</span> <span class="n">cache_page</span><span class="p">(</span><span class="mi">60</span> <span class="o">*</span> <span class="mi">15</span><span class="p">)(</span><span class="n">your_view</span><span class="p">)),</span>
<span class="p">]</span>
</code></pre>
<p>The cache itself is based on the URL, so requests to, say, <code>object/1</code> and <code>object/2</code> will be cached separately.</p>
<p>It's worth noting that implementing the cache directly on the view makes it more difficult to disable the cache in certain situations. For example, what if you wanted to allow certain users access to the view without the cache? Enabling the cache via the <code>URLConf</code> provides the opportunity to associate a different URL to the view that doesn't use the cache:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.views.decorators.cache</span> <span class="kn">import</span> <span class="n">cache_page</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">path</span><span class="p">(</span><span class="s1">'object/&lt;int:object_id&gt;/'</span><span class="p">,</span> <span class="n">your_view</span><span class="p">),</span>
<span class="n">path</span><span class="p">(</span><span class="s1">'object/cache/&lt;int:object_id&gt;/'</span><span class="p">,</span> <span class="n">cache_page</span><span class="p">(</span><span class="mi">60</span> <span class="o">*</span> <span class="mi">15</span><span class="p">)(</span><span class="n">your_view</span><span class="p">)),</span>
<span class="p">]</span>
</code></pre>
<h3 id="template-fragment-cache">Template fragment cache</h3>
<p>If your templates contain parts that change often based on the data you'll probably want to leave them out of the cache.</p>
<p>For example, perhaps you use the authenticated user's email in the navigation bar in an area of the template. Well, If you have thousands of users then that fragment will be duplicated thousands of times in RAM, one for each user. This is where template fragment caching comes into play, which allows you to specify the specific areas of a template to cache.</p>
<p>To cache a list of objects:</p>
<pre><span></span><code><span class="cp">{%</span> <span class="k">load</span> <span class="nv">cache</span> <span class="cp">%}</span>

<span class="cp">{%</span> <span class="k">cache</span> <span class="m">500</span> <span class="nv">object_list</span> <span class="cp">%}</span>
<span class="nt">&lt;ul&gt;</span>
<span class="cp">{%</span> <span class="k">for</span> <span class="nv">object</span> <span class="k">in</span> <span class="nv">objects</span> <span class="cp">%}</span>
<span class="nt">&lt;li&gt;</span><span class="cp">{{</span> <span class="nv">object.title</span> <span class="cp">}}</span><span class="nt">&lt;/li&gt;</span>
<span class="cp">{%</span> <span class="k">endfor</span> <span class="cp">%}</span>
<span class="nt">&lt;/ul&gt;</span>
<span class="cp">{%</span> <span class="k">endcache</span> <span class="cp">%}</span>
</code></pre>
<p>Here, <code>{% load cache %}</code> gives us access to the <code>cache</code> template tag, which expects a cache timeout in seconds (<code>500</code>) along with the name of the cache fragment (<code>object_list</code>).</p>
<h3 id="low-level-cache-api">Low-level cache API</h3>
<p>For cases where the previous options don't provide enough granularity, you can use the low-level API to manage individual objects in the cache by cache key.</p>
<p>For example:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.core.cache</span> <span class="kn">import</span> <span class="n">cache</span>


<span class="k">def</span> <span class="nf">get_context_data</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="n">context</span> <span class="o">=</span> <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">get_context_data</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>

<span class="n">objects</span> <span class="o">=</span> <span class="n">cache</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">'objects'</span><span class="p">)</span>

<span class="k">if</span> <span class="n">objects</span> <span class="ow">is</span> <span class="kc">None</span><span class="p">:</span>
<span class="n">objects</span> <span class="o">=</span> <span class="n">Objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>
<span class="n">cache</span><span class="o">.</span><span class="n">set</span><span class="p">(</span><span class="s1">'objects'</span><span class="p">,</span> <span class="n">objects</span><span class="p">)</span>

<span class="n">context</span><span class="p">[</span><span class="s1">'objects'</span><span class="p">]</span> <span class="o">=</span> <span class="n">objects</span>

<span class="k">return</span> <span class="n">context</span>
</code></pre>
<p>In this example, you'll want to invalidate (or remove) the cache when objects are added, changed, or removed from the database. One way to manage this is via database signals:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.core.cache</span> <span class="kn">import</span> <span class="n">cache</span>
<span class="kn">from</span> <span class="nn">django.db.models.signals</span> <span class="kn">import</span> <span class="n">post_delete</span><span class="p">,</span> <span class="n">post_save</span>
<span class="kn">from</span> <span class="nn">django.dispatch</span> <span class="kn">import</span> <span class="n">receiver</span>


<span class="nd">@receiver</span><span class="p">(</span><span class="n">post_delete</span><span class="p">,</span> <span class="n">sender</span><span class="o">=</span><span class="n">Object</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">object_post_delete_handler</span><span class="p">(</span><span class="n">sender</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="n">cache</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">'objects'</span><span class="p">)</span>


<span class="nd">@receiver</span><span class="p">(</span><span class="n">post_save</span><span class="p">,</span> <span class="n">sender</span><span class="o">=</span><span class="n">Object</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">object_post_save_handler</span><span class="p">(</span><span class="n">sender</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="n">cache</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">'objects'</span><span class="p">)</span>
</code></pre>

<h2 id="project-setup">Project Setup</h2>
<p>Check code to clone <a href="https://github.com/ShihabYasin/simple-django-view-caching">cache-django-view</a> repo, and then check out the base branch:</p>
<pre><span></span><code>$ git clone https://github.com/ShihabYasin/simple-django-view-caching.git --branch base --single-branch
$ <span class="nb">cd</span> cache-django-view
</code></pre>
<p>Create (and activate) a virtual environment and install the requirements:</p>
<pre><span></span><code>$ python3.9 -m venv venv
$ <span class="nb">source</span> venv/bin/activate
<span class="o">(</span>venv<span class="o">)</span>$ pip install -r requirements.txt
</code></pre>
<p>Apply the Django migrations, and then start the server:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ python manage.py migrate
<span class="o">(</span>venv<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>Navigate to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a> in your browser of choice to ensure that everything works as expected.</p>

<p>Take note of your terminal. You should see the total execution time for the request:</p>
<pre><span></span><code>Total time: <span class="m">2</span>.23s
</code></pre>
<p>This metric comes from <em>core/middleware.py</em>:</p>
<pre><span></span><code><span class="kn">import</span> <span class="nn">logging</span>
<span class="kn">import</span> <span class="nn">time</span>


<span class="k">def</span> <span class="nf">metric_middleware</span><span class="p">(</span><span class="n">get_response</span><span class="p">):</span>
<span class="k">def</span> <span class="nf">middleware</span><span class="p">(</span><span class="n">request</span><span class="p">):</span>
<span class="c1"># Get beginning stats</span>
<span class="n">start_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>

<span class="c1"># Process the request</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">get_response</span><span class="p">(</span><span class="n">request</span><span class="p">)</span>

<span class="c1"># Get ending stats</span>
<span class="n">end_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>

<span class="c1"># Calculate stats</span>
<span class="n">total_time</span> <span class="o">=</span> <span class="n">end_time</span> <span class="o">-</span> <span class="n">start_time</span>

<span class="c1"># Log the results</span>
<span class="n">logger</span> <span class="o">=</span> <span class="n">logging</span><span class="o">.</span><span class="n">getLogger</span><span class="p">(</span><span class="s1">'debug'</span><span class="p">)</span>
<span class="n">logger</span><span class="o">.</span><span class="n">info</span><span class="p">(</span><span class="sa">f</span><span class="s1">'Total time: </span><span class="si">{</span><span class="p">(</span><span class="n">total_time</span><span class="p">)</span><span class="si">:</span><span class="s1">.2f</span><span class="si">}</span><span class="s1">s'</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s1">'Total time: </span><span class="si">{</span><span class="p">(</span><span class="n">total_time</span><span class="p">)</span><span class="si">:</span><span class="s1">.2f</span><span class="si">}</span><span class="s1">s'</span><span class="p">)</span>

<span class="k">return</span> <span class="n">response</span>

<span class="k">return</span> <span class="n">middleware</span>
</code></pre>
<p>Take a quick look at the view in <em>apicalls/views.py</em>:</p>
<pre><span></span><code><span class="kn">import</span> <span class="nn">datetime</span>

<span class="kn">import</span> <span class="nn">requests</span>
<span class="kn">from</span> <span class="nn">django.views.generic</span> <span class="kn">import</span> <span class="n">TemplateView</span>


<span class="n">BASE_URL</span> <span class="o">=</span> <span class="s1">'https://httpbin.org/'</span>


<span class="k">class</span> <span class="nc">ApiCalls</span><span class="p">(</span><span class="n">TemplateView</span><span class="p">):</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s1">'apicalls/home.html'</span>

<span class="k">def</span> <span class="nf">get_context_data</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="n">context</span> <span class="o">=</span> <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">get_context_data</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">requests</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="sa">f</span><span class="s1">'</span><span class="si">{</span><span class="n">BASE_URL</span><span class="si">}</span><span class="s1">/delay/2'</span><span class="p">)</span>
<span class="n">response</span><span class="o">.</span><span class="n">raise_for_status</span><span class="p">()</span>
<span class="n">context</span><span class="p">[</span><span class="s1">'content'</span><span class="p">]</span> <span class="o">=</span> <span class="s1">'Results received!'</span>
<span class="n">context</span><span class="p">[</span><span class="s1">'current_time'</span><span class="p">]</span> <span class="o">=</span> <span class="n">datetime</span><span class="o">.</span><span class="n">datetime</span><span class="o">.</span><span class="n">now</span><span class="p">()</span>
<span class="k">return</span> <span class="n">context</span>
</code></pre>
<p>This view makes an HTTP call with <code>requests</code> to <a href="https://httpbin.org">httpbin.org</a>. To simulate a long request, the response from the API is delayed for two seconds. So, it should take about two seconds for <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a> to render not only on the initial request, but for each subsequent request as well. While a two second load is somewhat acceptable on the initial request, it's completely unacceptable for subsequent requests since the data is not changing. Let's fix this by caching the entire view using Django's Per-view cache level.</p>
<p>Workflow:</p>
<ol>
<li>Make full HTTP call to <a href="https://httpbin.org">httpbin.org</a> on the initial request</li>
<li>Cache the view</li>
<li>Subsequent requests will then pull from the cache, bypassing the HTTP call</li>
<li>Invalidate the cache after a period of time (TTL)</li>
</ol>
<li>Make full HTTP call to <a href="https://httpbin.org">httpbin.org</a> on the initial request</li>
<li>Cache the view</li>
<li>Subsequent requests will then pull from the cache, bypassing the HTTP call</li>
<li>Invalidate the cache after a period of time (TTL)</li>
<h2 id="baseline-performance-benchmark">Baseline Performance Benchmark</h2>
<p>Before adding cache, let's quickly run a load test to get a benchmark baseline using <a href="https://httpd.apache.org/docs/2.4/programs/ab.html">Apache Bench</a>, to get rough sense of how many requests our application can handle per second.</p>
<p>Apache Bench comes pre-installed on Mac.</p>
<p>If you're on a Linux system, chances are it's already installed and ready to go as well. If not, you can install via APT (<code>apt-get install apache2-utils</code>) or YUM (<code>yum install httpd-tools</code>).</p>
<p>Windows users will need to <a href="https://stackoverflow.com/questions/4314827/is-there-any-link-to-download-ab-apache-benchmark">download</a> and extract the Apache binaries.</p>
<p>Add <a href="https://gunicorn.org/">Gunicorn</a> to the requirements file:</p>
<pre><span></span><code>gunicorn==20.1.0
</code></pre>
<p>Kill the Django dev server and install Gunicorn:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ pip install -r requirements.txt
</code></pre>
<p>Next, serve up the Django app with Gunicorn (and four <a href="https://docs.gunicorn.org/en/stable/run.html#commonly-used-arguments">workers</a>) like so:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ gunicorn core.wsgi:application -w <span class="m">4</span>
</code></pre>
<p>In a new terminal window, run Apache Bench:</p>
<pre><span></span><code>$ ab -n <span class="m">100</span> -c <span class="m">10</span> http://127.0.0.1:8000/
</code></pre>
<p>This will simulate 100 connections over 10 concurrent threads. That's 100 requests, 10 at a time.</p>
<p>Take note of the requests per second:</p>
<pre><span></span><code>Requests per second:    <span class="m">1</span>.69 <span class="o">[</span><span class="c1">#/sec] (mean)</span>
</code></pre>
<p>Keep in mind that Django Debug Toolbar will add a bit of overhead. Benchmarking in general is difficult to get perfectly right. The important thing is consistency. Pick a metric to focus on and use the same environment for each test.</p>
<p>Kill the Gunicorn server and spin the Django dev server back up:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>With that, let's look at how to cache a view.</p>
<h2 id="caching-a-view">Caching a View</h2>
<p>Start by decorating the <code>ApiCalls</code> view with the <code>@cache_page</code> decorator like so:</p>
<pre><span></span><code><span class="kn">import</span> <span class="nn">datetime</span>

<span class="kn">import</span> <span class="nn">requests</span>
<span class="kn">from</span> <span class="nn">django.utils.decorators</span> <span class="kn">import</span> <span class="n">method_decorator</span> <span class="c1"># NEW</span>
<span class="kn">from</span> <span class="nn">django.views.decorators.cache</span> <span class="kn">import</span> <span class="n">cache_page</span> <span class="c1"># NEW</span>
<span class="kn">from</span> <span class="nn">django.views.generic</span> <span class="kn">import</span> <span class="n">TemplateView</span>


<span class="n">BASE_URL</span> <span class="o">=</span> <span class="s1">'https://httpbin.org/'</span>


<span class="nd">@method_decorator</span><span class="p">(</span><span class="n">cache_page</span><span class="p">(</span><span class="mi">60</span> <span class="o">*</span> <span class="mi">5</span><span class="p">),</span> <span class="n">name</span><span class="o">=</span><span class="s1">'dispatch'</span><span class="p">)</span> <span class="c1"># NEW</span>
<span class="k">class</span> <span class="nc">ApiCalls</span><span class="p">(</span><span class="n">TemplateView</span><span class="p">):</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s1">'apicalls/home.html'</span>

<span class="k">def</span> <span class="nf">get_context_data</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="n">context</span> <span class="o">=</span> <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">get_context_data</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">requests</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="sa">f</span><span class="s1">'</span><span class="si">{</span><span class="n">BASE_URL</span><span class="si">}</span><span class="s1">/delay/2'</span><span class="p">)</span>
<span class="n">response</span><span class="o">.</span><span class="n">raise_for_status</span><span class="p">()</span>
<span class="n">context</span><span class="p">[</span><span class="s1">'content'</span><span class="p">]</span> <span class="o">=</span> <span class="s1">'Results received!'</span>
<span class="n">context</span><span class="p">[</span><span class="s1">'current_time'</span><span class="p">]</span> <span class="o">=</span> <span class="n">datetime</span><span class="o">.</span><span class="n">datetime</span><span class="o">.</span><span class="n">now</span><span class="p">()</span>
<span class="k">return</span> <span class="n">context</span>
</code></pre>
<p>Since we're using a class-based view, we can't put the decorator directly on the class, so we used a <code>method_decorator</code> and specified <code>dispatch</code> (as the method to be decorated) for the name argument.</p>
<p>The cache in this example sets a timeout (or TTL) of five minutes.</p>
<p>Alternatively, you could set this in your settings like so:</p>
<pre><span></span><code><span class="c1"># Cache time to live is 5 minutes</span>
<span class="n">CACHE_TTL</span> <span class="o">=</span> <span class="mi">60</span> <span class="o">*</span> <span class="mi">5</span>
</code></pre>
<p>Then, back in the view:</p>
<pre><span></span><code><span class="kn">import</span> <span class="nn">datetime</span>

<span class="kn">import</span> <span class="nn">requests</span>
<span class="kn">from</span> <span class="nn">django.conf</span> <span class="kn">import</span> <span class="n">settings</span>
<span class="kn">from</span> <span class="nn">django.core.cache.backends.base</span> <span class="kn">import</span> <span class="n">DEFAULT_TIMEOUT</span>
<span class="kn">from</span> <span class="nn">django.utils.decorators</span> <span class="kn">import</span> <span class="n">method_decorator</span>
<span class="kn">from</span> <span class="nn">django.views.decorators.cache</span> <span class="kn">import</span> <span class="n">cache_page</span>
<span class="kn">from</span> <span class="nn">django.views.generic</span> <span class="kn">import</span> <span class="n">TemplateView</span>

<span class="n">BASE_URL</span> <span class="o">=</span> <span class="s1">'https://httpbin.org/'</span>
<span class="n">CACHE_TTL</span> <span class="o">=</span> <span class="nb">getattr</span><span class="p">(</span><span class="n">settings</span><span class="p">,</span> <span class="s1">'CACHE_TTL'</span><span class="p">,</span> <span class="n">DEFAULT_TIMEOUT</span><span class="p">)</span>


<span class="nd">@method_decorator</span><span class="p">(</span><span class="n">cache_page</span><span class="p">(</span><span class="n">CACHE_TTL</span><span class="p">),</span> <span class="n">name</span><span class="o">=</span><span class="s1">'dispatch'</span><span class="p">)</span>
<span class="k">class</span> <span class="nc">ApiCalls</span><span class="p">(</span><span class="n">TemplateView</span><span class="p">):</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s1">'apicalls/home.html'</span>

<span class="k">def</span> <span class="nf">get_context_data</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="n">context</span> <span class="o">=</span> <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">get_context_data</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">requests</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="sa">f</span><span class="s1">'</span><span class="si">{</span><span class="n">BASE_URL</span><span class="si">}</span><span class="s1">/delay/2'</span><span class="p">)</span>
<span class="n">response</span><span class="o">.</span><span class="n">raise_for_status</span><span class="p">()</span>
<span class="n">context</span><span class="p">[</span><span class="s1">'content'</span><span class="p">]</span> <span class="o">=</span> <span class="s1">'Results received!'</span>
<span class="n">context</span><span class="p">[</span><span class="s1">'current_time'</span><span class="p">]</span> <span class="o">=</span> <span class="n">datetime</span><span class="o">.</span><span class="n">datetime</span><span class="o">.</span><span class="n">now</span><span class="p">()</span>
<span class="k">return</span> <span class="n">context</span>
</code></pre>
<p>Next, let's add a cache backend.</p>
<h3 id="redis-vs-memcached">Redis vs Memcached</h3>
<p><a href="https://memcached.org/">Memcached</a> and <a href="https://redis.io/">Redis</a> are in-memory, key-value data stores. They are easy to use and optimized for high-performance lookups. You probably won't see much difference in performance or memory usage between the two. That said, Memcached is slightly easier to configure since it's designed for simplicity and ease of use. Redis, on the other hand, has a richer set of features so it has a wide range of use cases beyond caching. For example, it's often used to store user sessions or as message broker in a pub/sub system. Because of its flexibility, unless you're already invested in Memcached, Redis is much better solution.</p>

<p>Next, pick your data store of choice and let's look at how to cache a view.</p>
<h2 id="option-1-redis-with-django">Option 1: Redis with Django</h2>
<p><a href="https://redis.io/download">Download</a> and install Redis.</p>
<p>If you’re on a Mac, we recommend installing Redis with <a href="https://brew.sh/">Homebrew</a>:</p>
<pre><span></span>$ brew install redis
</pre>
<p>Once installed, in a new terminal window <a href="https://redis.io/topics/quickstart#starting-redis">start the Redis server</a> and make sure that it's running on its default port, 6379. The port number will be important when we tell Django how to communicate with Redis.</p>
<pre><span></span><code>$ redis-server
</code></pre>
<p>For Django to use Redis as a cache backend, we first need to install <a href="https://github.com/jazzband/django-redis">django-redis</a>.</p>
<p>Add it to the <em>requirements.txt</em> file:</p>
<pre><span></span><code>django-redis==5.0.0
</code></pre>
<p>Install:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ pip install -r requirements.txt
</code></pre>
<p>Next, add the custom backend to the <em>settings.py</em> file:</p>
<pre><span></span><code><span class="n">CACHES</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">'default'</span><span class="p">:</span> <span class="p">{</span>
<span class="s1">'BACKEND'</span><span class="p">:</span> <span class="s1">'django_redis.cache.RedisCache'</span><span class="p">,</span>
<span class="s1">'LOCATION'</span><span class="p">:</span> <span class="s1">'redis://127.0.0.1:6379/1'</span><span class="p">,</span>
<span class="s1">'OPTIONS'</span><span class="p">:</span> <span class="p">{</span>
<span class="s1">'CLIENT_CLASS'</span><span class="p">:</span> <span class="s1">'django_redis.client.DefaultClient'</span><span class="p">,</span>
<span class="p">}</span>
<span class="p">}</span>
<span class="p">}</span>
</code></pre>
<p>Now, when you run the server again, Redis will be used as the cache backend:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>With the server up and running, navigate to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a>.</p>
<p>The first request will still take about two seconds. Refresh the page. The page should load almost instantaneously. Take a look at the load time in your terminal. It should be close to zero:</p>
<pre><span></span><code>Total time: <span class="m">0</span>.01s
</code></pre>
<p>Curious what the cached data looks like inside of Redis?</p>
<p>Run Redis CLI in interactive mode in a new terminal window:</p>
<pre><span></span><code>$ redis-cli
</code></pre>
<p>You should see:</p>
<pre><span></span><code><span class="m">127</span>.0.0.1:6379&gt;
</code></pre>
<p>Run <code>ping</code> to ensure everything works properly:</p>
<pre><span></span><code><span class="m">127</span>.0.0.1:6379&gt; ping
PONG
</code></pre>
<p>Turn back to the settings file. We used Redis database number 1: <code>'LOCATION': 'redis://127.0.0.1:6379/1',</code>. So, run <code>select 1</code> to select that database and then run <code>keys *</code> to view all the keys:</p>
<pre><span></span><code><span class="m">127</span>.0.0.1:6379&gt; <span class="k">select</span> <span class="m">1</span>
OK

<span class="m">127</span>.0.0.1:6379<span class="o">[</span><span class="m">1</span><span class="o">]</span>&gt; keys *
<span class="m">1</span><span class="o">)</span> <span class="s2">":1:views.decorators.cache.cache_header..17abf5259517d604cc9599a00b7385d6.en-us.UTC"</span>
<span class="m">2</span><span class="o">)</span> <span class="s2">":1:views.decorators.cache.cache_page..GET.17abf5259517d604cc9599a00b7385d6.d41d8cd98f00b204e9800998ecf8427e.en-us.UTC"</span>
</code></pre>
<p>We can see that Django put in one header key and one <code>cache_page</code> key.</p>
<p>To view the actual cached data, run the <code>get</code> command with the key as an argument:</p>
<pre><span></span><code><span class="m">127</span>.0.0.1:6379<span class="o">[</span><span class="m">1</span><span class="o">]</span>&gt; get <span class="s2">":1:views.decorators.cache.cache_page..GET.17abf5259517d604cc9599a00b7385d6.d41d8cd98f00b204e9800998ecf8427e.en-us.UTC"</span>
</code></pre>
<p>Your should see something similar to:</p>
<pre><span></span><code><span class="s2">"\x80\x05\x95D\x04\x00\x00\x00\x00\x00\x00\x8c\x18django.template.response\x94\x8c\x10TemplateResponse</span>
<span class="s2">\x94\x93\x94)\x81\x94}\x94(\x8c\x05using\x94N\x8c\b_headers\x94}\x94(\x8c\x0ccontent-type\x94\x8c\</span>
<span class="s2">x0cContent-Type\x94\x8c\x18text/html; charset=utf-8\x94\x86\x94\x8c\aexpires\x94\x8c\aExpires\x94\x8c\x1d</span>
<span class="s2">Fri, 01 May 2020 13:36:59 GMT\x94\x86\x94\x8c\rcache-control\x94\x8c\rCache-Control\x94\x8c\x0</span>
<span class="s2">bmax-age=300\x94\x86\x94u\x8c\x11_resource_closers\x94]\x94\x8c\x0e_handler_class\x94N\x8c\acookies</span>
<span class="s2">\x94\x8c\x0chttp.cookies\x94\x8c\x0cSimpleCookie\x94\x93\x94)\x81\x94\x8c\x06closed\x94\x89\x8c</span>
<span class="s2">\x0e_reason_phrase\x94N\x8c\b_charset\x94N\x8c\n_container\x94]\x94B\xaf\x02\x00\x00</span>
<span class="s2">&lt;!DOCTYPE html&gt;\n&lt;html lang=\"en\"&gt;\n&lt;head&gt;\n    &lt;meta charset=\"UTF-8\"&gt;\n    &lt;title&gt;Home&lt;/title&gt;\n</span>
<span class="s2">&lt;link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css\</span>
<span class="s2">"</span><span class="se">\n</span>          <span class="nv">integrity</span><span class="o">=</span><span class="se">\"</span>sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh<span class="se">\"</span>
<span class="nv">crossorigin</span><span class="o">=</span><span class="se">\"</span>anonymous<span class="se">\"</span>&gt;<span class="se">\n\n</span>&lt;/head&gt;<span class="se">\n</span>&lt;body&gt;<span class="se">\n</span>&lt;div <span class="nv">class</span><span class="o">=</span><span class="se">\"</span>container<span class="se">\"</span>&gt;<span class="se">\n</span>    &lt;div <span class="nv">class</span><span class="o">=</span><span class="se">\"</span>pt-3<span class="se">\"</span>&gt;<span class="se">\n</span>
&lt;h1&gt;Below is the result of the APICall&lt;/h1&gt;<span class="se">\n</span>    &lt;/div&gt;<span class="se">\n</span>    &lt;div <span class="nv">class</span><span class="o">=</span><span class="se">\"</span>pt-3 pb-3<span class="se">\"</span>&gt;<span class="se">\n</span>
&lt;a <span class="nv">href</span><span class="o">=</span><span class="se">\"</span>/<span class="se">\"</span>&gt;<span class="se">\n</span>            &lt;button <span class="nv">type</span><span class="o">=</span><span class="se">\"</span>button<span class="se">\"</span> <span class="nv">class</span><span class="o">=</span><span class="se">\"</span>btn btn-success<span class="se">\"</span>&gt;<span class="se">\n</span>
Get new data<span class="se">\n</span>            &lt;/button&gt;<span class="se">\n</span>        &lt;/a&gt;<span class="se">\n</span>    &lt;/div&gt;<span class="se">\n</span>    Results received!&lt;br&gt;<span class="se">\n</span>
<span class="m">13</span>:31:59<span class="se">\n</span>&lt;/div&gt;<span class="se">\n</span>&lt;/body&gt;<span class="se">\n</span>&lt;/html&gt;<span class="se">\x</span>94a<span class="se">\x</span>8c<span class="se">\x</span>0c_is_rendered<span class="se">\x</span><span class="m">94</span><span class="se">\x</span>88ub.<span class="s2">"</span>
</code></pre>
<p>Exit the interactive CLI once done:</p>
<pre><span></span><code><span class="m">127</span>.0.0.1:6379<span class="o">[</span><span class="m">1</span><span class="o">]</span>&gt; <span class="nb">exit</span>
</code></pre>
<p>Skip down to the "Performance Tests" section.</p>
<h2 id="option-2-memcached-with-django">Option 2: Memcached with Django</h2>
<p>Start by adding <a href="https://pymemcache.readthedocs.io/">pymemcache</a> to the <em>requirements.txt</em> file:</p>
<pre><span></span><code>pymemcache==3.5.0
</code></pre>
<p>Install the dependencies:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ pip install -r requirements.txt
</code></pre>
<p>Next, we need to update the settings in <em>core/settings.py</em> to enable the Memcached backend:</p>
<pre><span></span><code><span class="n">CACHES</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">'default'</span><span class="p">:</span> <span class="p">{</span>
<span class="s1">'BACKEND'</span><span class="p">:</span> <span class="s1">'django.core.cache.backends.memcached.PyMemcacheCache'</span><span class="p">,</span>
<span class="s1">'LOCATION'</span><span class="p">:</span> <span class="s1">'127.0.0.1:11211'</span><span class="p">,</span>
<span class="p">}</span>
<span class="p">}</span>
</code></pre>
<p>Here, we added the <a href="https://docs.djangoproject.com/en/3.2/topics/cache/#memcached">PyMemcacheCache</a> backend and indicated that Memcached should be running on our local machine on localhost (127.0.0.1) port 11211, which is the default port for Memcached.</p>
<p>Next, we need to install and run the Memcached daemon. The easiest way to install it, is via a package manager like APT, YUM, Homebrew, or Chocolatey depending on your operating system:</p>
<pre><span></span><code><span class="c1"># linux</span>
$ apt-get install memcached
$ yum install memcached

<span class="c1"># mac</span>
$ brew install memcached

<span class="c1"># windows</span>
$ choco install memcached
</code></pre>
<p>Then, run it in a different terminal on port 11211:</p>
<pre><span></span><code>$ memcached -p <span class="m">11211</span>

<span class="c1"># test: telnet localhost 11211</span>
</code></pre>
<p>For more information on installation and configuration of Memcached, review the official <a href="https://github.com/memcached/memcached/wiki">wiki</a>.</p>
<p>Navigate to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a> in our browser again. The first request will still take the full two seconds, but all subsequent requests will take advantage of the cache. So, if you refresh or press the "Get new data button", the page should load almost instantly.</p>
<p>What's the execution time look like in your terminal?</p>
<pre><span></span><code>Total time: <span class="m">0</span>.03s
</code></pre>

<p>Spin Gunicorn back up again and re-run the performance tests:</p>
<pre><span></span><code>$ ab -n <span class="m">100</span> -c <span class="m">10</span> http://127.0.0.1:8000/
</code></pre>

