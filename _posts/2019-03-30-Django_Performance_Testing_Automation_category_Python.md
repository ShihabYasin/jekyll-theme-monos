---
layout: post
title: Django Performance Testing Automation
date: 2019-03-30 16:20:23 +0900
category: Python
tag: Python
---


<h1> Django Performance Testing Automation </h1>

<p> Find code <a href="https://github.com/ShihabYasin/django-performance-measure">here.</a> </p>
<h2 id="n1-queries">N+1 Queries</h2>

<p>Say, for example, you're working with a Django application that has the following models:</p>
<pre><span></span><code><span class="c1"># courses/models.py</span>

<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>


<span class="k">class</span> <span class="nc">Author</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">name</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">100</span><span class="p">)</span>

<span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">name</span>


<span class="k">class</span> <span class="nc">Course</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">title</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">100</span><span class="p">)</span>
<span class="n">author</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">ForeignKey</span><span class="p">(</span><span class="n">Author</span><span class="p">,</span> <span class="n">on_delete</span><span class="o">=</span><span class="n">models</span><span class="o">.</span><span class="n">CASCADE</span><span class="p">)</span>

<span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">title</span>
</code></pre>
<p>Now, if you're tasked with creating a new view for returning a JSON response of all courses with the title and author name, you could write the following code:</p>
<pre><span></span><code><span class="c1"># courses/views.py</span>

<span class="kn">from</span> <span class="nn">django.http</span> <span class="kn">import</span> <span class="n">JsonResponse</span>

<span class="kn">from</span> <span class="nn">courses.models</span> <span class="kn">import</span> <span class="n">Course</span>


<span class="k">def</span> <span class="nf">all_courses</span><span class="p">(</span><span class="n">request</span><span class="p">):</span>
<span class="n">queryset</span> <span class="o">=</span> <span class="n">Course</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>

<span class="n">courses</span> <span class="o">=</span> <span class="p">[]</span>

<span class="k">for</span> <span class="n">course</span> <span class="ow">in</span> <span class="n">queryset</span><span class="p">:</span>
<span class="n">courses</span><span class="o">.</span><span class="n">append</span><span class="p">(</span>
<span class="p">{</span><span class="s2">"title"</span><span class="p">:</span> <span class="n">course</span><span class="o">.</span><span class="n">title</span><span class="p">,</span> <span class="s2">"author"</span><span class="p">:</span> <span class="n">course</span><span class="o">.</span><span class="n">author</span><span class="o">.</span><span class="n">name</span><span class="p">}</span>
<span class="p">)</span>

<span class="k">return</span> <span class="n">JsonResponse</span><span class="p">(</span><span class="n">courses</span><span class="p">,</span> <span class="n">safe</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</code></pre>
<p>This code will work, but it's very inefficient since it will make far too many database queries:</p>
<li>1 query for obtaining all the courses</li>
<li>N queries for obtaining the branch in each iteration</li>
<p>Before addressing this, let's look at just how many queries are made and measure the execution time.</p>
<h2 id="metrics-middleware">Metrics Middleware</h2>
<p>You'll notice that the project includes custom middleware that calculates and logs the execution time of each request:</p>
<pre><span></span><code><span class="c1"># core/middleware.py</span>

<span class="kn">import</span> <span class="nn">logging</span>
<span class="kn">import</span> <span class="nn">time</span>

<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">connection</span><span class="p">,</span> <span class="n">reset_queries</span>


<span class="k">def</span> <span class="nf">metric_middleware</span><span class="p">(</span><span class="n">get_response</span><span class="p">):</span>
<span class="k">def</span> <span class="nf">middleware</span><span class="p">(</span><span class="n">request</span><span class="p">):</span>
<span class="n">reset_queries</span><span class="p">()</span>

<span class="c1"># Get beginning stats</span>
<span class="n">start_queries</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">connection</span><span class="o">.</span><span class="n">queries</span><span class="p">)</span>
<span class="n">start_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>

<span class="c1"># Process the request</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">get_response</span><span class="p">(</span><span class="n">request</span><span class="p">)</span>

<span class="c1"># Get ending stats</span>
<span class="n">end_time</span> <span class="o">=</span> <span class="n">time</span><span class="o">.</span><span class="n">perf_counter</span><span class="p">()</span>
<span class="n">end_queries</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">connection</span><span class="o">.</span><span class="n">queries</span><span class="p">)</span>

<span class="c1"># Calculate stats</span>
<span class="n">total_time</span> <span class="o">=</span> <span class="n">end_time</span> <span class="o">-</span> <span class="n">start_time</span>
<span class="n">total_queries</span> <span class="o">=</span> <span class="n">end_queries</span> <span class="o">-</span> <span class="n">start_queries</span>

<span class="c1"># Log the results</span>
<span class="n">logger</span> <span class="o">=</span> <span class="n">logging</span><span class="o">.</span><span class="n">getLogger</span><span class="p">(</span><span class="s2">"debug"</span><span class="p">)</span>
<span class="n">logger</span><span class="o">.</span><span class="n">debug</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Request: </span><span class="si">{</span><span class="n">request</span><span class="o">.</span><span class="n">method</span><span class="si">}</span><span class="s2"> </span><span class="si">{</span><span class="n">request</span><span class="o">.</span><span class="n">path</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="n">logger</span><span class="o">.</span><span class="n">debug</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Number of Queries: </span><span class="si">{</span><span class="n">total_queries</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
<span class="n">logger</span><span class="o">.</span><span class="n">debug</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Total time: </span><span class="si">{</span><span class="p">(</span><span class="n">total_time</span><span class="p">)</span><span class="si">:</span><span class="s2">.2f</span><span class="si">}</span><span class="s2">s"</span><span class="p">)</span>

<span class="k">return</span> <span class="n">response</span>

<span class="k">return</span> <span class="n">middleware</span>
</code></pre>
<p>Run the database seed command to add 10 authors and 100 courses to the database:</p>
<pre><span></span><code>$ python manage.py seed_db
</code></pre>
<p>With the Django development server up and running, navigate to <a href="http://localhost:8000/courses/">http://localhost:8000/courses/</a> in your browser. You should see the JSON response. Back in your terminal, take note of the metrics:</p>
<pre><span></span><code>Request: GET /courses/
Number of Queries: <span class="m">101</span>
Total time: <span class="m">0</span>.10s
</code></pre>
<p>That's a lot of queries! This is very inefficient. Each additional author and course added will require an additional database query, so performance will continue to degrade as the database grows. Fortunately, the fix for this is quite simple: You can add a <code>select_related</code> method to create a SQL join which will include the authors in the initial database query.</p>
<pre><span></span><code><span class="n">queryset</span> <span class="o">=</span> <span class="n">Course</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">select_related</span><span class="p">(</span><span class="s2">"author"</span><span class="p">)</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>
</code></pre>
<p>Before making any code changes, let's first start with some tests.</p>
<h2 id="performance-tests">Performance Tests</h2>
<p>Start with the following test, which uses the <a href="https://pytest-django.readthedocs.io/en/latest/helpers.html#django-assert-num-queries">django_assert_num_queries</a> pytest fixture to ensure that the database is hit only once when there is one or more author and course records present in the database:</p>
<pre><span></span><code><span class="kn">import</span> <span class="nn">json</span>

<span class="kn">import</span> <span class="nn">pytest</span>
<span class="kn">from</span> <span class="nn">faker</span> <span class="kn">import</span> <span class="n">Faker</span>
<span class="kn">from</span> <span class="nn">django.test</span> <span class="kn">import</span> <span class="n">override_settings</span>

<span class="kn">from</span> <span class="nn">courses.models</span> <span class="kn">import</span> <span class="n">Course</span><span class="p">,</span> <span class="n">Author</span>


<span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">django_db</span>
<span class="k">def</span> <span class="nf">test_number_of_sql_queries_all_courses</span><span class="p">(</span><span class="n">client</span><span class="p">,</span> <span class="n">django_assert_num_queries</span><span class="p">):</span>
<span class="n">fake</span> <span class="o">=</span> <span class="n">Faker</span><span class="p">()</span>

<span class="n">author_name</span> <span class="o">=</span> <span class="n">fake</span><span class="o">.</span><span class="n">name</span><span class="p">()</span>
<span class="n">author</span> <span class="o">=</span> <span class="n">Author</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="n">author_name</span><span class="p">)</span>
<span class="n">author</span><span class="o">.</span><span class="n">save</span><span class="p">()</span>
<span class="n">course_title</span> <span class="o">=</span> <span class="n">fake</span><span class="o">.</span><span class="n">sentence</span><span class="p">(</span><span class="n">nb_words</span><span class="o">=</span><span class="mi">4</span><span class="p">)</span>
<span class="n">course</span> <span class="o">=</span> <span class="n">Course</span><span class="p">(</span><span class="n">title</span><span class="o">=</span><span class="n">course_title</span><span class="p">,</span> <span class="n">author</span><span class="o">=</span><span class="n">author</span><span class="p">)</span>
<span class="n">course</span><span class="o">.</span><span class="n">save</span><span class="p">()</span>

<span class="k">with</span> <span class="n">django_assert_num_queries</span><span class="p">(</span><span class="mi">1</span><span class="p">):</span>
<span class="n">res</span> <span class="o">=</span> <span class="n">client</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"/courses/"</span><span class="p">)</span>
<span class="n">data</span> <span class="o">=</span> <span class="n">json</span><span class="o">.</span><span class="n">loads</span><span class="p">(</span><span class="n">res</span><span class="o">.</span><span class="n">content</span><span class="p">)</span>

<span class="k">assert</span> <span class="n">res</span><span class="o">.</span><span class="n">status_code</span> <span class="o">==</span> <span class="mi">200</span>
<span class="k">assert</span> <span class="nb">len</span><span class="p">(</span><span class="n">data</span><span class="p">)</span> <span class="o">==</span> <span class="mi">1</span>

<span class="n">author_name</span> <span class="o">=</span> <span class="n">fake</span><span class="o">.</span><span class="n">name</span><span class="p">()</span>
<span class="n">author</span> <span class="o">=</span> <span class="n">Author</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="n">author_name</span><span class="p">)</span>
<span class="n">author</span><span class="o">.</span><span class="n">save</span><span class="p">()</span>
<span class="n">course_title</span> <span class="o">=</span> <span class="n">fake</span><span class="o">.</span><span class="n">sentence</span><span class="p">(</span><span class="n">nb_words</span><span class="o">=</span><span class="mi">4</span><span class="p">)</span>
<span class="n">course</span> <span class="o">=</span> <span class="n">Course</span><span class="p">(</span><span class="n">title</span><span class="o">=</span><span class="n">course_title</span><span class="p">,</span> <span class="n">author</span><span class="o">=</span><span class="n">author</span><span class="p">)</span>
<span class="n">course</span><span class="o">.</span><span class="n">save</span><span class="p">()</span>

<span class="n">res</span> <span class="o">=</span> <span class="n">client</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"/courses/"</span><span class="p">)</span>
<span class="n">data</span> <span class="o">=</span> <span class="n">json</span><span class="o">.</span><span class="n">loads</span><span class="p">(</span><span class="n">res</span><span class="o">.</span><span class="n">content</span><span class="p">)</span>

<span class="k">assert</span> <span class="n">res</span><span class="o">.</span><span class="n">status_code</span> <span class="o">==</span> <span class="mi">200</span>
<span class="k">assert</span> <span class="nb">len</span><span class="p">(</span><span class="n">data</span><span class="p">)</span> <span class="o">==</span> <span class="mi">2</span>
</code></pre>
<p>Not using pytest? Use the <a href="https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries">assertNumQueries</a> test method in place of <code>django_assert_num_queries</code>.</p>
<p>What's more, we can also use <a href="https://github.com/jmcarp/nplusone">nplusone</a> to prevent the introduction of future N+1 queries. After installing the package and adding it to the settings file, you can add it to your tests with the <code>@override_settings</code> decorator:</p>
<pre><span></span><code><span class="o">...</span>
<span class="nd">@pytest</span><span class="o">.</span><span class="n">mark</span><span class="o">.</span><span class="n">django_db</span>
<span class="nd">@override_settings</span><span class="p">(</span><span class="n">NPLUSONE_RAISE</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">test_number_of_sql_queries_all_courses</span><span class="p">(</span><span class="n">client</span><span class="p">,</span> <span class="n">django_assert_num_queries</span><span class="p">):</span>
<span class="o">...</span>
</code></pre>
<p>Or if you'd like to automatically enable nplusone across the entire test suite, add the following to your test root <em>conftest.py</em> file:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.conf</span> <span class="kn">import</span> <span class="n">settings</span>


<span class="k">def</span> <span class="nf">pytest_configure</span><span class="p">(</span><span class="n">config</span><span class="p">):</span>
<span class="n">settings</span><span class="o">.</span><span class="n">NPLUSONE_RAISE</span> <span class="o">=</span> <span class="kc">True</span>
</code></pre>
<p>Hop back to the sample app, and you run the tests. You should see the following error:</p>
<pre><span></span><code>nplusone.core.exceptions.NPlusOneError: Potential n+1 query detected on <span class="sb">`</span>Course.author<span class="sb">`</span>
</code></pre>
<p>Now, make the recommended change -- adding the <code>select_related</code> method -- and then run the tests again. They should now pass.</p>


