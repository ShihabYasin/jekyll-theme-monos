---
layout: post
title: How to Low Level Cache in Django
date: 2019-03-25 16:20:23 +0900
category: Django
tag: Django
---

<h2 id="project-setup">Low Level Cache in Django</h2>

<h2 id="project-setup">Project Setup</h2>
<p>Clone down the base project from the <a href="https://github.com/ShihabYasin/django-premitive-caching">django-low-level-cache</a> repo on GitHub:</p>
<pre><span></span><code>$ git clone -b base https://github.com/ShihabYasin/django-premitive-caching
$ <span class="nb">cd</span> django-low-level-cache
</code></pre>
<p>Create (and activate) a virtual environment and install the requirements:</p>
<pre><span></span><code>$ python3.9 -m venv venv
$ <span class="nb">source</span> venv/bin/activate
<span class="o">(</span>venv<span class="o">)</span>$ pip install -r requirements.txt
</code></pre>
<p>Apply the Django migrations, load some product data into the database, and the start the server:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ python manage.py migrate
<span class="o">(</span>venv<span class="o">)</span>$ python manage.py seed_db
<span class="o">(</span>venv<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>Navigate to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a> in your browser to check that everything works as expected.</p>

<h2 id="cache-backend">Cache Backend</h2>
<p>We'll be using <a href="https://redis.io">Redis</a> for the cache backend.</p>
<p><a href="https://redis.io/download">Download</a> and install Redis.</p>
<p>If you’re on a Mac, we recommend installing Redis with <a href="https://brew.sh/">Homebrew</a>:</p>
<pre><span></span>$ brew install redis
</pre>
<p>Once installed, in a new terminal window <a href="https://redis.io/topics/quickstart#starting-redis">start the Redis server</a> and make sure that it's running on its default port, 6379. The port number will be important when we tell Django how to communicate with Redis.</p>
<pre><span></span><code>$ redis-server
</code></pre>
<p>For Django to use Redis as a cache backend, the <a href="https://github.com/jazzband/django-redis">django-redis</a> dependency is required. It's already been installed, so you just need to add the custom backend to the <em>settings.py</em> file:</p>
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
<p>Turn to the code. The <code>HomePageView</code> view in <em>products/views.py</em> simply lists all products in the database:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">HomePageView</span><span class="p">(</span><span class="n">View</span><span class="p">):</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s1">'products/home.html'</span>

<span class="k">def</span> <span class="nf">get</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">request</span><span class="p">):</span>
<span class="n">product_objects</span> <span class="o">=</span> <span class="n">Product</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>

<span class="n">context</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">'products'</span><span class="p">:</span> <span class="n">product_objects</span>
<span class="p">}</span>

<span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">template_name</span><span class="p">,</span> <span class="n">context</span><span class="p">)</span>
</code></pre>
<p>Let's add support for the low-level cache API to the product objects.</p>
<p>First, add the import to the top of <em>products/views.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.core.cache</span> <span class="kn">import</span> <span class="n">cache</span>
</code></pre>
<p>Then, add the code for caching the products to the view:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">HomePageView</span><span class="p">(</span><span class="n">View</span><span class="p">):</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s1">'products/home.html'</span>

<span class="k">def</span> <span class="nf">get</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">request</span><span class="p">):</span>
<span class="n">product_objects</span> <span class="o">=</span> <span class="n">cache</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">'product_objects'</span><span class="p">)</span>      <span class="c1"># NEW</span>

<span class="k">if</span> <span class="n">product_objects</span> <span class="ow">is</span> <span class="kc">None</span><span class="p">:</span>                         <span class="c1"># NEW</span>
<span class="n">product_objects</span> <span class="o">=</span> <span class="n">Product</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>
<span class="n">cache</span><span class="o">.</span><span class="n">set</span><span class="p">(</span><span class="s1">'product_objects'</span><span class="p">,</span> <span class="n">product_objects</span><span class="p">)</span>   <span class="c1"># NEW</span>

<span class="n">context</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">'products'</span><span class="p">:</span> <span class="n">product_objects</span>
<span class="p">}</span>

<span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">template_name</span><span class="p">,</span> <span class="n">context</span><span class="p">)</span>
</code></pre>
<p>Here, we first checked to see if there's a cache object with the name <code>product_objects</code> in our default cache:</p>
<li>If so, we just returned it to the template without doing a database query.</li>
<li>If it's not found in our cache, we queried the database and added the result to the cache with the key <code>product_objects</code>.</li>
<p>With the server running, navigate to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a> in your browser. Click on "Cache" in the right-hand menu of <a href="https://django-debug-toolbar.readthedocs.io/">Django Debug Toolbar</a>. 
<p>There were two cache calls:</p>
<ol>
<li>The first call attempted to get the cache object named <code>product_objects</code>, resulting in a cache miss since the object doesn't exist.</li>
<li>The second call set the cache object, using the same name, with the result of the queryset of all products.</li>
</ol>
<li>The first call attempted to get the cache object named <code>product_objects</code>, resulting in a cache miss since the object doesn't exist.</li>
<li>The second call set the cache object, using the same name, with the result of the queryset of all products.</li>
<p>There was also one SQL query. Overall, the page took about 313 milliseconds to load.</p>
<p>Refresh the page in your browser.
<p>This time, you should see a cache hit, which gets the cache object named <code>product_objects</code>. Also, there were no SQL queries, and the page took about 234 milliseconds to load.</p>
<p>Try adding a new product, updating an existing product, and deleting a product. You won't see any of the changes at <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a> until you manually invalidate the cache, by pressing the "Invalidate cache" button.</p>
<h2 id="invalidating-the-cache">Invalidating the Cache</h2>
<p>Next let's look at how to automatically invalidate the cache. In the <a href="/blog/django-caching/">previous article</a>, we looked at how to invalidate the cache after a period of time (TTL). In this article, we'll look at how to invalidate the cache when something in the model changes -- e.g., when a product is added to the products table or when an existing product is either updated or deleted.</p>
<h3 id="using-django-signals">Using Django Signals</h3>
<p>For this task we could use database <a href="https://docs.djangoproject.com/en/3.2/topics/signals/">signals</a>:</p>
<p>Django includes a “signal dispatcher” which helps decoupled applications get notified when actions occur elsewhere in the framework. In a nutshell, signals allow certain senders to notify a set of receivers that some action has taken place. They’re especially useful when many pieces of code may be interested in the same events.</p>
<h3 id="saves-and-deletes">Saves and Deletes</h3>
<p>To set up signals for handling cache invalidation, start by updating <em>products/apps.py</em> like so:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.apps</span> <span class="kn">import</span> <span class="n">AppConfig</span>


<span class="k">class</span> <span class="nc">ProductsConfig</span><span class="p">(</span><span class="n">AppConfig</span><span class="p">):</span>
<span class="n">name</span> <span class="o">=</span> <span class="s1">'products'</span>

<span class="k">def</span> <span class="nf">ready</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>                <span class="c1"># NEW</span>
<span class="kn">import</span> <span class="nn">products.signals</span>     <span class="c1"># NEW</span>
</code></pre>
<p>Next, create a file called <em>signals.py</em> in the "products" directory:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.core.cache</span> <span class="kn">import</span> <span class="n">cache</span>
<span class="kn">from</span> <span class="nn">django.db.models.signals</span> <span class="kn">import</span> <span class="n">post_delete</span><span class="p">,</span> <span class="n">post_save</span>
<span class="kn">from</span> <span class="nn">django.dispatch</span> <span class="kn">import</span> <span class="n">receiver</span>

<span class="kn">from</span> <span class="nn">.models</span> <span class="kn">import</span> <span class="n">Product</span>


<span class="nd">@receiver</span><span class="p">(</span><span class="n">post_delete</span><span class="p">,</span> <span class="n">sender</span><span class="o">=</span><span class="n">Product</span><span class="p">,</span> <span class="n">dispatch_uid</span><span class="o">=</span><span class="s1">'post_deleted'</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">object_post_delete_handler</span><span class="p">(</span><span class="n">sender</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="n">cache</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">'product_objects'</span><span class="p">)</span>


<span class="nd">@receiver</span><span class="p">(</span><span class="n">post_save</span><span class="p">,</span> <span class="n">sender</span><span class="o">=</span><span class="n">Product</span><span class="p">,</span> <span class="n">dispatch_uid</span><span class="o">=</span><span class="s1">'posts_updated'</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">object_post_save_handler</span><span class="p">(</span><span class="n">sender</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="n">cache</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">'product_objects'</span><span class="p">)</span>
</code></pre>
<p>Here, we used the <code>receiver</code> decorator from <code>django.dispatch</code> to decorate two functions that get called when a product is added or deleted, respectively. Let's look at the arguments:</p>
<ol>
<li>The first argument is the signal event in which to tie the decorated function to, either a <code>save</code> or <code>delete</code>.</li>
<li>We also specified a sender, the <code>Product</code> model in which to receive signals from.</li>
<li>Finally, we passed a string as the <code>dispatch_uid</code> to <a href="https://docs.djangoproject.com/en/3.2/topics/signals/#preventing-duplicate-signals">prevent duplicate signals</a>.</li>
</ol>
<li>The first argument is the signal event in which to tie the decorated function to, either a <code>save</code> or <code>delete</code>.</li>
<li>We also specified a sender, the <code>Product</code> model in which to receive signals from.</li>
<li>Finally, we passed a string as the <code>dispatch_uid</code> to <a href="https://docs.djangoproject.com/en/3.2/topics/signals/#preventing-duplicate-signals">prevent duplicate signals</a>.</li>
<p>So, when either a save or delete occurs against the <code>Product</code> model, the <code>delete</code> method on the cache object is called to remove the contents of the <code>product_objects</code> cache.</p>
<p>To see this in action, either start or restart the server and navigate to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a> in your browser. Open the "Cache" tab in the Django Debug Toolbar. You should see one cache miss. Refresh, and you should have no cache misses and one cache hit. Close the Debug Toolbar page. Then, click the "New product" button to add a new product. You should be redirected back to the homepage after you click "Save". This time, you should see one cache miss, indicating that the signal worked. Also, your new product should be seen at the top of the product list.</p>
<h3 id="updates">Updates</h3>
<p>What about an update?</p>
<p>The <code>post_save</code> signal is triggered if you update an item like so:</p>
<pre><span></span><code><span class="n">product</span> <span class="o">=</span> <span class="n">Product</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="nb">id</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
<span class="n">product</span><span class="o">.</span><span class="n">title</span> <span class="o">=</span> <span class="s1">'A new title'</span>
<span class="n">product</span><span class="o">.</span><span class="n">save</span><span class="p">()</span>
</code></pre>
<p>However, <code>post_save</code> won't be triggered if you perform an <code>update</code> on the model via a <code>QuerySet</code>:</p>
<pre><span></span><code><span class="n">Product</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">filter</span><span class="p">(</span><span class="nb">id</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span><span class="o">.</span><span class="n">update</span><span class="p">(</span><span class="n">title</span><span class="o">=</span><span class="s1">'A new title'</span><span class="p">)</span>
</code></pre>
<p>Take note of the <code>ProductUpdateView</code>:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">ProductUpdateView</span><span class="p">(</span><span class="n">UpdateView</span><span class="p">):</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Product</span>
<span class="n">fields</span> <span class="o">=</span> <span class="p">[</span><span class="s1">'title'</span><span class="p">,</span> <span class="s1">'price'</span><span class="p">]</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s1">'products/product_update.html'</span>

<span class="c1"># we overrode the post method for testing purposes</span>
<span class="k">def</span> <span class="nf">post</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">request</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="bp">self</span><span class="o">.</span><span class="n">object</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">get_object</span><span class="p">()</span>
<span class="n">Product</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">filter</span><span class="p">(</span><span class="nb">id</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">object</span><span class="o">.</span><span class="n">id</span><span class="p">)</span><span class="o">.</span><span class="n">update</span><span class="p">(</span>
<span class="n">title</span><span class="o">=</span><span class="n">request</span><span class="o">.</span><span class="n">POST</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">'title'</span><span class="p">),</span>
<span class="n">price</span><span class="o">=</span><span class="n">request</span><span class="o">.</span><span class="n">POST</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">'price'</span><span class="p">)</span>
<span class="p">)</span>
<span class="k">return</span> <span class="n">HttpResponseRedirect</span><span class="p">(</span><span class="n">reverse_lazy</span><span class="p">(</span><span class="s1">'home'</span><span class="p">))</span>
</code></pre>
<p>So, in order to trigger the <code>post_save</code>, let's override the queryset <code>update()</code> method. Start by creating a custom <code>QuerySet</code> and a custom <code>Manager</code>. At the top of <em>products/models.py</em>, add the following lines:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.core.cache</span> <span class="kn">import</span> <span class="n">cache</span>             <span class="c1"># NEW</span>
<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>
<span class="kn">from</span> <span class="nn">django.db.models</span> <span class="kn">import</span> <span class="n">QuerySet</span><span class="p">,</span> <span class="n">Manager</span>  <span class="c1"># NEW</span>
<span class="kn">from</span> <span class="nn">django.utils</span> <span class="kn">import</span> <span class="n">timezone</span>               <span class="c1"># NEW</span>
</code></pre>
<p>Next, let's add the following code to <em>products/models.py</em> right above the <code>Product</code> class:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">CustomQuerySet</span><span class="p">(</span><span class="n">QuerySet</span><span class="p">):</span>
<span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="n">cache</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">'product_objects'</span><span class="p">)</span>
<span class="nb">super</span><span class="p">(</span><span class="n">CustomQuerySet</span><span class="p">,</span> <span class="bp">self</span><span class="p">)</span><span class="o">.</span><span class="n">update</span><span class="p">(</span><span class="n">updated</span><span class="o">=</span><span class="n">timezone</span><span class="o">.</span><span class="n">now</span><span class="p">(),</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>


<span class="k">class</span> <span class="nc">CustomManager</span><span class="p">(</span><span class="n">Manager</span><span class="p">):</span>
<span class="k">def</span> <span class="nf">get_queryset</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="n">CustomQuerySet</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">model</span><span class="p">,</span> <span class="n">using</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">_db</span><span class="p">)</span>
</code></pre>
<p>Here, we created a custom <code>Manager</code>, which has a single job: To return our custom <code>QuerySet</code>. In our custom <code>QuerySet</code>, we overrode the <code>update()</code> method to first delete the cache key and then perform the <code>QuerySet</code> update per usual.</p>
<p>For this to be used by our code, you also need to update <code>Product</code> like so:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">Product</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">title</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">200</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
<span class="n">price</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">20</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
<span class="n">created</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now_add</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="n">updated</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<span class="n">objects</span> <span class="o">=</span> <span class="n">CustomManager</span><span class="p">()</span>           <span class="c1"># NEW</span>

<span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
<span class="n">ordering</span> <span class="o">=</span> <span class="p">[</span><span class="s1">'-created'</span><span class="p">]</span>
</code></pre>
<p>Full file:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.core.cache</span> <span class="kn">import</span> <span class="n">cache</span>
<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>
<span class="kn">from</span> <span class="nn">django.db.models</span> <span class="kn">import</span> <span class="n">QuerySet</span><span class="p">,</span> <span class="n">Manager</span>
<span class="kn">from</span> <span class="nn">django.utils</span> <span class="kn">import</span> <span class="n">timezone</span>


<span class="k">class</span> <span class="nc">CustomQuerySet</span><span class="p">(</span><span class="n">QuerySet</span><span class="p">):</span>
<span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="n">cache</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">'product_objects'</span><span class="p">)</span>
<span class="nb">super</span><span class="p">(</span><span class="n">CustomQuerySet</span><span class="p">,</span> <span class="bp">self</span><span class="p">)</span><span class="o">.</span><span class="n">update</span><span class="p">(</span><span class="n">updated</span><span class="o">=</span><span class="n">timezone</span><span class="o">.</span><span class="n">now</span><span class="p">(),</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>


<span class="k">class</span> <span class="nc">CustomManager</span><span class="p">(</span><span class="n">Manager</span><span class="p">):</span>
<span class="k">def</span> <span class="nf">get_queryset</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="n">CustomQuerySet</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">model</span><span class="p">,</span> <span class="n">using</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">_db</span><span class="p">)</span>


<span class="k">class</span> <span class="nc">Product</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">title</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">200</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
<span class="n">price</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">20</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
<span class="n">created</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now_add</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="n">updated</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<span class="n">objects</span> <span class="o">=</span> <span class="n">CustomManager</span><span class="p">()</span>

<span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
<span class="n">ordering</span> <span class="o">=</span> <span class="p">[</span><span class="s1">'-created'</span><span class="p">]</span>
</code></pre>
<p>Test this out.</p>
<h3 id="using-django-lifecycle">Using Django Lifecycle</h3>
<p>Rather than using database signals, you could use a third-party package called <a href="https://rsinger86.github.io/django-lifecycle/">Django Lifecycle</a>, which helps make invalidation of cache easier and more readable:</p>
<p>This project provides a @hook decorator as well as a base model and mixin to add lifecycle hooks to your Django models. Django's built-in approach to offering lifecycle hooks is Signals. However, my team often finds that Signals introduce unnecessary indirection and are at odds with Django's "fat models" approach.</p>
<p>To switch to using Django Lifecycle, kill the server, and then update <em>products/app.py</em> like so:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.apps</span> <span class="kn">import</span> <span class="n">AppConfig</span>


<span class="k">class</span> <span class="nc">ProductsConfig</span><span class="p">(</span><span class="n">AppConfig</span><span class="p">):</span>
<span class="n">name</span> <span class="o">=</span> <span class="s1">'products'</span>
</code></pre>
<p>Next, add Django Lifecycle to <em>requirements.txt</em>:</p>
<pre><span></span><code><span class="n">Django</span><span class="o">==</span><span class="mf">3.1</span><span class="o">.</span><span class="mi">13</span><span class="w"></span>
<span class="n">django</span><span class="o">-</span><span class="n">debug</span><span class="o">-</span><span class="n">toolbar</span><span class="o">==</span><span class="mf">3.2</span><span class="o">.</span><span class="mi">1</span><span class="w"></span>
<span class="n">django</span><span class="o">-</span><span class="n">lifecycle</span><span class="o">==</span><span class="mf">0.9</span><span class="o">.</span><span class="mi">1</span><span class="w">         </span><span class="c1"># NEW</span><span class="w"></span>
<span class="n">django</span><span class="o">-</span><span class="n">redis</span><span class="o">==</span><span class="mf">5.0</span><span class="o">.</span><span class="mi">0</span><span class="w"></span>
<span class="n">redis</span><span class="o">==</span><span class="mf">3.5</span><span class="o">.</span><span class="mi">3</span><span class="w"></span>
</code></pre>
<p>Install the new requirements:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ pip install -r requirements.txt
</code></pre>
<p>To use Lifecycle hooks, update <em>products/models.py</em> like so:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.core.cache</span> <span class="kn">import</span> <span class="n">cache</span>
<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>
<span class="kn">from</span> <span class="nn">django.db.models</span> <span class="kn">import</span> <span class="n">QuerySet</span><span class="p">,</span> <span class="n">Manager</span>
<span class="kn">from</span> <span class="nn">django_lifecycle</span> <span class="kn">import</span> <span class="n">LifecycleModel</span><span class="p">,</span> <span class="n">hook</span><span class="p">,</span> <span class="n">AFTER_DELETE</span><span class="p">,</span> <span class="n">AFTER_SAVE</span>   <span class="c1"># NEW</span>
<span class="kn">from</span> <span class="nn">django.utils</span> <span class="kn">import</span> <span class="n">timezone</span>


<span class="k">class</span> <span class="nc">CustomQuerySet</span><span class="p">(</span><span class="n">QuerySet</span><span class="p">):</span>
<span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="n">cache</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">'product_objects'</span><span class="p">)</span>
<span class="nb">super</span><span class="p">(</span><span class="n">CustomQuerySet</span><span class="p">,</span> <span class="bp">self</span><span class="p">)</span><span class="o">.</span><span class="n">update</span><span class="p">(</span><span class="n">updated</span><span class="o">=</span><span class="n">timezone</span><span class="o">.</span><span class="n">now</span><span class="p">(),</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>


<span class="k">class</span> <span class="nc">CustomManager</span><span class="p">(</span><span class="n">Manager</span><span class="p">):</span>
<span class="k">def</span> <span class="nf">get_queryset</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="n">CustomQuerySet</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">model</span><span class="p">,</span> <span class="n">using</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">_db</span><span class="p">)</span>


<span class="k">class</span> <span class="nc">Product</span><span class="p">(</span><span class="n">LifecycleModel</span><span class="p">):</span>              <span class="c1"># NEW</span>
<span class="n">title</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">200</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
<span class="n">price</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">20</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
<span class="n">created</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now_add</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="n">updated</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<span class="n">objects</span> <span class="o">=</span> <span class="n">CustomManager</span><span class="p">()</span>

<span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
<span class="n">ordering</span> <span class="o">=</span> <span class="p">[</span><span class="s1">'-created'</span><span class="p">]</span>

<span class="nd">@hook</span><span class="p">(</span><span class="n">AFTER_SAVE</span><span class="p">)</span>                       <span class="c1"># NEW</span>
<span class="nd">@hook</span><span class="p">(</span><span class="n">AFTER_DELETE</span><span class="p">)</span>                     <span class="c1"># NEW</span>
<span class="k">def</span> <span class="nf">invalidate_cache</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>             <span class="c1"># NEW</span>
<span class="n">cache</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">'product_objects'</span><span class="p">)</span>      <span class="c1"># NEW</span>
</code></pre>
<p>In the code above, we:</p>
<ol>
<li>First imported the necessary objects from Django Lifecycle</li>
<li>Then inherited from <code>LifecycleModel</code> rather than <code>django.db.models</code></li>
<li>Created an <code>invalidate_cache</code> method that deletes the <code>product_object</code> cache key</li>
<li>Used the <code>@hook</code> decorators to specify the events that we want to "hook" into</li>
</ol>
<li>First imported the necessary objects from Django Lifecycle</li>
<li>Then inherited from <code>LifecycleModel</code> rather than <code>django.db.models</code></li>
<li>Created an <code>invalidate_cache</code> method that deletes the <code>product_object</code> cache key</li>
<li>Used the <code>@hook</code> decorators to specify the events that we want to "hook" into</li>
<p>Test this out in your browser by-</p>
<ol>
<li>Navigating to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a></li>
<li>Refreshing and verifying in the Debug Toolbar that there's a cache hit</li>
<li>Adding a product and verifying that there's now a cache miss</li>
</ol>
<li>Navigating to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a></li>
<li>Refreshing and verifying in the Debug Toolbar that there's a cache hit</li>
<li>Adding a product and verifying that there's now a cache miss</li>
<p>As with <code>django signals</code> the hooks won't trigger if we do update via a <code>QuerySet</code> like in the previously mentioned example:</p>
<pre><span></span><code><span class="n">Product</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">filter</span><span class="p">(</span><span class="nb">id</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span><span class="o">.</span><span class="n">update</span><span class="p">(</span><span class="n">title</span><span class="o">=</span><span class="s2">"A new title"</span><span class="p">)</span>
</code></pre>
<p>In this case, we still need to create a custom <code>Manager</code> and <code>QuerySet</code> as we showed before.</p>
<p>Test out editing and deleting products as well.</p>
<h2 id="low-level-cache-api-methods">Low-level Cache API Methods</h2>
<p>Thus far, we've used the <code>cache.get</code>, <code>cache.set</code>, and <code>cache.delete</code> methods to get, set, and delete (for invalidation) objects in the cache. Let's take a look at some <a href="https://docs.djangoproject.com/en/3.2/topics/cache/#basic-usage">more methods</a> from <code>django.core.cache.cache</code>.</p>
<h3 id="cacheget_or_set">cache.get_or_set</h3>
<p>Gets the specified key if present. If it's not present, it sets the key.</p>
<p><strong>Syntax</strong></p>
<p><code>cache.get_or_set(key, default, timeout=DEFAULT_TIMEOUT, version=None)</code></p>
<p>The <code>timeout</code> parameter is used to set for how long (in seconds) the cache will be valid. Setting it to <code>None</code> will cache the value forever. Omitting it will use the timeout, if any, that is set in <code>setting.py</code> in the <code>CACHES</code> setting</p>
<p>Many of the cache methods also include a <code>version</code> parameter. With this parameter you can set or access different versions of the same cache key.</p>
<p><strong>Example</strong></p>
<pre><span></span><code>&gt;&gt;&gt; from django.core.cache import cache
&gt;&gt;&gt; cache.get_or_set<span class="o">(</span><span class="s1">'my_key'</span>, <span class="s1">'my new value'</span><span class="o">)</span>
<span class="s1">'my new value'</span>
</code></pre>
<p>We could have used this in our view instead of using the if statements:</p>
<pre><span></span><code><span class="c1"># current implementation</span>
<span class="n">product_objects</span> <span class="o">=</span> <span class="n">cache</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">'product_objects'</span><span class="p">)</span>

<span class="k">if</span> <span class="n">product_objects</span> <span class="ow">is</span> <span class="kc">None</span><span class="p">:</span>
<span class="n">product_objects</span> <span class="o">=</span> <span class="n">Product</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>
<span class="n">cache</span><span class="o">.</span><span class="n">set</span><span class="p">(</span><span class="s1">'product_objects'</span><span class="p">,</span> <span class="n">product_objects</span><span class="p">)</span>


<span class="c1"># with get_or_set</span>
<span class="n">product_objects</span> <span class="o">=</span> <span class="n">cache</span><span class="o">.</span><span class="n">get_or_set</span><span class="p">(</span><span class="s1">'product_objects'</span><span class="p">,</span> <span class="n">product_objects</span><span class="p">)</span>
</code></pre>
<h3 id="cacheset_many">cache.set_many</h3>
<p>Used to set multiple keys at once by passing a dictionary of key-value pairs.</p>
<p><strong>Syntax</strong></p>
<p><code>cache.set_many(dict, timeout)</code></p>
<p><strong>Example</strong></p>
<pre><span></span><code>&gt;&gt;&gt; cache.set_many<span class="o">({</span><span class="s1">'my_first_key'</span>: <span class="m">1</span>, <span class="s1">'my_second_key'</span>: <span class="m">2</span>, <span class="s1">'my_third_key'</span>: <span class="m">3</span><span class="o">})</span>
</code></pre>
<h3 id="cacheget_many">cache.get_many</h3>
<p>Used to get multiple cache objects at once. It returns a dictionary with the keys specified as parameters to the method, as long as they exist and haven't expired.</p>
<p><strong>Syntax</strong></p>
<p><code>cache.get_many(keys, version=None)</code></p>
<p><strong>Example</strong></p>
<pre><span></span><code>&gt;&gt;&gt; cache.get_many<span class="o">([</span><span class="s1">'my_key'</span>, <span class="s1">'my_first_key'</span>, <span class="s1">'my_second_key'</span>, <span class="s1">'my_third_key'</span><span class="o">])</span>
OrderedDict<span class="o">([(</span><span class="s1">'my_key'</span>, <span class="s1">'my new value'</span><span class="o">)</span>, <span class="o">(</span><span class="s1">'my_first_key'</span>, <span class="m">1</span><span class="o">)</span>, <span class="o">(</span><span class="s1">'my_second_key'</span>, <span class="m">2</span><span class="o">)</span>, <span class="o">(</span><span class="s1">'my_third_key'</span>, <span class="m">3</span><span class="o">)])</span>
</code></pre>
<h3 id="cachetouch">cache.touch</h3>
<p>If you want to update the expiration for a certain key, you can use this method. The timeout value is set in the timeout parameter in seconds.</p>
<p><strong>Syntax</strong></p>
<p><code>cache.touch(key, timeout=DEFAULT_TIMEOUT, version=None)</code></p>
<p><strong>Example</strong></p>
<pre><span></span><code>&gt;&gt;&gt; cache.set<span class="o">(</span><span class="s1">'sample'</span>, <span class="s1">'just a sample'</span>, <span class="nv">timeout</span><span class="o">=</span><span class="m">120</span><span class="o">)</span>
&gt;&gt;&gt; cache.touch<span class="o">(</span><span class="s1">'sample'</span>, <span class="nv">timeout</span><span class="o">=</span><span class="m">180</span><span class="o">)</span>
</code></pre>
<h3 id="cacheincr-and-cachedecr">cache.incr and cache.decr</h3>
<p>These two methods can be used to increment or decrement a value of a key that already exists. If the methods are used on a nonexistent cache key it will return a <code>ValueError</code>.</p>
<p>In the case of not specifying the delta parameter the value will be increased/decreased by 1.</p>
<p><strong>Syntax</strong></p>
<pre><span></span><code>cache.incr(key, delta=1, version=None)

cache.decr(key, delta=1, version=None)
</code></pre>
<p><strong>Example</strong></p>
<pre><span></span><code>&gt;&gt;&gt; cache.set<span class="o">(</span><span class="s1">'my_first_key'</span>, <span class="m">1</span><span class="o">)</span>
&gt;&gt;&gt; cache.incr<span class="o">(</span><span class="s1">'my_first_key'</span><span class="o">)</span>
<span class="m">2</span>
&gt;&gt;&gt;
&gt;&gt;&gt; cache.incr<span class="o">(</span><span class="s1">'my_first_key'</span>, <span class="m">10</span><span class="o">)</span>
<span class="m">12</span>
</code></pre>
<h3 id="cacheclose">cache.close()</h3>
<p>To close the connection to your cache you use the <code>close()</code> method.</p>
<p><strong>Syntax</strong></p>
<p><code>cache.close()</code></p>
<p><strong>Example</strong></p>
<p><code>cache.close()</code></p>
<h3 id="cacheclear">cache.clear</h3>
<p>To delete all the keys in the cache at once you can use this method. Just keep in mind that it will remove <em>everything</em> from the cache, not just the keys your application has set.</p>
<p><strong>Syntax</strong></p>
<p><code>cache.clear()</code></p>
<p><strong>Example</strong></p>
<p><code>cache.clear()</code></p>


