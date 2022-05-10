<li class="nav-item dropdown">
<a class="nav-link" href="https://testdriven.io/courses/">Courses</a>
</li>
<li class="nav-item">
<a class="nav-link" href="https://testdriven.io/bundles/">Bundles</a>
</li>
<li class="nav-item">
<a class="nav-link" href="https://testdriven.io/blog/">Blog</a>
</li>
<li class="nav-item dropdown">
<a aria-expanded="false" aria-haspopup="true" class="nav-link dropdown-toggle" data-toggle="dropdown" href="https://testdriven.io/blog/django-drf-elasticsearch/#" id="navbarDropdown" role="button">
          Guides
        </a>
<div aria-labelledby="navbarDropdown" class="dropdown-menu">
<a class="dropdown-item" href="https://testdriven.io/guides/complete-python/">Complete Python</a>
<a class="dropdown-item" href="https://testdriven.io/guides/django-celery/">Django and Celery</a>
<a class="dropdown-item" href="https://testdriven.io/guides/flask-deep-dive/">Deep Dive Into Flask</a>
</div>
</li>
<li class="nav-item dropdown">
<a aria-expanded="false" aria-haspopup="true" class="nav-link dropdown-toggle" data-toggle="dropdown" href="https://testdriven.io/blog/django-drf-elasticsearch/#" id="navbarDropdown" role="button">
          More
        </a>
<div aria-labelledby="navbarDropdown" class="dropdown-menu">
<a class="dropdown-item" href="https://testdriven.io/support/">Support and Consulting</a>
<a class="dropdown-item" href="https://testdriven.io/test-driven-development/">What is Test-Driven Development?</a>
<a class="dropdown-item" href="https://testdriven.io/testimonials/">Testimonials</a>
<a class="dropdown-item" href="https://testdriven.io/opensource/">Open Source Donations</a>
<a class="dropdown-item" href="https://testdriven.io/about/">About Us</a>
<a class="dropdown-item" href="https://testdriven.io/authors/">Meet the Authors</a>
<a class="dropdown-item" href="https://testdriven.io/tips/">Tips and Tricks</a>
</div>
</li>
<li class="nav-item">
<a class="nav-link" data-a-social-outbound="Twitter" href="https://twitter.com/testdrivenio"><i class="fab fa-twitter"></i></a>
</li>
<li class="nav-item">
<a class="nav-link" data-a-social-outbound="GitHub" href="https://github.com/testdrivenio"><i class="fab fa-github"></i></a>
</li>
<li class="nav-item">
<a class="nav-link" href="https://testdriven.io/feeds/"><i class="fas fa-rss"></i></a>
</li>
<li class="nav-item nav-right-btn">
<a class="btn btn-primary" data-a-nav-signin="" href="https://testdriven.io/accounts/login/?next=/blog/django-drf-elasticsearch/">Sign In</a>
<a class="btn btn-brand1" data-a-nav-signup="" href="https://testdriven.io/accounts/signup/?next=/blog/django-drf-elasticsearch/">Sign Up</a>
</li>
<li class="nav-item">
<a class="nav-link" data-a-nav-signin="" href="https://testdriven.io/accounts/login/">Sign In</a>
</li>
<li class="nav-item">
<a class="nav-link" data-a-nav-signup="" href="https://testdriven.io/accounts/signup/">Sign Up</a>
</li>
<h1>Django REST Framework and Elasticsearch</h1>
<h2 class="social-share-heading sr-only">Share this tutorial</h2>
<li>
<a aria-label="Twitter" class="btn social-share-link twitter" data-a-social-share="Twitter" href="https://twitter.com/intent/tweet/?text=Django%20REST%20Framework%20and%20Elasticsearch%20from%20%40TestDrivenio&amp;url=https%3A//testdriven.io/blog/django-drf-elasticsearch/" rel="noopener" target="_blank">
<span aria-hidden="true">
<i class="fab fa-twitter"></i>
<span class="label">Twitter</span>
</span>
</a>
</li>
<li>
<a aria-label="Reddit" class="btn social-share-link reddit" data-a-social-share="Reddit" href="https://reddit.com/submit/?url=https%3A//testdriven.io/blog/django-drf-elasticsearch/&amp;resubmit=true&amp;title=Django%20REST%20Framework%20and%20Elasticsearch" rel="noopener" target="_blank">
<span aria-hidden="true">
<i class="fab fa-reddit-alien"></i>
<span class="label">Reddit</span>
</span>
</a>
</li>
<li>
<a aria-label="Hacker News" class="btn social-share-link hackernews" data-a-social-share="HackerNews" href="https://news.ycombinator.com/submitlink?u=https%3A//testdriven.io/blog/django-drf-elasticsearch/&amp;t=Django%20REST%20Framework%20and%20Elasticsearch" rel="noopener" target="_blank">
<span aria-hidden="true">
<i class="fab fa-hacker-news"></i>
<span class="label">Hacker News</span>
</span>
</a>
</li>
<li>
<a aria-label="Facebook" class="btn social-share-link facebook" data-a-social-share="Facebook" href="https://facebook.com/sharer/sharer.php?u=https%3A//testdriven.io/blog/django-drf-elasticsearch/" rel="noopener" target="_blank">
<span aria-hidden="true">
<i aria-hidden="true" class="fab fa-facebook-square"></i>
<span class="label">Facebook</span>
</span>
</a>
</li>
<p>In this tutorial, we'll look at how to integrate <a href="https://www.django-rest-framework.org/">Django REST Framework</a> (DRF) with <a href="https://www.elastic.co/elasticsearch/">Elasticsearch</a>. We'll use Django to model our data and DRF to serialize and serve it. Finally, we'll index the data with Elasticsearch and make it searchable.</p>
<h2 class="toc-header">Contents</h2>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#what-is-elasticsearch">What is Elasticsearch?</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#elasticsearch-structure-and-concepts">Elasticsearch Structure and Concepts</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#elasticsearch-vs-postgresql-full-text-search">Elasticsearch vs PostgreSQL Full-text Search</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#project-setup">Project Setup</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#database-models">Database Models</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#django-rest-framework">Django REST Framework</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#elasticsearch-setup">Elasticsearch Setup</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#creating-documents">Creating Documents</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#elasticsearch-queries">Elasticsearch Queries</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#search-views">Search Views</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#alternative-libraries">Alternative Libraries</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#conclusion">Conclusion</a></li>
<h2 id="what-is-elasticsearch">What is Elasticsearch?</h2>
<p>Elasticsearch is a distributed, free and open search and analytics engine for all types of data, including textual, numerical, geospatial, structured, and unstructured. It's known for its simple RESTful APIs, distributed nature, speed, and scalability. Elasticsearch is the central component of the <a href="https://www.elastic.co/elastic-stack/">Elastic Stack</a> (also known as the <a href="https://www.elastic.co/what-is/elk-stack">ELK Stack</a>), a set of free and open tools for data ingestion, enrichment, storage, analysis, and visualization.</p>
<p>Its use cases include:</p>
<ol>
<li>Site search and application search</li>
<li>Monitoring and visualizing your system metrics</li>
<li>Security and business analytics</li>
<li>Logging and log analysis</li>
</ol>
<li>Site search and application search</li>
<li>Monitoring and visualizing your system metrics</li>
<li>Security and business analytics</li>
<li>Logging and log analysis</li>
<p>To learn more about Elasticsearch check out <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html">What is Elasticsearch?</a> from the <a href="https://www.elastic.co/guide/index.html">official documentation</a>.</p>
<h2 id="elasticsearch-structure-and-concepts">Elasticsearch Structure and Concepts</h2>
<p>Before working with Elasticsearch, we should get familiar with the basic Elasticsearch concepts. These are listed from biggest to smallest:</p>
<ol>
<li><strong>Cluster</strong> is a collection of one or more nodes.</li>
<li><strong>Node</strong> is a single server instance that runs Elasticsearch. While communicating with the cluster, it:<ol>
<li>Stores and indexes your data</li>
<li>Provides search</li>
</ol>
</li>
<li><strong>Index</strong> is used to store the documents in dedicated data structures corresponding to the data type of fields (akin to a SQL database). Each index has one or more shards and replicas.</li>
<li><strong>Type</strong> is a collection of documents, which have something in common (akin to a SQL table).</li>
<li><strong>Shard</strong> is an <a href="https://lucene.apache.org/">Apache Lucene</a> index. It's used to split indices and keep large amounts of data manageable.</li>
<li><strong>Replica</strong> is a fail-safe mechanism and basically a copy of your index's shard.</li>
<li><strong>Document</strong> is a basic unit of information that can be indexed (akin to a SQL row). It's expressed in <a href="https://en.wikipedia.org/wiki/JSON">JSON</a>, which is a ubiquitous internet data interchange format.</li>
<li><strong>Field</strong> is the smallest individual unit of data in Elasticsearch (akin to a SQL column).</li>
</ol>
<li><strong>Cluster</strong> is a collection of one or more nodes.</li>
<li><strong>Node</strong> is a single server instance that runs Elasticsearch. While communicating with the cluster, it:<ol>
<li>Stores and indexes your data</li>
<li>Provides search</li>
</ol>
</li>
<ol>
<li>Stores and indexes your data</li>
<li>Provides search</li>
</ol>
<li>Stores and indexes your data</li>
<li>Provides search</li>
<li><strong>Index</strong> is used to store the documents in dedicated data structures corresponding to the data type of fields (akin to a SQL database). Each index has one or more shards and replicas.</li>
<li><strong>Type</strong> is a collection of documents, which have something in common (akin to a SQL table).</li>
<li><strong>Shard</strong> is an <a href="https://lucene.apache.org/">Apache Lucene</a> index. It's used to split indices and keep large amounts of data manageable.</li>
<li><strong>Replica</strong> is a fail-safe mechanism and basically a copy of your index's shard.</li>
<li><strong>Document</strong> is a basic unit of information that can be indexed (akin to a SQL row). It's expressed in <a href="https://en.wikipedia.org/wiki/JSON">JSON</a>, which is a ubiquitous internet data interchange format.</li>
<li><strong>Field</strong> is the smallest individual unit of data in Elasticsearch (akin to a SQL column).</li>
<p>The Elasticsearch cluster has the following structure:</p>
<p><img alt="Elasticsearch cluster structure" class="lazyload" data-src="/static/images/blog/django/django-drf-elasticsearch/elasticsearch_cluster.png" loading="lazy" src="./input_files/elasticsearch_cluster.png" style="max-width:100%;"/></p>
<p>Curious how relational database concepts relate to Elasticsearch concepts?</p>
<p>Review <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/_mapping_concepts_across_sql_and_elasticsearch.html">Mapping concepts across SQL and Elasticsearch</a> for more on how concepts in SQL and Elasticsearch relate to one another.</p>
<h2 id="elasticsearch-vs-postgresql-full-text-search">Elasticsearch vs PostgreSQL Full-text Search</h2>
<p>With regards to full-text search, Elasticsearch and <a href="https://www.postgresql.org/">PostgreSQL</a> both have their advantages and disadvantages. When choosing between them you should consider speed, query complexity, and budget.</p>
<p>PostgreSQL advantages:</p>
<ol>
<li>Django support</li>
<li>Faster and easier to setup</li>
<li>Doesn't require maintenance</li>
</ol>
<li>Django support</li>
<li>Faster and easier to setup</li>
<li>Doesn't require maintenance</li>
<p>Elasticsearch advantages:</p>
<ol>
<li>Optimized just for searching</li>
<li>Elasicsearch is faster (especially as the number of records increases)</li>
<li>Supports different query types (Leaf, Compound, Fuzzy, Regexp, to name a few)</li>
</ol>
<li>Optimized just for searching</li>
<li>Elasicsearch is faster (especially as the number of records increases)</li>
<li>Supports different query types (Leaf, Compound, Fuzzy, Regexp, to name a few)</li>
<p>If you're working on a simple project where speed isn't important you should opt for PostgreSQL. If performance is important and you want to write complex lookups opt for Elasticsearch.</p>
<p>For more on full-text search with Django and Postgres, check out the <a href="https://testdriven.io/blog/django-search/">Basic and Full-text Search with Django and Postgres</a> article.</p>
<h2 id="project-setup">Project Setup</h2>
<p>We'll be building a simple blog application. Our project will consist of multiple models, which will be serialized and served via <a href="https://www.django-rest-framework.org/">Django REST Framework</a>. After integrating Elasticsearch, we'll create an endpoint that will allow us to look up different authors, categories, and articles.</p>
<p>To keep our code clean and modular, we'll split our project into the following two apps:</p>
<ol>
<li><code>blog</code> - for our Django models, serializers, and ViewSets</li>
<li><code>search</code> - for Elasticsearch documents, indexes, and queries</li>
</ol>
<li><code>blog</code> - for our Django models, serializers, and ViewSets</li>
<li><code>search</code> - for Elasticsearch documents, indexes, and queries</li>
<p>Start by creating a new directory and setting up a new Django project:</p>
<pre><span></span><code>$ mkdir django-drf-elasticsearch <span class="o">&amp;&amp;</span> <span class="nb">cd</span> django-drf-elasticsearch
$ python3.9 -m venv env
$ <span class="nb">source</span> env/bin/activate

<span class="o">(</span>env<span class="o">)</span>$ pip install <span class="nv">django</span><span class="o">==</span><span class="m">3</span>.2.6
<span class="o">(</span>env<span class="o">)</span>$ django-admin.py startproject core .
</code></pre>
<p>After that, create a new app called <code>blog</code>:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py startapp blog
</code></pre>
<p>Register the app in <em>core/settings.py</em> under <code>INSTALLED_APPS</code>:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
    <span class="s1">'django.contrib.admin'</span><span class="p">,</span>
    <span class="s1">'django.contrib.auth'</span><span class="p">,</span>
    <span class="s1">'django.contrib.contenttypes'</span><span class="p">,</span>
    <span class="s1">'django.contrib.sessions'</span><span class="p">,</span>
    <span class="s1">'django.contrib.messages'</span><span class="p">,</span>
    <span class="s1">'django.contrib.staticfiles'</span><span class="p">,</span>
    <span class="s1">'blog.apps.BlogConfig'</span><span class="p">,</span> <span class="c1"># new</span>
<span class="p">]</span>
</code></pre>
<h2 id="database-models">Database Models</h2>
<p>Next, create <code>Category</code> and <code>Article</code> models in <em>blog/models.py</em>:</p>
<pre><span></span><code><span class="c1"># blog/models.py</span>

<span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>


<span class="k">class</span> <span class="nc">Category</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
    <span class="n">name</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">32</span><span class="p">)</span>
    <span class="n">description</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">TextField</span><span class="p">(</span><span class="n">null</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

    <span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
        <span class="n">verbose_name_plural</span> <span class="o">=</span> <span class="s1">'categories'</span>

    <span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">return</span> <span class="sa">f</span><span class="s1">'</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">name</span><span class="si">}</span><span class="s1">'</span>


<span class="n">ARTICLE_TYPES</span> <span class="o">=</span> <span class="p">[</span>
    <span class="p">(</span><span class="s1">'UN'</span><span class="p">,</span> <span class="s1">'Unspecified'</span><span class="p">),</span>
    <span class="p">(</span><span class="s1">'TU'</span><span class="p">,</span> <span class="s1">'Tutorial'</span><span class="p">),</span>
    <span class="p">(</span><span class="s1">'RS'</span><span class="p">,</span> <span class="s1">'Research'</span><span class="p">),</span>
    <span class="p">(</span><span class="s1">'RW'</span><span class="p">,</span> <span class="s1">'Review'</span><span class="p">),</span>
<span class="p">]</span>


<span class="k">class</span> <span class="nc">Article</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
    <span class="n">title</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">256</span><span class="p">)</span>
    <span class="n">author</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">ForeignKey</span><span class="p">(</span><span class="n">to</span><span class="o">=</span><span class="n">User</span><span class="p">,</span> <span class="n">on_delete</span><span class="o">=</span><span class="n">models</span><span class="o">.</span><span class="n">CASCADE</span><span class="p">)</span>
    <span class="nb">type</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="n">ARTICLE_TYPES</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="s1">'UN'</span><span class="p">)</span>
    <span class="n">categories</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">ManyToManyField</span><span class="p">(</span><span class="n">to</span><span class="o">=</span><span class="n">Category</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">related_name</span><span class="o">=</span><span class="s1">'categories'</span><span class="p">)</span>
    <span class="n">content</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">TextField</span><span class="p">()</span>
    <span class="n">created_datetime</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now_add</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">updated_datetime</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

    <span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">return</span> <span class="sa">f</span><span class="s1">'</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">author</span><span class="si">}</span><span class="s1">: </span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">title</span><span class="si">}</span><span class="s1"> (</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">created_datetime</span><span class="o">.</span><span class="n">date</span><span class="p">()</span><span class="si">}</span><span class="s1">)'</span>
</code></pre>
<p>Notes:</p>
<ol>
<li><code>Category</code> represents an article category -- i.e, programming, Linux, testing.</li>
<li><code>Article</code> represents an individual article. Each article can have multiple categories. Articles have a specific type -- <code>Tutorial</code>, <code>Research</code>, <code>Review</code>, or <code>Unspecified</code>.</li>
<li>Authors are represented by the default Django user model.</li>
</ol>
<li><code>Category</code> represents an article category -- i.e, programming, Linux, testing.</li>
<li><code>Article</code> represents an individual article. Each article can have multiple categories. Articles have a specific type -- <code>Tutorial</code>, <code>Research</code>, <code>Review</code>, or <code>Unspecified</code>.</li>
<li>Authors are represented by the default Django user model.</li>
<h3 id="run-migrations">Run Migrations</h3>
<p>Make migrations and then apply them:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py makemigrations
<span class="o">(</span>env<span class="o">)</span>$ python manage.py migrate
</code></pre>
<p>Register the models in <em>blog/admin.py</em>:</p>
<pre><span></span><code><span class="c1"># blog/admin.py</span>

<span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>

<span class="kn">from</span> <span class="nn">blog.models</span> <span class="kn">import</span> <span class="n">Category</span><span class="p">,</span> <span class="n">Article</span>


<span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="n">Category</span><span class="p">)</span>
<span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="n">Article</span><span class="p">)</span>
</code></pre>
<h3 id="populate-the-database">Populate the Database</h3>
<p>Before moving to the next step, we need some data to work with. I've created a simple command we can use to populate the database.</p>
<p>Create a new folder in "blog" called "management", and then inside that folder create another folder called "commands". Inside of the "commands" folder, create a new file called <em>populate_db.py</em>.</p>
<pre><span></span><code>management
└── commands
    └── populate_db.py
</code></pre>
<p>Copy the file contents from <a href="https://github.com/testdrivenio/django-drf-elasticsearch/blob/main/blog/management/commands/populate_db.py">populate_db.py</a> and paste it inside your <em>populate_db.py</em>.</p>
<p>Run the following command to populate the DB:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py populate_db
</code></pre>
<p>If everything went well you should see a <code>Successfully populated the database.</code> message in the console and there should be a few articles in your database.</p>
<h2 id="django-rest-framework">Django REST Framework</h2>
<p>Now let's install <code>djangorestframework</code> using pip:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ pip install <span class="nv">djangorestframework</span><span class="o">==</span><span class="m">3</span>.12.4
</code></pre>
<p>Register it in our <em>settings.py</em> like so:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
    <span class="s1">'django.contrib.admin'</span><span class="p">,</span>
    <span class="s1">'django.contrib.auth'</span><span class="p">,</span>
    <span class="s1">'django.contrib.contenttypes'</span><span class="p">,</span>
    <span class="s1">'django.contrib.sessions'</span><span class="p">,</span>
    <span class="s1">'django.contrib.messages'</span><span class="p">,</span>
    <span class="s1">'django.contrib.staticfiles'</span><span class="p">,</span>
    <span class="s1">'blog.apps.BlogConfig'</span><span class="p">,</span>
    <span class="s1">'rest_framework'</span><span class="p">,</span> <span class="c1"># new</span>
<span class="p">]</span>
</code></pre>
<p>Add the following settings:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">REST_FRAMEWORK</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s1">'DEFAULT_PAGINATION_CLASS'</span><span class="p">:</span> <span class="s1">'rest_framework.pagination.LimitOffsetPagination'</span><span class="p">,</span>
    <span class="s1">'PAGE_SIZE'</span><span class="p">:</span> <span class="mi">25</span>
<span class="p">}</span>
</code></pre>
<p>We'll need these settings to implement pagination.</p>
<h3 id="create-serializers">Create Serializers</h3>
<p>To serialize our Django models, we need to create a serializer for each of them. The easiest way to create serializers that depend on Django models is by using the <code>ModelSerializer</code> class.</p>
<p><em>blog/serializers.py</em>:</p>
<pre><span></span><code><span class="c1"># blog/serializers.py</span>

<span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">rest_framework</span> <span class="kn">import</span> <span class="n">serializers</span>

<span class="kn">from</span> <span class="nn">blog.models</span> <span class="kn">import</span> <span class="n">Article</span><span class="p">,</span> <span class="n">Category</span>


<span class="k">class</span> <span class="nc">UserSerializer</span><span class="p">(</span><span class="n">serializers</span><span class="o">.</span><span class="n">ModelSerializer</span><span class="p">):</span>
    <span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
        <span class="n">model</span> <span class="o">=</span> <span class="n">User</span>
        <span class="n">fields</span> <span class="o">=</span> <span class="p">(</span><span class="s1">'id'</span><span class="p">,</span> <span class="s1">'username'</span><span class="p">,</span> <span class="s1">'first_name'</span><span class="p">,</span> <span class="s1">'last_name'</span><span class="p">)</span>


<span class="k">class</span> <span class="nc">CategorySerializer</span><span class="p">(</span><span class="n">serializers</span><span class="o">.</span><span class="n">ModelSerializer</span><span class="p">):</span>
    <span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
        <span class="n">model</span> <span class="o">=</span> <span class="n">Category</span>
        <span class="n">fields</span> <span class="o">=</span> <span class="s1">'__all__'</span>


<span class="k">class</span> <span class="nc">ArticleSerializer</span><span class="p">(</span><span class="n">serializers</span><span class="o">.</span><span class="n">ModelSerializer</span><span class="p">):</span>
    <span class="n">author</span> <span class="o">=</span> <span class="n">UserSerializer</span><span class="p">()</span>
    <span class="n">categories</span> <span class="o">=</span> <span class="n">CategorySerializer</span><span class="p">(</span><span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

    <span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
        <span class="n">model</span> <span class="o">=</span> <span class="n">Article</span>
        <span class="n">fields</span> <span class="o">=</span> <span class="s1">'__all__'</span>
</code></pre>
<p>Notes:</p>
<ol>
<li><code>UserSerializer</code> and <code>CategorySerializer</code> are fairly simple: We just provided the fields we want serialized.</li>
<li>In the <code>ArticleSerializer</code>, we needed to take care of the relationships to make sure they also get serialized. This is why we provided <code>UserSerializer</code> and <code>CategorySerializer</code>.</li>
</ol>
<li><code>UserSerializer</code> and <code>CategorySerializer</code> are fairly simple: We just provided the fields we want serialized.</li>
<li>In the <code>ArticleSerializer</code>, we needed to take care of the relationships to make sure they also get serialized. This is why we provided <code>UserSerializer</code> and <code>CategorySerializer</code>.</li>
<p>Want to learn more about DRF serializers? Check out <a href="https://testdriven.io/blog/drf-serializers/">Effectively Using Django REST Framework Serializers</a>.</p>
<h3 id="create-viewsets">Create ViewSets</h3>
<p>Let's create a ViewSet for each of our models in <em>blog/views.py</em>:</p>
<pre><span></span><code><span class="c1"># blog/views.py</span>

<span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">rest_framework</span> <span class="kn">import</span> <span class="n">viewsets</span>

<span class="kn">from</span> <span class="nn">blog.models</span> <span class="kn">import</span> <span class="n">Category</span><span class="p">,</span> <span class="n">Article</span>
<span class="kn">from</span> <span class="nn">blog.serializers</span> <span class="kn">import</span> <span class="n">CategorySerializer</span><span class="p">,</span> <span class="n">ArticleSerializer</span><span class="p">,</span> <span class="n">UserSerializer</span>


<span class="k">class</span> <span class="nc">UserViewSet</span><span class="p">(</span><span class="n">viewsets</span><span class="o">.</span><span class="n">ModelViewSet</span><span class="p">):</span>
    <span class="n">serializer_class</span> <span class="o">=</span> <span class="n">UserSerializer</span>
    <span class="n">queryset</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>


<span class="k">class</span> <span class="nc">CategoryViewSet</span><span class="p">(</span><span class="n">viewsets</span><span class="o">.</span><span class="n">ModelViewSet</span><span class="p">):</span>
    <span class="n">serializer_class</span> <span class="o">=</span> <span class="n">CategorySerializer</span>
    <span class="n">queryset</span> <span class="o">=</span> <span class="n">Category</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>


<span class="k">class</span> <span class="nc">ArticleViewSet</span><span class="p">(</span><span class="n">viewsets</span><span class="o">.</span><span class="n">ModelViewSet</span><span class="p">):</span>
    <span class="n">serializer_class</span> <span class="o">=</span> <span class="n">ArticleSerializer</span>
    <span class="n">queryset</span> <span class="o">=</span> <span class="n">Article</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>
</code></pre>
<p>In this block of code, we created the ViewSets by providing the <code>serializer_class</code> and <code>queryset</code> for each ViewSet.</p>
<h3 id="define-urls">Define URLs</h3>
<p>Create the app-level URLs for the ViewSets:</p>
<pre><span></span><code><span class="c1"># blog/urls.py</span>

<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span><span class="p">,</span> <span class="n">include</span>
<span class="kn">from</span> <span class="nn">rest_framework</span> <span class="kn">import</span> <span class="n">routers</span>

<span class="kn">from</span> <span class="nn">blog.views</span> <span class="kn">import</span> <span class="n">UserViewSet</span><span class="p">,</span> <span class="n">CategoryViewSet</span><span class="p">,</span> <span class="n">ArticleViewSet</span>

<span class="n">router</span> <span class="o">=</span> <span class="n">routers</span><span class="o">.</span><span class="n">DefaultRouter</span><span class="p">()</span>
<span class="n">router</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="sa">r</span><span class="s1">'user'</span><span class="p">,</span> <span class="n">UserViewSet</span><span class="p">)</span>
<span class="n">router</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="sa">r</span><span class="s1">'category'</span><span class="p">,</span> <span class="n">CategoryViewSet</span><span class="p">)</span>
<span class="n">router</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="sa">r</span><span class="s1">'article'</span><span class="p">,</span> <span class="n">ArticleViewSet</span><span class="p">)</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
    <span class="n">path</span><span class="p">(</span><span class="s1">''</span><span class="p">,</span> <span class="n">include</span><span class="p">(</span><span class="n">router</span><span class="o">.</span><span class="n">urls</span><span class="p">)),</span>
<span class="p">]</span>
</code></pre>
<p>Then, wire up the app URLs to the project URLs:</p>
<pre><span></span><code><span class="c1"># core/urls.py</span>

<span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>
<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span><span class="p">,</span> <span class="n">include</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
    <span class="n">path</span><span class="p">(</span><span class="s1">'blog/'</span><span class="p">,</span> <span class="n">include</span><span class="p">(</span><span class="s1">'blog.urls'</span><span class="p">)),</span>
    <span class="n">path</span><span class="p">(</span><span class="s1">'admin/'</span><span class="p">,</span> <span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">urls</span><span class="p">),</span>
<span class="p">]</span>
</code></pre>
<p>Our app now has the following URLs:</p>
<ol>
<li><code>/blog/user/</code> lists all users</li>
<li><code>/blog/user/&lt;USER_ID&gt;/</code> fetches a specific user</li>
<li><code>/blog/category/</code> lists all categories</li>
<li><code>/blog/category/&lt;CATEGORY_ID&gt;/</code> fetches a specific category</li>
<li><code>/blog/article/</code> lists all articles</li>
<li><code>/blog/article/&lt;ARTICLE_ID&gt;/</code> fetches a specific article</li>
</ol>
<li><code>/blog/user/</code> lists all users</li>
<li><code>/blog/user/&lt;USER_ID&gt;/</code> fetches a specific user</li>
<li><code>/blog/category/</code> lists all categories</li>
<li><code>/blog/category/&lt;CATEGORY_ID&gt;/</code> fetches a specific category</li>
<li><code>/blog/article/</code> lists all articles</li>
<li><code>/blog/article/&lt;ARTICLE_ID&gt;/</code> fetches a specific article</li>
<h3 id="testing">Testing</h3>
<p>Now that we've registered the URLs, we can test the endpoints to see if everything works correctly.</p>
<p>Run the development server:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>Then, in your browser of choice, navigate to <a href="http://127.0.0.1:8000/blog/article/">http://127.0.0.1:8000/blog/article/</a>. The response should look something like this:</p>
<pre><span></span><code><span class="p">{</span><span class="w"></span>
<span class="w">    </span><span class="nt">"count"</span><span class="p">:</span><span class="w"> </span><span class="mi">4</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="nt">"next"</span><span class="p">:</span><span class="w"> </span><span class="kc">null</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="nt">"previous"</span><span class="p">:</span><span class="w"> </span><span class="kc">null</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="nt">"results"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w"></span>
<span class="w">        </span><span class="p">{</span><span class="w"></span>
<span class="w">            </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">"author"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w"></span>
<span class="w">                </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"></span>
<span class="w">                </span><span class="nt">"username"</span><span class="p">:</span><span class="w"> </span><span class="s2">"jess_"</span><span class="p">,</span><span class="w"></span>
<span class="w">                </span><span class="nt">"first_name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Jess"</span><span class="p">,</span><span class="w"></span>
<span class="w">                </span><span class="nt">"last_name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Brown"</span><span class="w"></span>
<span class="w">            </span><span class="p">},</span><span class="w"></span>
<span class="w">            </span><span class="nt">"categories"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w"></span>
<span class="w">                </span><span class="p">{</span><span class="w"></span>
<span class="w">                    </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"></span>
<span class="w">                    </span><span class="nt">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"SEO optimization"</span><span class="p">,</span><span class="w"></span>
<span class="w">                    </span><span class="nt">"description"</span><span class="p">:</span><span class="w"> </span><span class="kc">null</span><span class="w"></span>
<span class="w">                </span><span class="p">}</span><span class="w"></span>
<span class="w">            </span><span class="p">],</span><span class="w"></span>
<span class="w">            </span><span class="nt">"title"</span><span class="p">:</span><span class="w"> </span><span class="s2">"How to improve your Google rating?"</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">"type"</span><span class="p">:</span><span class="w"> </span><span class="s2">"TU"</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">"content"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Firstly, add the correct SEO tags..."</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">"created_datetime"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2021-08-12T17:34:31.271610Z"</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">"updated_datetime"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2021-08-12T17:34:31.322165Z"</span><span class="w"></span>
<span class="w">        </span><span class="p">},</span><span class="w"></span>
<span class="w">        </span><span class="p">{</span><span class="w"></span>
<span class="w">            </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">"author"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w"></span>
<span class="w">                </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">4</span><span class="p">,</span><span class="w"></span>
<span class="w">                </span><span class="nt">"username"</span><span class="p">:</span><span class="w"> </span><span class="s2">"johnny"</span><span class="p">,</span><span class="w"></span>
<span class="w">                </span><span class="nt">"first_name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Johnny"</span><span class="p">,</span><span class="w"></span>
<span class="w">                </span><span class="nt">"last_name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Davis"</span><span class="w"></span>
<span class="w">            </span><span class="p">},</span><span class="w"></span>
<span class="w">            </span><span class="nt">"categories"</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w"></span>
<span class="w">                </span><span class="p">{</span><span class="w"></span>
<span class="w">                    </span><span class="nt">"id"</span><span class="p">:</span><span class="w"> </span><span class="mi">4</span><span class="p">,</span><span class="w"></span>
<span class="w">                    </span><span class="nt">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Programming"</span><span class="p">,</span><span class="w"></span>
<span class="w">                    </span><span class="nt">"description"</span><span class="p">:</span><span class="w"> </span><span class="kc">null</span><span class="w"></span>
<span class="w">                </span><span class="p">}</span><span class="w"></span>
<span class="w">            </span><span class="p">],</span><span class="w"></span>
<span class="w">            </span><span class="nt">"title"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Installing latest version of Ubuntu"</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">"type"</span><span class="p">:</span><span class="w"> </span><span class="s2">"TU"</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">"content"</span><span class="p">:</span><span class="w"> </span><span class="s2">"In this tutorial, we'll take a look at how to setup the latest version of Ubuntu. Ubuntu (/ʊˈbʊntuː/ is a Linux distribution based on Debian and composed mostly of free and open-source software. Ubuntu is officially released in three editions: Desktop, Server, and Core for Internet of things devices and robots."</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">"created_datetime"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2021-08-12T17:34:31.540628Z"</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">"updated_datetime"</span><span class="p">:</span><span class="w"> </span><span class="s2">"2021-08-12T17:34:31.592555Z"</span><span class="w"></span>
<span class="w">        </span><span class="p">},</span><span class="w"></span>
<span class="w">        </span><span class="err">...</span><span class="w"></span>
<span class="w">    </span><span class="p">]</span><span class="w"></span>
<span class="p">}</span><span class="w"></span>
</code></pre>
<p>Manually test the other endpoints as well.</p>
<h2 id="elasticsearch-setup">Elasticsearch Setup</h2>
<p>Start by installing and running Elasticsearch in the background.</p>
<p>Need help getting Elasticsearch up and running? Check out the <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html">Installing Elasticsearch</a> guide.
If you're familiar with Docker, you can simply run the following command to pull the <a href="https://www.docker.elastic.co/r/elasticsearch">official image</a> and spin up a container with Elasticsearch running:</p>
<pre><span></span><code>$ docker run -p <span class="m">9200</span>:9200 -p <span class="m">9300</span>:9300 -e <span class="s2">"discovery.type=single-node"</span> docker.elastic.co/elasticsearch/elasticsearch:7.14.0
</code></pre>
<p>To integrate Elasticsearch with Django, we need to install the following packages:</p>
<ol>
<li><a href="https://elasticsearch-py.readthedocs.io/en/7.x/">elasticsearch</a> - official low-level Python client for Elasticsearch</li>
<li><a href="https://elasticsearch-dsl.readthedocs.io/en/latest/">elasticsearch-dsl-py</a> - high-level library for writing and running queries against Elasticsearch</li>
<li><a href="https://django-elasticsearch-dsl.readthedocs.io/en/latest/">django-elasticsearch-dsl</a> - wrapper around elasticsearch-dsl-py that allows indexing Django models in Elasticsearch</li>
</ol>
<li><a href="https://elasticsearch-py.readthedocs.io/en/7.x/">elasticsearch</a> - official low-level Python client for Elasticsearch</li>
<li><a href="https://elasticsearch-dsl.readthedocs.io/en/latest/">elasticsearch-dsl-py</a> - high-level library for writing and running queries against Elasticsearch</li>
<li><a href="https://django-elasticsearch-dsl.readthedocs.io/en/latest/">django-elasticsearch-dsl</a> - wrapper around elasticsearch-dsl-py that allows indexing Django models in Elasticsearch</li>
<p>Install:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ pip install <span class="nv">elasticsearch</span><span class="o">==</span><span class="m">7</span>.14.0
<span class="o">(</span>env<span class="o">)</span>$ pip install elasticsearch-dsl<span class="o">==</span><span class="m">7</span>.4.0
<span class="o">(</span>env<span class="o">)</span>$ pip install django-elasticsearch-dsl<span class="o">==</span><span class="m">7</span>.2.0
</code></pre>
<p>Start a new app called <code>search</code>, which will hold our Elasticsearch documents, indexes, and queries:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py startapp search
</code></pre>
<p>Register the <code>search</code> and <code>django_elasticsearch_dsl</code> in <em>core/settings.py</em> under <code>INSTALLED_APPS</code>:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
    <span class="s1">'django.contrib.admin'</span><span class="p">,</span>
    <span class="s1">'django.contrib.auth'</span><span class="p">,</span>
    <span class="s1">'django.contrib.contenttypes'</span><span class="p">,</span>
    <span class="s1">'django.contrib.sessions'</span><span class="p">,</span>
    <span class="s1">'django.contrib.messages'</span><span class="p">,</span>
    <span class="s1">'django.contrib.staticfiles'</span><span class="p">,</span>
    <span class="s1">'django_elasticsearch_dsl'</span><span class="p">,</span> <span class="c1"># new</span>
    <span class="s1">'blog.apps.BlogConfig'</span><span class="p">,</span>
    <span class="s1">'search.apps.SearchConfig'</span><span class="p">,</span> <span class="c1"># new</span>
    <span class="s1">'rest_framework'</span><span class="p">,</span>
<span class="p">]</span>
</code></pre>
<p>Now we need to let Django know where Elasticsearch is running. We do that by adding the following to our <em>core/settings.py</em> file:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="c1"># Elasticsearch</span>
<span class="c1"># https://django-elasticsearch-dsl.readthedocs.io/en/latest/settings.html</span>

<span class="n">ELASTICSEARCH_DSL</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s1">'default'</span><span class="p">:</span> <span class="p">{</span>
        <span class="s1">'hosts'</span><span class="p">:</span> <span class="s1">'localhost:9200'</span>
    <span class="p">},</span>
<span class="p">}</span>
</code></pre>
<p>If your Elasticsearch is running on a different port, make sure to change the above settings accordingly.</p>
<p>We can test if Django can connect to the Elasticsearch by starting our server:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>If your Django server fails, Elasticsearch is probably not working correctly.</p>
<h2 id="creating-documents">Creating Documents</h2>
<p>Before creating the documents, we need to make sure all the data is going to get saved in the proper format. We're using <code>CharField(max_length=2)</code> for our article <code>type</code>, which by itself doesn't make much sense. This is why we'll transform it to human-readable text.</p>
<p>We'll achieve this by adding a <code>type_to_string()</code> method inside our model like so:</p>
<pre><span></span><code><span class="c1"># blog/models.py</span>

<span class="k">class</span> <span class="nc">Article</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
    <span class="n">title</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">256</span><span class="p">)</span>
    <span class="n">author</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">ForeignKey</span><span class="p">(</span><span class="n">to</span><span class="o">=</span><span class="n">User</span><span class="p">,</span> <span class="n">on_delete</span><span class="o">=</span><span class="n">models</span><span class="o">.</span><span class="n">CASCADE</span><span class="p">)</span>
    <span class="nb">type</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="n">ARTICLE_TYPES</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="s1">'UN'</span><span class="p">)</span>
    <span class="n">categories</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">ManyToManyField</span><span class="p">(</span><span class="n">to</span><span class="o">=</span><span class="n">Category</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">related_name</span><span class="o">=</span><span class="s1">'categories'</span><span class="p">)</span>
    <span class="n">content</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">TextField</span><span class="p">()</span>
    <span class="n">created_datetime</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now_add</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">updated_datetime</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

    <span class="c1"># new</span>
    <span class="k">def</span> <span class="nf">type_to_string</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">type</span> <span class="o">==</span> <span class="s1">'UN'</span><span class="p">:</span>
            <span class="k">return</span> <span class="s1">'Unspecified'</span>
        <span class="k">elif</span> <span class="bp">self</span><span class="o">.</span><span class="n">type</span> <span class="o">==</span> <span class="s1">'TU'</span><span class="p">:</span>
            <span class="k">return</span> <span class="s1">'Tutorial'</span>
        <span class="k">elif</span> <span class="bp">self</span><span class="o">.</span><span class="n">type</span> <span class="o">==</span> <span class="s1">'RS'</span><span class="p">:</span>
            <span class="k">return</span> <span class="s1">'Research'</span>
        <span class="k">elif</span> <span class="bp">self</span><span class="o">.</span><span class="n">type</span> <span class="o">==</span> <span class="s1">'RW'</span><span class="p">:</span>
            <span class="k">return</span> <span class="s1">'Review'</span>

    <span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">return</span> <span class="sa">f</span><span class="s1">'</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">author</span><span class="si">}</span><span class="s1">: </span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">title</span><span class="si">}</span><span class="s1"> (</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">created_datetime</span><span class="o">.</span><span class="n">date</span><span class="p">()</span><span class="si">}</span><span class="s1">)'</span>
</code></pre>
<p>Without <code>type_to_string()</code> our model would be serialized like this:</p>
<pre><span></span><code><span class="p">{</span><span class="w"></span>
<span class="w">    </span><span class="nt">"title"</span><span class="p">:</span><span class="w"> </span><span class="s2">"This is my article."</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="nt">"type"</span><span class="p">:</span><span class="w"> </span><span class="s2">"TU"</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="err">...</span><span class="w"></span>
<span class="p">}</span><span class="w"></span>
</code></pre>
<p>After implementing <code>type_to_string()</code> our model is serialized like this:</p>
<pre><span></span><code><span class="p">{</span><span class="w"></span>
<span class="w">    </span><span class="nt">"title"</span><span class="p">:</span><span class="w"> </span><span class="s2">"This is my article."</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="nt">"type"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Tutorial"</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="err">...</span><span class="w"></span>
<span class="p">}</span><span class="w"></span>
</code></pre>
<p>Now let's create the documents. Each document needs to have an <code>Index</code> and <code>Django</code> class. In the <code>Index</code> class, we need to provide the index name and <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-update-settings.html">Elasticsearch index settings</a>. In the <code>Django</code> class, we tell the document which Django model to associate it to and provide the fields we want to be indexed.</p>
<p><em>blog/documents.py</em>:</p>
<pre><span></span><code><span class="c1"># blog/documents.py</span>

<span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django_elasticsearch_dsl</span> <span class="kn">import</span> <span class="n">Document</span><span class="p">,</span> <span class="n">fields</span>
<span class="kn">from</span> <span class="nn">django_elasticsearch_dsl.registries</span> <span class="kn">import</span> <span class="n">registry</span>

<span class="kn">from</span> <span class="nn">blog.models</span> <span class="kn">import</span> <span class="n">Category</span><span class="p">,</span> <span class="n">Article</span>


<span class="nd">@registry</span><span class="o">.</span><span class="n">register_document</span>
<span class="k">class</span> <span class="nc">UserDocument</span><span class="p">(</span><span class="n">Document</span><span class="p">):</span>
    <span class="k">class</span> <span class="nc">Index</span><span class="p">:</span>
        <span class="n">name</span> <span class="o">=</span> <span class="s1">'users'</span>
        <span class="n">settings</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">'number_of_shards'</span><span class="p">:</span> <span class="mi">1</span><span class="p">,</span>
            <span class="s1">'number_of_replicas'</span><span class="p">:</span> <span class="mi">0</span><span class="p">,</span>
        <span class="p">}</span>

    <span class="k">class</span> <span class="nc">Django</span><span class="p">:</span>
        <span class="n">model</span> <span class="o">=</span> <span class="n">User</span>
        <span class="n">fields</span> <span class="o">=</span> <span class="p">[</span>
            <span class="s1">'id'</span><span class="p">,</span>
            <span class="s1">'first_name'</span><span class="p">,</span>
            <span class="s1">'last_name'</span><span class="p">,</span>
            <span class="s1">'username'</span><span class="p">,</span>
        <span class="p">]</span>


<span class="nd">@registry</span><span class="o">.</span><span class="n">register_document</span>
<span class="k">class</span> <span class="nc">CategoryDocument</span><span class="p">(</span><span class="n">Document</span><span class="p">):</span>
    <span class="nb">id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">IntegerField</span><span class="p">()</span>

    <span class="k">class</span> <span class="nc">Index</span><span class="p">:</span>
        <span class="n">name</span> <span class="o">=</span> <span class="s1">'categories'</span>
        <span class="n">settings</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">'number_of_shards'</span><span class="p">:</span> <span class="mi">1</span><span class="p">,</span>
            <span class="s1">'number_of_replicas'</span><span class="p">:</span> <span class="mi">0</span><span class="p">,</span>
        <span class="p">}</span>

    <span class="k">class</span> <span class="nc">Django</span><span class="p">:</span>
        <span class="n">model</span> <span class="o">=</span> <span class="n">Category</span>
        <span class="n">fields</span> <span class="o">=</span> <span class="p">[</span>
            <span class="s1">'name'</span><span class="p">,</span>
            <span class="s1">'description'</span><span class="p">,</span>
        <span class="p">]</span>


<span class="nd">@registry</span><span class="o">.</span><span class="n">register_document</span>
<span class="k">class</span> <span class="nc">ArticleDocument</span><span class="p">(</span><span class="n">Document</span><span class="p">):</span>
    <span class="n">author</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">ObjectField</span><span class="p">(</span><span class="n">properties</span><span class="o">=</span><span class="p">{</span>
        <span class="s1">'id'</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">IntegerField</span><span class="p">(),</span>
        <span class="s1">'first_name'</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">TextField</span><span class="p">(),</span>
        <span class="s1">'last_name'</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">TextField</span><span class="p">(),</span>
        <span class="s1">'username'</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">TextField</span><span class="p">(),</span>
    <span class="p">})</span>
    <span class="n">categories</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">ObjectField</span><span class="p">(</span><span class="n">properties</span><span class="o">=</span><span class="p">{</span>
        <span class="s1">'id'</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">IntegerField</span><span class="p">(),</span>
        <span class="s1">'name'</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">TextField</span><span class="p">(),</span>
        <span class="s1">'description'</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">TextField</span><span class="p">(),</span>
    <span class="p">})</span>
    <span class="nb">type</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">TextField</span><span class="p">(</span><span class="n">attr</span><span class="o">=</span><span class="s1">'type_to_string'</span><span class="p">)</span>

    <span class="k">class</span> <span class="nc">Index</span><span class="p">:</span>
        <span class="n">name</span> <span class="o">=</span> <span class="s1">'articles'</span>
        <span class="n">settings</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">'number_of_shards'</span><span class="p">:</span> <span class="mi">1</span><span class="p">,</span>
            <span class="s1">'number_of_replicas'</span><span class="p">:</span> <span class="mi">0</span><span class="p">,</span>
        <span class="p">}</span>

    <span class="k">class</span> <span class="nc">Django</span><span class="p">:</span>
        <span class="n">model</span> <span class="o">=</span> <span class="n">Article</span>
        <span class="n">fields</span> <span class="o">=</span> <span class="p">[</span>
            <span class="s1">'title'</span><span class="p">,</span>
            <span class="s1">'content'</span><span class="p">,</span>
            <span class="s1">'created_datetime'</span><span class="p">,</span>
            <span class="s1">'updated_datetime'</span><span class="p">,</span>
        <span class="p">]</span>
</code></pre>
<p>Notes:</p>
<ol>
<li>In order to transform the article type, we added the <code>type</code> attribute to the <code>ArticleDocument</code>.</li>
<li>Because our <code>Article</code> model is in a many-to-many (M:N) relationship with <code>Category</code> and a many-to-one (N:1) relationship with <code>User</code> we needed to take care of the relationships. We did that by adding <code>ObjectField</code> attributes.</li>
</ol>
<li>In order to transform the article type, we added the <code>type</code> attribute to the <code>ArticleDocument</code>.</li>
<li>Because our <code>Article</code> model is in a many-to-many (M:N) relationship with <code>Category</code> and a many-to-one (N:1) relationship with <code>User</code> we needed to take care of the relationships. We did that by adding <code>ObjectField</code> attributes.</li>
<h3 id="populate-elasticsearch">Populate Elasticsearch</h3>
<p>To create and populate the Elasticsearch index and mapping, use the <code>search_index</code> command:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py search_index --rebuild

Deleting index <span class="s1">'users'</span>
Deleting index <span class="s1">'categories'</span>
Deleting index <span class="s1">'articles'</span>
Creating index <span class="s1">'users'</span>
Creating index <span class="s1">'categories'</span>
Creating index <span class="s1">'articles'</span>
Indexing <span class="m">3</span> <span class="s1">'User'</span> objects
Indexing <span class="m">4</span> <span class="s1">'Article'</span> objects
Indexing <span class="m">4</span> <span class="s1">'Category'</span> objects
</code></pre>
<p>You need to run this command every time you change your index settings.</p>
<p>django-elasticsearch-dsl created the appropriate database signals so that your Elasticsearch storage gets updated every time an instance of a model is created, deleted, or edited.</p>
<h2 id="elasticsearch-queries">Elasticsearch Queries</h2>
<p>Before creating the appropriate views, let's look at how Elasticsearch queries work.</p>
<p>We first have to obtain the <code>Search</code> instance. We do that by calling <code>search()</code> on our Document like so:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">blog.documents</span> <span class="kn">import</span> <span class="n">ArticleDocument</span>

<span class="n">search</span> <span class="o">=</span> <span class="n">ArticleDocument</span><span class="o">.</span><span class="n">search</span><span class="p">()</span>
</code></pre>
<p>Feel free to run these queries within the Django shell.</p>
<p>Once we have the <code>Search</code> instance we can pass queries to the <code>query()</code> method and fetch the response:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">elasticsearch_dsl</span> <span class="kn">import</span> <span class="n">Q</span>
<span class="kn">from</span> <span class="nn">blog.documents</span> <span class="kn">import</span> <span class="n">ArticleDocument</span>


<span class="c1"># Looks up all the articles that contain `How to` in the title.</span>
<span class="n">query</span> <span class="o">=</span> <span class="s1">'How to'</span>
<span class="n">q</span> <span class="o">=</span> <span class="n">Q</span><span class="p">(</span>
     <span class="s1">'multi_match'</span><span class="p">,</span>
     <span class="n">query</span><span class="o">=</span><span class="n">query</span><span class="p">,</span>
     <span class="n">fields</span><span class="o">=</span><span class="p">[</span>
         <span class="s1">'title'</span>
     <span class="p">])</span>
<span class="n">search</span> <span class="o">=</span> <span class="n">ArticleDocument</span><span class="o">.</span><span class="n">search</span><span class="p">()</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="n">q</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">search</span><span class="o">.</span><span class="n">execute</span><span class="p">()</span>

<span class="c1"># print all the hits</span>
<span class="k">for</span> <span class="n">hit</span> <span class="ow">in</span> <span class="n">search</span><span class="p">:</span>
    <span class="nb">print</span><span class="p">(</span><span class="n">hit</span><span class="o">.</span><span class="n">title</span><span class="p">)</span>
</code></pre>
<p>We can also combine multiple Q statements like so:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">elasticsearch_dsl</span> <span class="kn">import</span> <span class="n">Q</span>
<span class="kn">from</span> <span class="nn">blog.documents</span> <span class="kn">import</span> <span class="n">ArticleDocument</span>

<span class="sd">"""</span>
<span class="sd">Looks up all the articles that:</span>
<span class="sd">1) Contain 'language' in the 'title'</span>
<span class="sd">2) Don't contain 'ruby' or 'javascript' in the 'title'</span>
<span class="sd">3) And contain the query either in the 'title' or 'description'</span>
<span class="sd">"""</span>
<span class="n">query</span> <span class="o">=</span> <span class="s1">'programming'</span>
<span class="n">q</span> <span class="o">=</span> <span class="n">Q</span><span class="p">(</span>
     <span class="s1">'bool'</span><span class="p">,</span>
     <span class="n">must</span><span class="o">=</span><span class="p">[</span>
         <span class="n">Q</span><span class="p">(</span><span class="s1">'match'</span><span class="p">,</span> <span class="n">title</span><span class="o">=</span><span class="s1">'language'</span><span class="p">),</span>
     <span class="p">],</span>
     <span class="n">must_not</span><span class="o">=</span><span class="p">[</span>
         <span class="n">Q</span><span class="p">(</span><span class="s1">'match'</span><span class="p">,</span> <span class="n">title</span><span class="o">=</span><span class="s1">'ruby'</span><span class="p">),</span>
         <span class="n">Q</span><span class="p">(</span><span class="s1">'match'</span><span class="p">,</span> <span class="n">title</span><span class="o">=</span><span class="s1">'javascript'</span><span class="p">),</span>
     <span class="p">],</span>
     <span class="n">should</span><span class="o">=</span><span class="p">[</span>
         <span class="n">Q</span><span class="p">(</span><span class="s1">'match'</span><span class="p">,</span> <span class="n">title</span><span class="o">=</span><span class="n">query</span><span class="p">),</span>
         <span class="n">Q</span><span class="p">(</span><span class="s1">'match'</span><span class="p">,</span> <span class="n">description</span><span class="o">=</span><span class="n">query</span><span class="p">),</span>
     <span class="p">],</span>
     <span class="n">minimum_should_match</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
<span class="n">search</span> <span class="o">=</span> <span class="n">ArticleDocument</span><span class="o">.</span><span class="n">search</span><span class="p">()</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="n">q</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">search</span><span class="o">.</span><span class="n">execute</span><span class="p">()</span>

<span class="c1"># print all the hits</span>
<span class="k">for</span> <span class="n">hit</span> <span class="ow">in</span> <span class="n">search</span><span class="p">:</span>
    <span class="nb">print</span><span class="p">(</span><span class="n">hit</span><span class="o">.</span><span class="n">title</span><span class="p">)</span>
</code></pre>
<p>Another important thing when working with Elasticsearch queries is fuzziness. Fuzzy queries are queries that allow us to handle typos. They use the <a href="https://en.wikipedia.org/wiki/Levenshtein_distance">Levenshtein Distance Algorithm</a> which calculates the distance between the result in our database and the query.</p>
<p>Let's look at an example.</p>
<p>By running the following query we won't get any results, because the user misspelled 'django'.</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">elasticsearch_dsl</span> <span class="kn">import</span> <span class="n">Q</span>
<span class="kn">from</span> <span class="nn">blog.documents</span> <span class="kn">import</span> <span class="n">ArticleDocument</span>

<span class="n">query</span> <span class="o">=</span> <span class="s1">'djengo'</span>  <span class="c1"># notice the typo</span>
<span class="n">q</span> <span class="o">=</span> <span class="n">Q</span><span class="p">(</span>
     <span class="s1">'multi_match'</span><span class="p">,</span>
     <span class="n">query</span><span class="o">=</span><span class="n">query</span><span class="p">,</span>
     <span class="n">fields</span><span class="o">=</span><span class="p">[</span>
         <span class="s1">'title'</span>
     <span class="p">])</span>
<span class="n">search</span> <span class="o">=</span> <span class="n">ArticleDocument</span><span class="o">.</span><span class="n">search</span><span class="p">()</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="n">q</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">search</span><span class="o">.</span><span class="n">execute</span><span class="p">()</span>

<span class="c1"># print all the hits</span>
<span class="k">for</span> <span class="n">hit</span> <span class="ow">in</span> <span class="n">search</span><span class="p">:</span>
    <span class="nb">print</span><span class="p">(</span><span class="n">hit</span><span class="o">.</span><span class="n">title</span><span class="p">)</span>
</code></pre>
<p>If we enable fuzziness like so:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">elasticsearch_dsl</span> <span class="kn">import</span> <span class="n">Q</span>
<span class="kn">from</span> <span class="nn">blog.documents</span> <span class="kn">import</span> <span class="n">ArticleDocument</span>

<span class="n">query</span> <span class="o">=</span> <span class="s1">'djengo'</span>  <span class="c1"># notice the typo</span>
<span class="n">q</span> <span class="o">=</span> <span class="n">Q</span><span class="p">(</span>
     <span class="s1">'multi_match'</span><span class="p">,</span>
     <span class="n">query</span><span class="o">=</span><span class="n">query</span><span class="p">,</span>
     <span class="n">fields</span><span class="o">=</span><span class="p">[</span>
         <span class="s1">'title'</span>
     <span class="p">],</span>
     <span class="n">fuzziness</span><span class="o">=</span><span class="s1">'auto'</span><span class="p">)</span>
<span class="n">search</span> <span class="o">=</span> <span class="n">ArticleDocument</span><span class="o">.</span><span class="n">search</span><span class="p">()</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="n">q</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">search</span><span class="o">.</span><span class="n">execute</span><span class="p">()</span>

<span class="c1"># print all the hits</span>
<span class="k">for</span> <span class="n">hit</span> <span class="ow">in</span> <span class="n">search</span><span class="p">:</span>
    <span class="nb">print</span><span class="p">(</span><span class="n">hit</span><span class="o">.</span><span class="n">title</span><span class="p">)</span>
</code></pre>
<p>The user will get the correct result.</p>
<p>The difference between a <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html">full-text search</a> and <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html">exact match</a> is that full-text search runs an analyzer on the text before it gets indexed to Elasticsearch. The text gets broken down into different tokens, which are transformed to their root form (e.g., reading -&gt; read). These tokens then get saved into the <a href="https://www.elastic.co/blog/found-elasticsearch-from-the-bottom-up#inverted-indexes-and-index-terms">Inverted Index</a>. Because of that, full-text search yields more results, but takes longer to process.</p>
<p>Elasticsearch has a number of additional features. To get familiar with the API, try implementing:</p>
<ol>
<li>Your own <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html">analyzer</a>.</li>
<li><a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.8/search-suggesters-completion.html">Completion suggester</a> - when a user queries 'j' your app should suggest 'johhny' or 'jess_'.</li>
<li><a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/highlighting.html">Highlighting</a> - when user makes a typo, highlight it (e.g., Linuks -&gt; <em>Linux</em>).</li>
</ol>
<li>Your own <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html">analyzer</a>.</li>
<li><a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.8/search-suggesters-completion.html">Completion suggester</a> - when a user queries 'j' your app should suggest 'johhny' or 'jess_'.</li>
<li><a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/highlighting.html">Highlighting</a> - when user makes a typo, highlight it (e.g., Linuks -&gt; <em>Linux</em>).</li>
<p>You can see all the <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html">Elasticsearch Search APIs</a> here.</p>
<h2 id="search-views">Search Views</h2>
<p>With that, let's create sime views. To make our code more DRY we can use the following abstract class in <em>search/views.py</em>:</p>
<pre><span></span><code><span class="c1"># search/views.py</span>

<span class="kn">import</span> <span class="nn">abc</span>

<span class="kn">from</span> <span class="nn">django.http</span> <span class="kn">import</span> <span class="n">HttpResponse</span>
<span class="kn">from</span> <span class="nn">elasticsearch_dsl</span> <span class="kn">import</span> <span class="n">Q</span>
<span class="kn">from</span> <span class="nn">rest_framework.pagination</span> <span class="kn">import</span> <span class="n">LimitOffsetPagination</span>
<span class="kn">from</span> <span class="nn">rest_framework.views</span> <span class="kn">import</span> <span class="n">APIView</span>


<span class="k">class</span> <span class="nc">PaginatedElasticSearchAPIView</span><span class="p">(</span><span class="n">APIView</span><span class="p">,</span> <span class="n">LimitOffsetPagination</span><span class="p">):</span>
    <span class="n">serializer_class</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">document_class</span> <span class="o">=</span> <span class="kc">None</span>

    <span class="nd">@abc</span><span class="o">.</span><span class="n">abstractmethod</span>
    <span class="k">def</span> <span class="nf">generate_q_expression</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">query</span><span class="p">):</span>
        <span class="sd">"""This method should be overridden</span>
<span class="sd">        and return a Q() expression."""</span>

    <span class="k">def</span> <span class="nf">get</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">request</span><span class="p">,</span> <span class="n">query</span><span class="p">):</span>
        <span class="k">try</span><span class="p">:</span>
            <span class="n">q</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">generate_q_expression</span><span class="p">(</span><span class="n">query</span><span class="p">)</span>
            <span class="n">search</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">document_class</span><span class="o">.</span><span class="n">search</span><span class="p">()</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="n">q</span><span class="p">)</span>
            <span class="n">response</span> <span class="o">=</span> <span class="n">search</span><span class="o">.</span><span class="n">execute</span><span class="p">()</span>

            <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s1">'Found </span><span class="si">{</span><span class="n">response</span><span class="o">.</span><span class="n">hits</span><span class="o">.</span><span class="n">total</span><span class="o">.</span><span class="n">value</span><span class="si">}</span><span class="s1"> hit(s) for query: "</span><span class="si">{</span><span class="n">query</span><span class="si">}</span><span class="s1">"'</span><span class="p">)</span>

            <span class="n">results</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">paginate_queryset</span><span class="p">(</span><span class="n">response</span><span class="p">,</span> <span class="n">request</span><span class="p">,</span> <span class="n">view</span><span class="o">=</span><span class="bp">self</span><span class="p">)</span>
            <span class="n">serializer</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">serializer_class</span><span class="p">(</span><span class="n">results</span><span class="p">,</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
            <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">get_paginated_response</span><span class="p">(</span><span class="n">serializer</span><span class="o">.</span><span class="n">data</span><span class="p">)</span>
        <span class="k">except</span> <span class="ne">Exception</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span>
            <span class="k">return</span> <span class="n">HttpResponse</span><span class="p">(</span><span class="n">e</span><span class="p">,</span> <span class="n">status</span><span class="o">=</span><span class="mi">500</span><span class="p">)</span>
</code></pre>
<p>Notes:</p>
<ol>
<li>To use the class, we have to provide our <code>serializer_class</code> and <code>document_class</code> and override <code>generate_q_expression()</code>.</li>
<li>The class does nothing else than run the <code>generate_q_expression()</code> query, fetch the response, paginate it, and return serialized data.</li>
</ol>
<li>To use the class, we have to provide our <code>serializer_class</code> and <code>document_class</code> and override <code>generate_q_expression()</code>.</li>
<li>The class does nothing else than run the <code>generate_q_expression()</code> query, fetch the response, paginate it, and return serialized data.</li>
<p>All the views should now inherit from <code>PaginatedElasticSearchAPIView</code>:</p>
<pre><span></span><code><span class="c1"># search/views.py</span>

<span class="kn">import</span> <span class="nn">abc</span>

<span class="kn">from</span> <span class="nn">django.http</span> <span class="kn">import</span> <span class="n">HttpResponse</span>
<span class="kn">from</span> <span class="nn">elasticsearch_dsl</span> <span class="kn">import</span> <span class="n">Q</span>
<span class="kn">from</span> <span class="nn">rest_framework.pagination</span> <span class="kn">import</span> <span class="n">LimitOffsetPagination</span>
<span class="kn">from</span> <span class="nn">rest_framework.views</span> <span class="kn">import</span> <span class="n">APIView</span>

<span class="kn">from</span> <span class="nn">blog.documents</span> <span class="kn">import</span> <span class="n">ArticleDocument</span><span class="p">,</span> <span class="n">UserDocument</span><span class="p">,</span> <span class="n">CategoryDocument</span>
<span class="kn">from</span> <span class="nn">blog.serializers</span> <span class="kn">import</span> <span class="n">ArticleSerializer</span><span class="p">,</span> <span class="n">UserSerializer</span><span class="p">,</span> <span class="n">CategorySerializer</span>


<span class="k">class</span> <span class="nc">PaginatedElasticSearchAPIView</span><span class="p">(</span><span class="n">APIView</span><span class="p">,</span> <span class="n">LimitOffsetPagination</span><span class="p">):</span>
    <span class="n">serializer_class</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">document_class</span> <span class="o">=</span> <span class="kc">None</span>

    <span class="nd">@abc</span><span class="o">.</span><span class="n">abstractmethod</span>
    <span class="k">def</span> <span class="nf">generate_q_expression</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">query</span><span class="p">):</span>
        <span class="sd">"""This method should be overridden</span>
<span class="sd">        and return a Q() expression."""</span>

    <span class="k">def</span> <span class="nf">get</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">request</span><span class="p">,</span> <span class="n">query</span><span class="p">):</span>
        <span class="k">try</span><span class="p">:</span>
            <span class="n">q</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">generate_q_expression</span><span class="p">(</span><span class="n">query</span><span class="p">)</span>
            <span class="n">search</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">document_class</span><span class="o">.</span><span class="n">search</span><span class="p">()</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="n">q</span><span class="p">)</span>
            <span class="n">response</span> <span class="o">=</span> <span class="n">search</span><span class="o">.</span><span class="n">execute</span><span class="p">()</span>

            <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s1">'Found </span><span class="si">{</span><span class="n">response</span><span class="o">.</span><span class="n">hits</span><span class="o">.</span><span class="n">total</span><span class="o">.</span><span class="n">value</span><span class="si">}</span><span class="s1"> hit(s) for query: "</span><span class="si">{</span><span class="n">query</span><span class="si">}</span><span class="s1">"'</span><span class="p">)</span>

            <span class="n">results</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">paginate_queryset</span><span class="p">(</span><span class="n">response</span><span class="p">,</span> <span class="n">request</span><span class="p">,</span> <span class="n">view</span><span class="o">=</span><span class="bp">self</span><span class="p">)</span>
            <span class="n">serializer</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">serializer_class</span><span class="p">(</span><span class="n">results</span><span class="p">,</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
            <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">get_paginated_response</span><span class="p">(</span><span class="n">serializer</span><span class="o">.</span><span class="n">data</span><span class="p">)</span>
        <span class="k">except</span> <span class="ne">Exception</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span>
            <span class="k">return</span> <span class="n">HttpResponse</span><span class="p">(</span><span class="n">e</span><span class="p">,</span> <span class="n">status</span><span class="o">=</span><span class="mi">500</span><span class="p">)</span>


<span class="c1"># views</span>


<span class="k">class</span> <span class="nc">SearchUsers</span><span class="p">(</span><span class="n">PaginatedElasticSearchAPIView</span><span class="p">):</span>
    <span class="n">serializer_class</span> <span class="o">=</span> <span class="n">UserSerializer</span>
    <span class="n">document_class</span> <span class="o">=</span> <span class="n">UserDocument</span>

    <span class="k">def</span> <span class="nf">generate_q_expression</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">query</span><span class="p">):</span>
        <span class="k">return</span> <span class="n">Q</span><span class="p">(</span><span class="s1">'bool'</span><span class="p">,</span>
                 <span class="n">should</span><span class="o">=</span><span class="p">[</span>
                     <span class="n">Q</span><span class="p">(</span><span class="s1">'match'</span><span class="p">,</span> <span class="n">username</span><span class="o">=</span><span class="n">query</span><span class="p">),</span>
                     <span class="n">Q</span><span class="p">(</span><span class="s1">'match'</span><span class="p">,</span> <span class="n">first_name</span><span class="o">=</span><span class="n">query</span><span class="p">),</span>
                     <span class="n">Q</span><span class="p">(</span><span class="s1">'match'</span><span class="p">,</span> <span class="n">last_name</span><span class="o">=</span><span class="n">query</span><span class="p">),</span>
                 <span class="p">],</span> <span class="n">minimum_should_match</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>


<span class="k">class</span> <span class="nc">SearchCategories</span><span class="p">(</span><span class="n">PaginatedElasticSearchAPIView</span><span class="p">):</span>
    <span class="n">serializer_class</span> <span class="o">=</span> <span class="n">CategorySerializer</span>
    <span class="n">document_class</span> <span class="o">=</span> <span class="n">CategoryDocument</span>

    <span class="k">def</span> <span class="nf">generate_q_expression</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">query</span><span class="p">):</span>
        <span class="k">return</span> <span class="n">Q</span><span class="p">(</span>
                <span class="s1">'multi_match'</span><span class="p">,</span> <span class="n">query</span><span class="o">=</span><span class="n">query</span><span class="p">,</span>
                <span class="n">fields</span><span class="o">=</span><span class="p">[</span>
                    <span class="s1">'name'</span><span class="p">,</span>
                    <span class="s1">'description'</span><span class="p">,</span>
                <span class="p">],</span> <span class="n">fuzziness</span><span class="o">=</span><span class="s1">'auto'</span><span class="p">)</span>


<span class="k">class</span> <span class="nc">SearchArticles</span><span class="p">(</span><span class="n">PaginatedElasticSearchAPIView</span><span class="p">):</span>
    <span class="n">serializer_class</span> <span class="o">=</span> <span class="n">ArticleSerializer</span>
    <span class="n">document_class</span> <span class="o">=</span> <span class="n">ArticleDocument</span>

    <span class="k">def</span> <span class="nf">generate_q_expression</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">query</span><span class="p">):</span>
        <span class="k">return</span> <span class="n">Q</span><span class="p">(</span>
                <span class="s1">'multi_match'</span><span class="p">,</span> <span class="n">query</span><span class="o">=</span><span class="n">query</span><span class="p">,</span>
                <span class="n">fields</span><span class="o">=</span><span class="p">[</span>
                    <span class="s1">'title'</span><span class="p">,</span>
                    <span class="s1">'author'</span><span class="p">,</span>
                    <span class="s1">'type'</span><span class="p">,</span>
                    <span class="s1">'content'</span>
                <span class="p">],</span> <span class="n">fuzziness</span><span class="o">=</span><span class="s1">'auto'</span><span class="p">)</span>
</code></pre>
<h3 id="define-urls_1">Define URLs</h3>
<p>Lastly, let's create the URLs for our views:</p>
<pre><span></span><code><span class="c1"># search.urls.py</span>

<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span>

<span class="kn">from</span> <span class="nn">search.views</span> <span class="kn">import</span> <span class="n">SearchArticles</span><span class="p">,</span> <span class="n">SearchCategories</span><span class="p">,</span> <span class="n">SearchUsers</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
    <span class="n">path</span><span class="p">(</span><span class="s1">'user/&lt;str:query&gt;/'</span><span class="p">,</span> <span class="n">SearchUsers</span><span class="o">.</span><span class="n">as_view</span><span class="p">()),</span>
    <span class="n">path</span><span class="p">(</span><span class="s1">'category/&lt;str:query&gt;/'</span><span class="p">,</span> <span class="n">SearchCategories</span><span class="o">.</span><span class="n">as_view</span><span class="p">()),</span>
    <span class="n">path</span><span class="p">(</span><span class="s1">'article/&lt;str:query&gt;/'</span><span class="p">,</span> <span class="n">SearchArticles</span><span class="o">.</span><span class="n">as_view</span><span class="p">()),</span>
<span class="p">]</span>
</code></pre>
<p>Then, wire up the app URLs to the project URLs:</p>
<pre><span></span><code><span class="c1"># core/urls.py</span>

<span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>
<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span><span class="p">,</span> <span class="n">include</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
    <span class="n">path</span><span class="p">(</span><span class="s1">'blog/'</span><span class="p">,</span> <span class="n">include</span><span class="p">(</span><span class="s1">'blog.urls'</span><span class="p">)),</span>
    <span class="n">path</span><span class="p">(</span><span class="s1">'search/'</span><span class="p">,</span> <span class="n">include</span><span class="p">(</span><span class="s1">'search.urls'</span><span class="p">)),</span> <span class="c1"># new</span>
    <span class="n">path</span><span class="p">(</span><span class="s1">'admin/'</span><span class="p">,</span> <span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">urls</span><span class="p">),</span>
<span class="p">]</span>
</code></pre>
<h3 id="testing_1">Testing</h3>
<p>Our web application is done. We can test our search endpoints by visiting the following URLs:</p>
<p>Notice the typo with the fourth request. We spelled 'progreming', but still got the correct result thanks to fuzziness.</p>
<h2 id="alternative-libraries">Alternative Libraries</h2>
<p>The path we took isn't the only way to integrate Django with Elasticsearch. There are a few other libraries you <em>might</em> want to check out:</p>
<ol>
<li><a href="https://django-elasticsearch-dsl-drf.readthedocs.io/en/latest/">django-elasicsearch-dsl-drf</a> is a wrapper around Elasticsearch and Django REST Framework. It provides views, serializers, filter backends, pagination and more. It works well, but it might be overkill for smaller projects. I'd recommend using it if you need advanced Elasticsearch features.</li>
<li><a href="https://haystacksearch.org/">Haystack</a> is a wrapper for a number of search backends, like Elasticsearch, <a href="https://lucene.apache.org/solr/">Solr</a>, and <a href="https://github.com/mchaput/whoosh/">Whoosh</a>. It allows you to write your search code once and reuse it with different search backends. It works great for implementing a simple search box. Because Haystack is another abstraction layer, there's more overhead involved so you shouldn't use it if performance is really important or if you're working with big amounts of data. It also requires some configuration.</li>
<li><a href="https://github.com/rhblind/drf-haystack">Haystack for Django REST Framework</a> is a small library which tries to simplify integration of Haystack with Django REST Framework. At the time of writing, the project is a bit outdated and their documentation is badly written. I've spent a decent amount of time trying to get it to work with no luck.</li>
</ol>
<li><a href="https://django-elasticsearch-dsl-drf.readthedocs.io/en/latest/">django-elasicsearch-dsl-drf</a> is a wrapper around Elasticsearch and Django REST Framework. It provides views, serializers, filter backends, pagination and more. It works well, but it might be overkill for smaller projects. I'd recommend using it if you need advanced Elasticsearch features.</li>
<li><a href="https://haystacksearch.org/">Haystack</a> is a wrapper for a number of search backends, like Elasticsearch, <a href="https://lucene.apache.org/solr/">Solr</a>, and <a href="https://github.com/mchaput/whoosh/">Whoosh</a>. It allows you to write your search code once and reuse it with different search backends. It works great for implementing a simple search box. Because Haystack is another abstraction layer, there's more overhead involved so you shouldn't use it if performance is really important or if you're working with big amounts of data. It also requires some configuration.</li>
<li><a href="https://github.com/rhblind/drf-haystack">Haystack for Django REST Framework</a> is a small library which tries to simplify integration of Haystack with Django REST Framework. At the time of writing, the project is a bit outdated and their documentation is badly written. I've spent a decent amount of time trying to get it to work with no luck.</li>
<h2 id="conclusion">Conclusion</h2>
<p>In this tutorial, you learned the basics of working with Django REST Framework and Elasticsearch. You now know how to integrate them, create Elasticsearch documents and queries, and serve the data via a RESTful API.</p>
<p>Before launching your project in production, consider using one of the managed Elasticsearch services like <a href="https://www.elastic.co/pricing/">Elastic Cloud</a>, <a href="https://aws.amazon.com/elasticsearch-service/">Amazon Elasticsearch Service</a>, or <a href="https://azure.microsoft.com/en-us/overview/linux-on-azure/elastic/">Elastic on Azure</a>. The cost of using a managed service will be higher than managing your own cluster, but they provide all of the infrastructure required for deploying, securing, and running Elasticsearch clusters. Plus, they'll handle version updates, regular backups, and scaling.</p>
<p>Grab the code from <a href="https://github.com/testdrivenio/django-drf-elasticsearch">django-drf-elasticsearch</a> repo on GitHub.</p>
<h2 class="author-card-name">
<a href="https://testdriven.io/authors/tomazic/">Nik Tomazic</a>
</h2>
<p>Nik is a software developer from Slovenia. He's interested in object-oriented programming and web development. He likes learning new things and accepting new challenges. When he's not coding, Nik's either swimming or watching movies.</p>
<li>
<a aria-label="GitHub" href="https://github.com/duplxey">
<i aria-hidden="true" class="fab fa-github"></i>
</a>
</li>
<li>
<a aria-label="Personal Site" href="https://duplxey.com/">
<i aria-hidden="true" class="fas fa-globe"></i>
</a>
</li>
<h2 class="eyebrow mb-0">Share this tutorial</h2>
<h2 class="social-share-heading sr-only">Share this tutorial</h2>
<li>
<a aria-label="Twitter" class="btn social-share-link twitter" data-a-social-share="Twitter" href="https://twitter.com/intent/tweet/?text=Django%20REST%20Framework%20and%20Elasticsearch%20from%20%40TestDrivenio&amp;url=https%3A//testdriven.io/blog/django-drf-elasticsearch/" rel="noopener" target="_blank">
<span aria-hidden="true">
<i class="fab fa-twitter"></i>
<span class="label">Twitter</span>
</span>
</a>
</li>
<li>
<a aria-label="Reddit" class="btn social-share-link reddit" data-a-social-share="Reddit" href="https://reddit.com/submit/?url=https%3A//testdriven.io/blog/django-drf-elasticsearch/&amp;resubmit=true&amp;title=Django%20REST%20Framework%20and%20Elasticsearch" rel="noopener" target="_blank">
<span aria-hidden="true">
<i class="fab fa-reddit-alien"></i>
<span class="label">Reddit</span>
</span>
</a>
</li>
<li>
<a aria-label="Hacker News" class="btn social-share-link hackernews" data-a-social-share="HackerNews" href="https://news.ycombinator.com/submitlink?u=https%3A//testdriven.io/blog/django-drf-elasticsearch/&amp;t=Django%20REST%20Framework%20and%20Elasticsearch" rel="noopener" target="_blank">
<span aria-hidden="true">
<i class="fab fa-hacker-news"></i>
<span class="label">Hacker News</span>
</span>
</a>
</li>
<li>
<a aria-label="Facebook" class="btn social-share-link facebook" data-a-social-share="Facebook" href="https://facebook.com/sharer/sharer.php?u=https%3A//testdriven.io/blog/django-drf-elasticsearch/" rel="noopener" target="_blank">
<span aria-hidden="true">
<i aria-hidden="true" class="fab fa-facebook-square"></i>
<span class="label">Facebook</span>
</span>
</a>
</li>
<h2 class="course-card-heading"><a href="https://testdriven.io/courses/django-full-text-search/">Full-text Search in Django with Postgres and Elasticsearch</a></h2>
<p class="course-card-description">Learn how to add full-text search to Django with both Postgres and Elasticsearch.</p>
<h3 class="eyebrow">Tutorial Topics</h3>
<h3 class="eyebrow blog-toc-heading">Table of Contents</h3>
<ol data-local-nav-list="" id="blog-toc"><li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#what-is-elasticsearch">What is Elasticsearch?</a></li><li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#elasticsearch-structure-and-concepts">Elasticsearch Structure and Concepts</a></li><li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#elasticsearch-vs-postgresql-full-text-search">Elasticsearch vs PostgreSQL Full-text Search</a></li><li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#project-setup">Project Setup</a></li><li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#database-models">Database Models</a></li><li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#django-rest-framework">Django REST Framework</a></li><li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#elasticsearch-setup">Elasticsearch Setup</a></li><li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#creating-documents">Creating Documents</a></li><li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#elasticsearch-queries">Elasticsearch Queries</a></li><li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#search-views">Search Views</a></li><li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#alternative-libraries">Alternative Libraries</a></li><li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#conclusion">Conclusion</a></li></ol>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#what-is-elasticsearch">What is Elasticsearch?</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#elasticsearch-structure-and-concepts">Elasticsearch Structure and Concepts</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#elasticsearch-vs-postgresql-full-text-search">Elasticsearch vs PostgreSQL Full-text Search</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#project-setup">Project Setup</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#database-models">Database Models</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#django-rest-framework">Django REST Framework</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#elasticsearch-setup">Elasticsearch Setup</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#creating-documents">Creating Documents</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#elasticsearch-queries">Elasticsearch Queries</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#search-views">Search Views</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#alternative-libraries">Alternative Libraries</a></li>
<li><a href="https://testdriven.io/blog/django-drf-elasticsearch/#conclusion">Conclusion</a></li>
<h2 class="course-card-heading"><a href="https://testdriven.io/courses/django-full-text-search/">Full-text Search in Django with Postgres and Elasticsearch</a></h2>
<p class="course-card-description">Learn how to add full-text search to Django with both Postgres and Elasticsearch.</p>
<h2 class="eyebrow">Recommended Tutorials</h2>
<h2 class="signup-ribbon-heading">Stay Sharp with Course Updates</h2>
<p class="lead">Join our mailing list to be notified about updates and new releases.</p>
<li>
<span class="footer-nav-heading">Learn</span>
<ul>
<li>
<a href="https://testdriven.io/courses/">Courses</a>
</li>
<li>
<a href="https://testdriven.io/bundles/">Bundles</a>
</li>
<li>
<a href="https://testdriven.io/blog/">Blog</a>
</li>
</ul>
</li>
<li>
<a href="https://testdriven.io/courses/">Courses</a>
</li>
<li>
<a href="https://testdriven.io/bundles/">Bundles</a>
</li>
<li>
<a href="https://testdriven.io/blog/">Blog</a>
</li>
<li>
<span class="footer-nav-heading">Guides</span>
<ul>
<li><a href="https://testdriven.io/guides/complete-python/">Complete Python</a></li>
<li><a href="https://testdriven.io/guides/django-celery/">Django and Celery</a></li>
<li><a href="https://testdriven.io/guides/flask-deep-dive/">Deep Dive Into Flask</a></li>
</ul>
</li>
<li><a href="https://testdriven.io/guides/complete-python/">Complete Python</a></li>
<li><a href="https://testdriven.io/guides/django-celery/">Django and Celery</a></li>
<li><a href="https://testdriven.io/guides/flask-deep-dive/">Deep Dive Into Flask</a></li>
<li>
<span class="footer-nav-heading">About TestDriven.io</span>
<ul>
<li><a href="https://testdriven.io/support/">Support and Consulting</a></li>
<li><a href="https://testdriven.io/test-driven-development/">What is Test-Driven Development?</a></li>
<li><a href="https://testdriven.io/testimonials/">Testimonials</a></li>
<li><a href="https://testdriven.io/opensource/">Open Source Donations</a></li>
<li><a href="https://testdriven.io/about/">About Us</a></li>
<li><a href="https://testdriven.io/authors/">Meet the Authors</a></li>
<li><a href="https://testdriven.io/tips/">Tips and Tricks</a></li>
</ul>
</li>
<li><a href="https://testdriven.io/support/">Support and Consulting</a></li>
<li><a href="https://testdriven.io/test-driven-development/">What is Test-Driven Development?</a></li>
<li><a href="https://testdriven.io/testimonials/">Testimonials</a></li>
<li><a href="https://testdriven.io/opensource/">Open Source Donations</a></li>
<li><a href="https://testdriven.io/about/">About Us</a></li>
<li><a href="https://testdriven.io/authors/">Meet the Authors</a></li>
<li><a href="https://testdriven.io/tips/">Tips and Tricks</a></li>
<h3 class="donation-blurb-heading">TestDriven.io is a proud supporter of open source</h3>
<p>
<strong>10% of profits</strong> from each of our <a href="https://testdriven.io/courses/topics/fastapi/">FastAPI</a> courses and our <a href="https://testdriven.io/courses/learn-flask/">Flask Web Development</a> course will be donated to the FastAPI and Flask teams, respectively.
            <br/>
</p>
<p>
<span>© Copyright 2017 - 2022 TestDriven Labs.</span>
<br/>
<span>Developed by </span>
<a href="http://mherman.org/">Michael Herman</a>.
          </p>
<p><small class="copyright">
</small>
</p>
<h5 class="modal-title" id="feedbackModalTitle">Send Us Feedback</h5>
<h4 class="thankyou-message"></h4>
