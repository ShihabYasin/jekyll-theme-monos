---
layout: post
title: Basic and Full-text Search in Django
date: 2019-03-31 16:20:23 +0900
category: Django
tag: Django
---


<h1>Basic and Full-text Search in Django</h1>

<h2 id="project-setup-and-overview">Project Setup</h2>
<p>Code is <a href="https://github.com/ShihabYasin/simple-django-full-text-searching">here.</a> </p>


<p>You'll use Docker to simplify setting up and running Postgres along with Django.</p>
<p>From the project root, create the images and spin up the Docker containers:</p>
<pre><span></span><code>$ docker-compose up -d --build
</code></pre>
<p>Next, apply the migrations and create a superuser:</p>
<pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py makemigrations
$ docker-compose <span class="nb">exec</span> web python manage.py migrate
$ docker-compose <span class="nb">exec</span> web python manage.py createsuperuser
</code></pre>
<p>Once done, navigate to <a href="http://127.0.0.1:8011/quotes/">http://127.0.0.1:8011/quotes/</a> to ensure the app works as expected. 

<p>Take note of the <code>Quote</code> model in <em>quotes/models.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>

<span class="k">class</span> <span class="nc">Quote</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">name</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">250</span><span class="p">)</span>
<span class="n">quote</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">TextField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">1000</span><span class="p">)</span>

<span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">quote</span>
</code></pre>
<p>Next, run the following management command to add 10,000 quotes to the database:</p>
<pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py add_quotes
</code></pre>
<p>This will take a couple of minutes. Once done, navigate to <a href="http://127.0.0.1:8011/quotes/">http://127.0.0.1:8011/quotes/</a> to see the data.</p>
<p>The output of the view is cached for five minutes, so you may want to comment out the <code>@method_decorator</code> in <em>quotes/views.py</em> to load the quotes. Make sure to remove the comment once done.</p>

<p>In the <em>quotes/templates/quote.html</em> file, you have a basic form with a search input field:</p>
<pre><span></span><code><span class="p">&lt;</span><span class="nt">form</span> <span class="na">action</span><span class="o">=</span><span class="s">"{% url 'search_results' %}"</span> <span class="na">method</span><span class="o">=</span><span class="s">"get"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">input</span>
<span class="na">type</span><span class="o">=</span><span class="s">"search"</span>
<span class="na">name</span><span class="o">=</span><span class="s">"q"</span>
<span class="na">placeholder</span><span class="o">=</span><span class="s">"Search by name or quote..."</span>
<span class="na">class</span><span class="o">=</span><span class="s">"form-control"</span>
<span class="p">/&gt;</span>
<span class="p">&lt;/</span><span class="nt">form</span><span class="p">&gt;</span>
</code></pre>
<p>On submit, the form sends the data to the backend. A <code>GET</code> request is used rather than a <code>POST</code> so that way we have access to the query string both in the URL and in the Django view, allowing users to share search results as links.</p>
<p>Before proceeding further, take a quick look at the project structure and the rest of the code.</p>
<h2 id="basic-search">Basic Search</h2>
<p>When it comes to search, with Django, you'll typically start by performing search queries with <code>contains</code> or <code>icontains</code> for exact matches. The <a href="https://docs.djangoproject.com/en/3.2/topics/db/queries/#complex-lookups-with-q-objects">Q object</a> can be used as well to add AND (<code>&amp;</code>) or OR (<code>|</code>) logical operators.</p>
<p>For instance, using the OR operator, override the<code>SearchResultsList</code>'s default <code>QuerySet</code> in <em>quotes/views.py</em> like so:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">SearchResultsList</span><span class="p">(</span><span class="n">ListView</span><span class="p">):</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Quote</span>
<span class="n">context_object_name</span> <span class="o">=</span> <span class="s2">"quotes"</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s2">"search.html"</span>

<span class="k">def</span> <span class="nf">get_queryset</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="n">query</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">request</span><span class="o">.</span><span class="n">GET</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"q"</span><span class="p">)</span>
<span class="k">return</span> <span class="n">Quote</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">filter</span><span class="p">(</span>
<span class="n">Q</span><span class="p">(</span><span class="n">name__icontains</span><span class="o">=</span><span class="n">query</span><span class="p">)</span> <span class="o">|</span> <span class="n">Q</span><span class="p">(</span><span class="n">quote__icontains</span><span class="o">=</span><span class="n">query</span><span class="p">)</span>
<span class="p">)</span>
</code></pre>
<p>Here, we used the <a href="https://docs.djangoproject.com/en/3.2/topics/db/queries/#retrieving-specific-objects-with-filters">filter</a> method to filter against the <code>name</code> or <code>quote</code> fields. Furthermore, we also used the <a href="https://docs.djangoproject.com/en/3.2/ref/models/querysets/#icontains">icontains</a> extension to check if the query is present in the <code>name</code> or <code>quote</code> fields (case insensitive). A positive result will be returned if a match is found.</p>
<p>Don't forget the import:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.db.models</span> <span class="kn">import</span> <span class="n">Q</span>
</code></pre>

<p>For small data sets, this is a great way to add basic search functionality to your app. If you're dealing with a large data set or want search functionality that feels like an Internet search engine, you'll want to move to full-text search.</p>
<h2 id="full-text-search">Full-text Search</h2>
<p>The basic search that we saw earlier has several limitations especially when you want to perform complex lookups.</p>
<p>As mentioned, with basic search, you can only perform exact matches.</p>
<p>Another limitation is that of <strong>stop words</strong>. <a href="https://www.postgresql.org/docs/current/textsearch-dictionaries.html#TEXTSEARCH-STOPWORDS">Stop words</a> are words such as "a", "an", and "the". These words are common and insufficiently meaningful, therefore they should be ignored. To test, try searching for a word with "the" in front of it. Say you searched for "the middle". In this case, you'll only see results for "the middle", so you won't see any results that have the word "middle" without "the" before it.</p>
<p>Say you have these two sentences:</p>
<ol>
<li>I am in the middle.</li>
<li>You don't like middle school.</li>
</ol>
<li>I am in the middle.</li>
<li>You don't like middle school.</li>
<p>You'll get the following returned with each type of search:</p>
<p>Another issue is that of ignoring similar words. With basic search, only exact matches are returned. However, with full-text search, similar words are accounted for. To test, try to find some similar words like "pony" and "ponies". With basic search, if you search for "pony" you won't see results that contain "ponies" -- and vice versa.</p>
<p>Say you have these two sentences.</p>
<ol>
<li>I am a pony.</li>
<li>You don't like ponies</li>
</ol>
<li>I am a pony.</li>
<li>You don't like ponies</li>
<p>You'll get the following returned with each type of search:</p>
<p>With full-text search, both of these issues are mitigated. However, keep in mind that depending on your goal, full-text search may actually decrease <strong>precision</strong> (quality) and <strong>recall</strong> (quantity of relevant results). Typically, full-text search is less precise than basic search, since basic search yields exact matches. That said, if you're searching through large data sets with large blocks of text, full-text search is preferred since it's usually much faster.</p>
<p><a href="https://en.wikipedia.org/wiki/Full-text_search">Full-text search</a> is an advanced searching technique that examines all the words in every stored document as it tries to match the search criteria. In addition, with full-text search, you can employ language-specific <a href="https://en.wikipedia.org/wiki/Stemming">stemming</a> on the words being indexed. For instance, the word "drives", "drove", and "driven" will be recorded under the single concept word "drive". Stemming is the process of reducing words to their word stem, base, or root form.</p>
<p>It suffices to say that full-text search is not perfect. It's likely to retrieve many documents that are not relevant (false positives) to the intended search query. However, there are some techniques based on Bayesian algorithms that can help reduce such problems.</p>
<p>To take advantage of Postgres full-text search with Django, add <code>django.contrib.postgres</code> to your <code>INSTALLED_APPS</code> list:</p>
<pre><span></span><code><span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
<span class="o">...</span>

<span class="s2">"django.contrib.postgres"</span><span class="p">,</span>  <span class="c1"># new</span>
<span class="p">]</span>
</code></pre>
<p>Next, let's look at two quick examples of full-text search, on a single field and on multiple fields.</p>
<h3 id="single-field-search">Single Field Search</h3>
<p>Update the <code>get_queryset</code> function under the <code>SearchResultsList</code> view function like so:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">SearchResultsList</span><span class="p">(</span><span class="n">ListView</span><span class="p">):</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Quote</span>
<span class="n">context_object_name</span> <span class="o">=</span> <span class="s2">"quotes"</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s2">"search.html"</span>

<span class="k">def</span> <span class="nf">get_queryset</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="n">query</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">request</span><span class="o">.</span><span class="n">GET</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"q"</span><span class="p">)</span>
<span class="k">return</span> <span class="n">Quote</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">filter</span><span class="p">(</span><span class="n">quote__search</span><span class="o">=</span><span class="n">query</span><span class="p">)</span>
</code></pre>
<p>Here, we set up full-text search against a single field -- the quote field.</p>

<p>As you can see, it takes similar words into account. In the above example, "ponies" and "pony" are treated as similar words.</p>
<h3 id="multi-field-search">Multi Field Search</h3>
<p>To search against multiple fields and on related models, you can use the <code>SearchVector</code> class.</p>
<p>Again, update <code>SearchResultsList</code>:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">SearchResultsList</span><span class="p">(</span><span class="n">ListView</span><span class="p">):</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Quote</span>
<span class="n">context_object_name</span> <span class="o">=</span> <span class="s2">"quotes"</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s2">"search.html"</span>

<span class="k">def</span> <span class="nf">get_queryset</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="n">query</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">request</span><span class="o">.</span><span class="n">GET</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"q"</span><span class="p">)</span>
<span class="k">return</span> <span class="n">Quote</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">annotate</span><span class="p">(</span><span class="n">search</span><span class="o">=</span><span class="n">SearchVector</span><span class="p">(</span><span class="s2">"name"</span><span class="p">,</span> <span class="s2">"quote"</span><span class="p">))</span><span class="o">.</span><span class="n">filter</span><span class="p">(</span>
<span class="n">search</span><span class="o">=</span><span class="n">query</span>
<span class="p">)</span>
</code></pre>
<p>To search against multiple fields, you <a href="https://docs.djangoproject.com/en/3.2/topics/db/aggregation/">annotate</a>d the queryset using a <code>SearchVector</code>. The vector is the data that you're searching for, which has been converted into a form that is easy to search. In the example above, this data is the <code>name</code> and <code>quote</code> fields in your database.</p>
<p>Make sure to add the import:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.postgres.search</span> <span class="kn">import</span> <span class="n">SearchVector</span>
</code></pre>
<p>Try some searches out.</p>
<h2 id="stemming-and-ranking">Stemming and Ranking</h2>
<p>In this section, you'll combine several methods such as <a href="https://docs.djangoproject.com/en/3.1/ref/contrib/postgres/search/#searchvector">SearchVector</a>, <a href="https://docs.djangoproject.com/en/3.1/ref/contrib/postgres/search/#searchquery">SearchQuery</a>, and <a href="https://docs.djangoproject.com/en/3.1/ref/contrib/postgres/search/#searchrank">SearchRank</a> to produce a very robust search that uses both stemming and ranking.</p>
<p>Again, stemming is the process of reducing words to their word stem, base, or root form. With stemming, words like "child" and "children" will be treated as similar words. Ranking, on the other hand, allows us to order results by relevancy.</p>
<p>Update <code>SearchResultsList</code>:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">SearchResultsList</span><span class="p">(</span><span class="n">ListView</span><span class="p">):</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Quote</span>
<span class="n">context_object_name</span> <span class="o">=</span> <span class="s2">"quotes"</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s2">"search.html"</span>

<span class="k">def</span> <span class="nf">get_queryset</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="n">query</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">request</span><span class="o">.</span><span class="n">GET</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"q"</span><span class="p">)</span>
<span class="n">search_vector</span> <span class="o">=</span> <span class="n">SearchVector</span><span class="p">(</span><span class="s2">"name"</span><span class="p">,</span> <span class="s2">"quote"</span><span class="p">)</span>
<span class="n">search_query</span> <span class="o">=</span> <span class="n">SearchQuery</span><span class="p">(</span><span class="n">query</span><span class="p">)</span>
<span class="k">return</span> <span class="p">(</span>
<span class="n">Quote</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">annotate</span><span class="p">(</span>
<span class="n">search</span><span class="o">=</span><span class="n">search_vector</span><span class="p">,</span> <span class="n">rank</span><span class="o">=</span><span class="n">SearchRank</span><span class="p">(</span><span class="n">search_vector</span><span class="p">,</span> <span class="n">search_query</span><span class="p">)</span>
<span class="p">)</span>
<span class="o">.</span><span class="n">filter</span><span class="p">(</span><span class="n">search</span><span class="o">=</span><span class="n">search_query</span><span class="p">)</span>
<span class="o">.</span><span class="n">order_by</span><span class="p">(</span><span class="s2">"-rank"</span><span class="p">)</span>
<span class="p">)</span>
</code></pre>
<p>What's happening here?</p>
<ol>
<li><code>SearchVector</code> - again you used a search vector to search against multiple fields. The data is converted into another form since you're no longer just searching the raw text like you did when <code>icontains</code> was used. Therefore, with this, you will be able to search plurals easily. For example, searching for "flask" and "flasks" will yield the same search because they are, well, <em>basically</em> the same thing.</li>
<li><code>SearchQuery</code> - translates the words provided to us as a query from the form, passes them through a stemming algorithm, and then it looks for matches for all of the resulting terms.</li>
<li><code>SearchRank</code> - allows us to order the results by relevancy. It takes into account how often the query terms appear in the document, how close the terms are on the document, and how important the part of the document is where they occur.</li>
</ol>
<li><code>SearchVector</code> - again you used a search vector to search against multiple fields. The data is converted into another form since you're no longer just searching the raw text like you did when <code>icontains</code> was used. Therefore, with this, you will be able to search plurals easily. For example, searching for "flask" and "flasks" will yield the same search because they are, well, <em>basically</em> the same thing.</li>
<li><code>SearchQuery</code> - translates the words provided to us as a query from the form, passes them through a stemming algorithm, and then it looks for matches for all of the resulting terms.</li>
<li><code>SearchRank</code> - allows us to order the results by relevancy. It takes into account how often the query terms appear in the document, how close the terms are on the document, and how important the part of the document is where they occur.</li>
<p>Add the imports:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.postgres.search</span> <span class="kn">import</span> <span class="n">SearchVector</span><span class="p">,</span> <span class="n">SearchQuery</span><span class="p">,</span> <span class="n">SearchRank</span>
</code></pre>


<p>Compare the results from the basic search to that of the full-text search. There's a clear difference. In the full-text search, the query with the highest results is shown first. This is the power of <code>SearchRank</code>. Combining <code>SearchVector</code>, <code>SearchQuery</code>, and <code>SearchRank</code> is a quick way to produce a much more powerful and precise search than the basic search.</p>
<h2 id="adding-weights">Adding Weights</h2>
<p>Full-text search gives us the ability to add more importance to some fields in our table in the database over other fields. We can achieve this by adding weights to our queries.</p>
<p>The <a href="https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/#postgresql-fts-weighting-queries">weight</a> should be one of the following letters D, C, B, A. By default, these weights refer to the numbers 0.1, 0.2, 0.4, and 1.0, respectively.</p>
<p>Update <code>SearchResultsList</code>:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">SearchResultsList</span><span class="p">(</span><span class="n">ListView</span><span class="p">):</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Quote</span>
<span class="n">context_object_name</span> <span class="o">=</span> <span class="s2">"quotes"</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s2">"search.html"</span>

<span class="k">def</span> <span class="nf">get_queryset</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="n">query</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">request</span><span class="o">.</span><span class="n">GET</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"q"</span><span class="p">)</span>
<span class="n">search_vector</span> <span class="o">=</span> <span class="n">SearchVector</span><span class="p">(</span><span class="s2">"name"</span><span class="p">,</span> <span class="n">weight</span><span class="o">=</span><span class="s2">"B"</span><span class="p">)</span> <span class="o">+</span> <span class="n">SearchVector</span><span class="p">(</span>
<span class="s2">"quote"</span><span class="p">,</span> <span class="n">weight</span><span class="o">=</span><span class="s2">"A"</span>
<span class="p">)</span>
<span class="n">search_query</span> <span class="o">=</span> <span class="n">SearchQuery</span><span class="p">(</span><span class="n">query</span><span class="p">)</span>
<span class="k">return</span> <span class="p">(</span>
<span class="n">Quote</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">annotate</span><span class="p">(</span><span class="n">rank</span><span class="o">=</span><span class="n">SearchRank</span><span class="p">(</span><span class="n">search_vector</span><span class="p">,</span> <span class="n">search_query</span><span class="p">))</span>
<span class="o">.</span><span class="n">filter</span><span class="p">(</span><span class="n">rank__gte</span><span class="o">=</span><span class="mf">0.3</span><span class="p">)</span>
<span class="o">.</span><span class="n">order_by</span><span class="p">(</span><span class="s2">"-rank"</span><span class="p">)</span>
<span class="p">)</span>
</code></pre>
<p>Here, you added weights to the <code>SearchVector</code> using both the <code>name</code> and <code>quote</code> fields. Weights of 0.4 and 1.0 were applied to the name and quote fields, respectively. Therefore, quote matches will prevail over name content matches. Finally, you filtered the results to display only the ones that are greater than 0.3.</p>
<h2 id="adding-a-preview-to-the-search-results">Adding a Preview to the Search Results</h2>
<p>In this section, you'll add a little preview of your search result via the <a href="https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/#searchheadline">SearchHeadline</a> method. This will highlight the search result query.</p>
<p>Update <code>SearchResultsList</code> again:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">SearchResultsList</span><span class="p">(</span><span class="n">ListView</span><span class="p">):</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Quote</span>
<span class="n">context_object_name</span> <span class="o">=</span> <span class="s2">"quotes"</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s2">"search.html"</span>

<span class="k">def</span> <span class="nf">get_queryset</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="n">query</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">request</span><span class="o">.</span><span class="n">GET</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"q"</span><span class="p">)</span>
<span class="n">search_vector</span> <span class="o">=</span> <span class="n">SearchVector</span><span class="p">(</span><span class="s2">"name"</span><span class="p">,</span> <span class="s2">"quote"</span><span class="p">)</span>
<span class="n">search_query</span> <span class="o">=</span> <span class="n">SearchQuery</span><span class="p">(</span><span class="n">query</span><span class="p">)</span>
<span class="n">search_headline</span> <span class="o">=</span> <span class="n">SearchHeadline</span><span class="p">(</span><span class="s2">"quote"</span><span class="p">,</span> <span class="n">search_query</span><span class="p">)</span>
<span class="k">return</span> <span class="n">Quote</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">annotate</span><span class="p">(</span>
<span class="n">search</span><span class="o">=</span><span class="n">search_vector</span><span class="p">,</span>
<span class="n">rank</span><span class="o">=</span><span class="n">SearchRank</span><span class="p">(</span><span class="n">search_vector</span><span class="p">,</span> <span class="n">search_query</span><span class="p">)</span>
<span class="p">)</span><span class="o">.</span><span class="n">annotate</span><span class="p">(</span><span class="n">headline</span><span class="o">=</span><span class="n">search_headline</span><span class="p">)</span><span class="o">.</span><span class="n">filter</span><span class="p">(</span><span class="n">search</span><span class="o">=</span><span class="n">search_query</span><span class="p">)</span><span class="o">.</span><span class="n">order_by</span><span class="p">(</span><span class="s2">"-rank"</span><span class="p">)</span>
</code></pre>
<p>The <code>SearchHeadline</code> takes in the field you want to preview. In this case, this will be the <code>quote</code> field along with the query, which will be in bold.</p>
<p>Make sure to add the import:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.postgres.search</span> <span class="kn">import</span> <span class="n">SearchVector</span><span class="p">,</span> <span class="n">SearchQuery</span><span class="p">,</span> <span class="n">SearchRank</span><span class="p">,</span> <span class="n">SearchHeadline</span>
</code></pre>
<p>Before trying out some searches, update the <code>&lt;li&gt;&lt;/li&gt;</code> in <em>quotes/templates/search.html</em> like so:</p>
<pre><span></span><code><span class="p">&lt;</span><span class="nt">li</span><span class="p">&gt;</span>{{ quote.headline | safe }} - <span class="p">&lt;</span><span class="nt">b</span><span class="p">&gt;</span>By <span class="p">&lt;</span><span class="nt">i</span><span class="p">&gt;</span>{{ quote.name }}<span class="p">&lt;/</span><span class="nt">i</span><span class="p">&gt;&lt;/</span><span class="nt">b</span><span class="p">&gt;&lt;/</span><span class="nt">li</span><span class="p">&gt;</span>
</code></pre>
<p>Now, instead of showing the quotes as you did before, only a preview of the full quote field is displayed along with the highlighted search query.</p>
<h2 id="boosting-performance">Boosting Performance</h2>
<p>Full-text search is an intensive process. To combat slow performance, you can:</p>
<ol>
<li>Save the search vectors to the database with <a href="https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/#searchvectorfield">SearchVectorField</a>. In other words, rather than converting the strings to search vectors on the fly, we'll create a separate database field that contains the processed search vectors and update the field any time there's an insert or update to either the <code>quote</code> or <code>name</code> fields.</li>
<li>Create a <a href="https://en.wikipedia.org/wiki/Database_index">database index</a>, which is a data structure that enhances the speed of the data retrieval processes on a database. It, therefore, speeds up the query. Postgres gives you several <a href="https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/indexes/">indexes</a> to work with that might be applicable for different situations. The <a href="https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/indexes/#ginindex">GinIndex</a> is arguably the most popular.</li>
</ol>
<li>Save the search vectors to the database with <a href="https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/#searchvectorfield">SearchVectorField</a>. In other words, rather than converting the strings to search vectors on the fly, we'll create a separate database field that contains the processed search vectors and update the field any time there's an insert or update to either the <code>quote</code> or <code>name</code> fields.</li>
<li>Create a <a href="https://en.wikipedia.org/wiki/Database_index">database index</a>, which is a data structure that enhances the speed of the data retrieval processes on a database. It, therefore, speeds up the query. Postgres gives you several <a href="https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/indexes/">indexes</a> to work with that might be applicable for different situations. The <a href="https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/indexes/#ginindex">GinIndex</a> is arguably the most popular.</li>
<p>To learn more about performance with full-text search, review the <a href="https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/#performance">Performance</a> section from the Django docs.</p>
<h3 id="search-vector-field">Search Vector Field</h3>
<p>Start by adding a new <a href="https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/#searchvectorfield">SearchVectorField</a> field to the <code>Quote</code> model in <em>quotes/models.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.postgres.search</span> <span class="kn">import</span> <span class="n">SearchVectorField</span>  <span class="c1"># new</span>
<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>


<span class="k">class</span> <span class="nc">Quote</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">name</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">250</span><span class="p">)</span>
<span class="n">quote</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">TextField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">1000</span><span class="p">)</span>
<span class="n">search_vector</span> <span class="o">=</span> <span class="n">SearchVectorField</span><span class="p">(</span><span class="n">null</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>  <span class="c1"># new</span>

<span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">quote</span>
</code></pre>
<p>Create the migration file:</p>
<pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py makemigrations
</code></pre>
<p>Now, you can only populate this field when the <code>quote</code> or <code>name</code> objects already exists in the database. Thus, we need to add a trigger to update the <code>search_vector</code> field whenever the <code>quote</code> or <code>name</code> fields are updated. To achieve this, create a custom migration file in "quotes/migrations" called <em>0003_search_vector_trigger.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.postgres.search</span> <span class="kn">import</span> <span class="n">SearchVector</span>
<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">migrations</span>


<span class="k">def</span> <span class="nf">compute_search_vector</span><span class="p">(</span><span class="n">apps</span><span class="p">,</span> <span class="n">schema_editor</span><span class="p">):</span>
<span class="n">Quote</span> <span class="o">=</span> <span class="n">apps</span><span class="o">.</span><span class="n">get_model</span><span class="p">(</span><span class="s2">"quotes"</span><span class="p">,</span> <span class="s2">"Quote"</span><span class="p">)</span>
<span class="n">Quote</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">update</span><span class="p">(</span><span class="n">search_vector</span><span class="o">=</span><span class="n">SearchVector</span><span class="p">(</span><span class="s2">"name"</span><span class="p">,</span> <span class="s2">"quote"</span><span class="p">))</span>


<span class="k">class</span> <span class="nc">Migration</span><span class="p">(</span><span class="n">migrations</span><span class="o">.</span><span class="n">Migration</span><span class="p">):</span>

<span class="n">dependencies</span> <span class="o">=</span> <span class="p">[</span>
<span class="p">(</span><span class="s2">"quotes"</span><span class="p">,</span> <span class="s2">"0002_quote_search_vector"</span><span class="p">),</span>
<span class="p">]</span>

<span class="n">operations</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">migrations</span><span class="o">.</span><span class="n">RunSQL</span><span class="p">(</span>
<span class="n">sql</span><span class="o">=</span><span class="s2">"""</span>
<span class="s2">            CREATE TRIGGER search_vector_trigger</span>
<span class="s2">            BEFORE INSERT OR UPDATE OF name, quote, search_vector</span>
<span class="s2">            ON quotes_quote</span>
<span class="s2">            FOR EACH ROW EXECUTE PROCEDURE</span>
<span class="s2">            tsvector_update_trigger(</span>
<span class="s2">                search_vector, 'pg_catalog.english', name, quote</span>
<span class="s2">            );</span>
<span class="s2">            UPDATE quotes_quote SET search_vector = NULL;</span>
<span class="s2">            """</span><span class="p">,</span>
<span class="n">reverse_sql</span><span class="o">=</span><span class="s2">"""</span>
<span class="s2">            DROP TRIGGER IF EXISTS search_vector_trigger</span>
<span class="s2">            ON quotes_quote;</span>
<span class="s2">            """</span><span class="p">,</span>
<span class="p">),</span>
<span class="n">migrations</span><span class="o">.</span><span class="n">RunPython</span><span class="p">(</span>
<span class="n">compute_search_vector</span><span class="p">,</span> <span class="n">reverse_code</span><span class="o">=</span><span class="n">migrations</span><span class="o">.</span><span class="n">RunPython</span><span class="o">.</span><span class="n">noop</span>
<span class="p">),</span>
<span class="p">]</span>
</code></pre>
<p>Depending on your project structure, you may need to update the name of the previous migration file in <code>dependencies</code>.</p>
<p>Apply the migrations:</p>
<pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py migrate
</code></pre>
<p>To use the new field for searches, update <code>SearchResultsList</code> like so:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">SearchResultsList</span><span class="p">(</span><span class="n">ListView</span><span class="p">):</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Quote</span>
<span class="n">context_object_name</span> <span class="o">=</span> <span class="s2">"quotes"</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s2">"search.html"</span>

<span class="k">def</span> <span class="nf">get_queryset</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="n">query</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">request</span><span class="o">.</span><span class="n">GET</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"q"</span><span class="p">)</span>
<span class="k">return</span> <span class="n">Quote</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">filter</span><span class="p">(</span><span class="n">search_vector</span><span class="o">=</span><span class="n">query</span><span class="p">)</span>
</code></pre>
<p>Update the <code>&lt;li&gt;&lt;/li&gt;</code> in <em>quotes/templates/search.html</em> again:</p>
<pre><span></span><code><span class="p">&lt;</span><span class="nt">li</span><span class="p">&gt;</span>{{ quote.quote | safe }} - <span class="p">&lt;</span><span class="nt">b</span><span class="p">&gt;</span>By <span class="p">&lt;</span><span class="nt">i</span><span class="p">&gt;</span>{{ quote.name }}<span class="p">&lt;/</span><span class="nt">i</span><span class="p">&gt;&lt;/</span><span class="nt">b</span><span class="p">&gt;&lt;/</span><span class="nt">li</span><span class="p">&gt;</span>
</code></pre>
<h3 id="index">Index</h3>
<p>Finally, let's set up a a functional index, <a href="https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/indexes/#ginindex">GinIndex</a>.</p>
<p>Update the <code>Quote</code> model:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.postgres.indexes</span> <span class="kn">import</span> <span class="n">GinIndex</span>  <span class="c1"># new</span>
<span class="kn">from</span> <span class="nn">django.contrib.postgres.search</span> <span class="kn">import</span> <span class="n">SearchVectorField</span>
<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>


<span class="k">class</span> <span class="nc">Quote</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">name</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">250</span><span class="p">)</span>
<span class="n">quote</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">TextField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">1000</span><span class="p">)</span>
<span class="n">search_vector</span> <span class="o">=</span> <span class="n">SearchVectorField</span><span class="p">(</span><span class="n">null</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">quote</span>

<span class="c1"># new</span>
<span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
<span class="n">indexes</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">GinIndex</span><span class="p">(</span><span class="n">fields</span><span class="o">=</span><span class="p">[</span><span class="s2">"search_vector"</span><span class="p">]),</span>
<span class="p">]</span>
</code></pre>
<p>Create and apply the migrations one last time:</p>
<pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py makemigrations
$ docker-compose <span class="nb">exec</span> web python manage.py migrate
</code></pre>
