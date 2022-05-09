---
layout: post
title: Simple-Blog-App-Using-Django-and-Elasticsearch
date: 2019-03-07 16:20:23 +0900
category: Python
tag: Python
---

## A Simple-Blog-App-Using-Django-and-Elasticsearch: 

### This project will consist of multiple models, which will be serialized and served via <a href="https://www.django-rest-framework.org/">Django REST Framework</a>.

<html lang="en">
<head>
</head>
<body>
<div class="container">
<div class="content">


<h2 id="project-setup">Project Setup</h2>
<p> After integrating Elasticsearch, we'll create an endpoint that will allow us to look up different authors, categories, and articles.</p>
<p>To keep our code clean and modular, we'll split our project into the following two apps:</p>
<ol>
<li><code>blog</code> - for our Django models, serializers, and ViewSets</li>
<li><code>search</code> - for Elasticsearch documents, indexes, and queries</li>
</ol>
<p>Start by creating a new directory and setting up a new Django project:</p>
<div class="codehilite"><pre><span></span><code>$ mkdir django-drf-elasticsearch <span class="o">&amp;&amp;</span> <span class="nb">cd</span> django-drf-elasticsearch
$ python3.9 -m venv env
$ <span class="nb">source</span> env/bin/activate

<span class="o">(</span>env<span class="o">)</span>$ pip install <span class="nv">django</span><span class="o">==</span><span class="m">3</span>.2.6
<span class="o">(</span>env<span class="o">)</span>$ django-admin.py startproject core .
</code></pre></div>

<p>After that, create a new app called <code>blog</code>:</p>
<div class="codehilite"><pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py startapp blog
</code></pre></div>

<p>Register the app in <em>core/settings.py</em> under <code>INSTALLED_APPS</code>:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
<span class="s1">&#39;django.contrib.admin&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.auth&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.contenttypes&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.sessions&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.messages&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.staticfiles&#39;</span><span class="p">,</span>
<span class="s1">&#39;blog.apps.BlogConfig&#39;</span><span class="p">,</span> <span class="c1"># new</span>
<span class="p">]</span>
</code></pre></div>

<h2 id="database-models">Database Models</h2>
<p>Next, create <code>Category</code> and <code>Article</code> models in <em>blog/models.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># blog/models.py</span>

<span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>


<span class="k">class</span> <span class="nc">Category</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">name</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">32</span><span class="p">)</span>
<span class="n">description</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">TextField</span><span class="p">(</span><span class="n">null</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
<span class="n">verbose_name_plural</span> <span class="o">=</span> <span class="s1">&#39;categories&#39;</span>

<span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">name</span><span class="si">}</span><span class="s1">&#39;</span>


<span class="n">ARTICLE_TYPES</span> <span class="o">=</span> <span class="p">[</span>
<span class="p">(</span><span class="s1">&#39;UN&#39;</span><span class="p">,</span> <span class="s1">&#39;Unspecified&#39;</span><span class="p">),</span>
<span class="p">(</span><span class="s1">&#39;TU&#39;</span><span class="p">,</span> <span class="s1">&#39;Tutorial&#39;</span><span class="p">),</span>
<span class="p">(</span><span class="s1">&#39;RS&#39;</span><span class="p">,</span> <span class="s1">&#39;Research&#39;</span><span class="p">),</span>
<span class="p">(</span><span class="s1">&#39;RW&#39;</span><span class="p">,</span> <span class="s1">&#39;Review&#39;</span><span class="p">),</span>
<span class="p">]</span>


<span class="k">class</span> <span class="nc">Article</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">title</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">256</span><span class="p">)</span>
<span class="n">author</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">ForeignKey</span><span class="p">(</span><span class="n">to</span><span class="o">=</span><span class="n">User</span><span class="p">,</span> <span class="n">on_delete</span><span class="o">=</span><span class="n">models</span><span class="o">.</span><span class="n">CASCADE</span><span class="p">)</span>
<span class="nb">type</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="n">ARTICLE_TYPES</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="s1">&#39;UN&#39;</span><span class="p">)</span>
<span class="n">categories</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">ManyToManyField</span><span class="p">(</span><span class="n">to</span><span class="o">=</span><span class="n">Category</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">related_name</span><span class="o">=</span><span class="s1">&#39;categories&#39;</span><span class="p">)</span>
<span class="n">content</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">TextField</span><span class="p">()</span>
<span class="n">created_datetime</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now_add</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="n">updated_datetime</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">author</span><span class="si">}</span><span class="s1">: </span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">title</span><span class="si">}</span><span class="s1"> (</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">created_datetime</span><span class="o">.</span><span class="n">date</span><span class="p">()</span><span class="si">}</span><span class="s1">)&#39;</span>
</code></pre></div>

<p>Notes:</p>
<ol>
<li><code>Category</code> represents an article category -- i.e, programming, Linux, testing.</li>
<li><code>Article</code> represents an individual article. Each article can have multiple categories. Articles have a specific type -- <code>Tutorial</code>, <code>Research</code>, <code>Review</code>, or <code>Unspecified</code>.</li>
<li>Authors are represented by the default Django user model.</li>
</ol>
<h3 id="run-migrations">Run Migrations</h3>
<p>Make migrations and then apply them:</p>
<div class="codehilite"><pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py makemigrations
<span class="o">(</span>env<span class="o">)</span>$ python manage.py migrate
</code></pre></div>

<p>Register the models in <em>blog/admin.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># blog/admin.py</span>

<span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>

<span class="kn">from</span> <span class="nn">blog.models</span> <span class="kn">import</span> <span class="n">Category</span><span class="p">,</span> <span class="n">Article</span>


<span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="n">Category</span><span class="p">)</span>
<span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="n">Article</span><span class="p">)</span>
</code></pre></div>

<h3 id="populate-the-database">Populate the Database</h3>
<p>Before moving to the next step, we need some data to work with. I've created a simple command we can use to populate the database.</p>
<p>Create a new folder in "blog" called "management", and then inside that folder create another folder called "commands". Inside of the "commands" folder, create a new file called <em>populate_db.py</em>.</p>
<div class="codehilite"><pre><span></span><code>management
└── commands
└── populate_db.py
</code></pre></div>

<p>Copy the file contents from <a href="https://github.com/testdrivenio/django-drf-elasticsearch/blob/main/blog/management/commands/populate_db.py">populate_db.py</a> and paste it inside your <em>populate_db.py</em>.</p>
<p>Run the following command to populate the DB:</p>
<div class="codehilite"><pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py populate_db
</code></pre></div>

<p>If everything went well you should see a <code>Successfully populated the database.</code> message in the console and there should be a few articles in your database.</p>
<h2 id="django-rest-framework">Django REST Framework</h2>
<p>Now let's install <code>djangorestframework</code> using pip:</p>
<div class="codehilite"><pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ pip install <span class="nv">djangorestframework</span><span class="o">==</span><span class="m">3</span>.12.4
</code></pre></div>

<p>Register it in our <em>settings.py</em> like so:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
<span class="s1">&#39;django.contrib.admin&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.auth&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.contenttypes&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.sessions&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.messages&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.staticfiles&#39;</span><span class="p">,</span>
<span class="s1">&#39;blog.apps.BlogConfig&#39;</span><span class="p">,</span>
<span class="s1">&#39;rest_framework&#39;</span><span class="p">,</span> <span class="c1"># new</span>
<span class="p">]</span>
</code></pre></div>

<p>Add the following settings:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">REST_FRAMEWORK</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">&#39;DEFAULT_PAGINATION_CLASS&#39;</span><span class="p">:</span> <span class="s1">&#39;rest_framework.pagination.LimitOffsetPagination&#39;</span><span class="p">,</span>
<span class="s1">&#39;PAGE_SIZE&#39;</span><span class="p">:</span> <span class="mi">25</span>
<span class="p">}</span>
</code></pre></div>

<p>We'll need these settings to implement pagination.</p>
<h3 id="create-serializers">Create Serializers</h3>
<p>To serialize our Django models, we need to create a serializer for each of them. The easiest way to create serializers that depend on Django models is by using the <code>ModelSerializer</code> class.</p>
<p><em>blog/serializers.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># blog/serializers.py</span>

<span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">rest_framework</span> <span class="kn">import</span> <span class="n">serializers</span>

<span class="kn">from</span> <span class="nn">blog.models</span> <span class="kn">import</span> <span class="n">Article</span><span class="p">,</span> <span class="n">Category</span>


<span class="k">class</span> <span class="nc">UserSerializer</span><span class="p">(</span><span class="n">serializers</span><span class="o">.</span><span class="n">ModelSerializer</span><span class="p">):</span>
<span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">User</span>
<span class="n">fields</span> <span class="o">=</span> <span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="s1">&#39;username&#39;</span><span class="p">,</span> <span class="s1">&#39;first_name&#39;</span><span class="p">,</span> <span class="s1">&#39;last_name&#39;</span><span class="p">)</span>


<span class="k">class</span> <span class="nc">CategorySerializer</span><span class="p">(</span><span class="n">serializers</span><span class="o">.</span><span class="n">ModelSerializer</span><span class="p">):</span>
<span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Category</span>
<span class="n">fields</span> <span class="o">=</span> <span class="s1">&#39;__all__&#39;</span>


<span class="k">class</span> <span class="nc">ArticleSerializer</span><span class="p">(</span><span class="n">serializers</span><span class="o">.</span><span class="n">ModelSerializer</span><span class="p">):</span>
<span class="n">author</span> <span class="o">=</span> <span class="n">UserSerializer</span><span class="p">()</span>
<span class="n">categories</span> <span class="o">=</span> <span class="n">CategorySerializer</span><span class="p">(</span><span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Article</span>
<span class="n">fields</span> <span class="o">=</span> <span class="s1">&#39;__all__&#39;</span>
</code></pre></div>

<p>Notes:</p>
<ol>
<li><code>UserSerializer</code> and <code>CategorySerializer</code> are fairly simple: We just provided the fields we want serialized.</li>
<li>In the <code>ArticleSerializer</code>, we needed to take care of the relationships to make sure they also get serialized. This is why we provided <code>UserSerializer</code> and <code>CategorySerializer</code>.</li>
</ol>
<h3 id="create-viewsets">Create ViewSets</h3>
<p>Let's create a ViewSet for each of our models in <em>blog/views.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># blog/views.py</span>

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
</code></pre></div>

<p>In this block of code, we created the ViewSets by providing the <code>serializer_class</code> and <code>queryset</code> for each ViewSet.</p>
<h3 id="define-urls">Define URLs</h3>
<p>Create the app-level URLs for the ViewSets:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># blog/urls.py</span>

<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span><span class="p">,</span> <span class="n">include</span>
<span class="kn">from</span> <span class="nn">rest_framework</span> <span class="kn">import</span> <span class="n">routers</span>

<span class="kn">from</span> <span class="nn">blog.views</span> <span class="kn">import</span> <span class="n">UserViewSet</span><span class="p">,</span> <span class="n">CategoryViewSet</span><span class="p">,</span> <span class="n">ArticleViewSet</span>

<span class="n">router</span> <span class="o">=</span> <span class="n">routers</span><span class="o">.</span><span class="n">DefaultRouter</span><span class="p">()</span>
<span class="n">router</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="sa">r</span><span class="s1">&#39;user&#39;</span><span class="p">,</span> <span class="n">UserViewSet</span><span class="p">)</span>
<span class="n">router</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="sa">r</span><span class="s1">&#39;category&#39;</span><span class="p">,</span> <span class="n">CategoryViewSet</span><span class="p">)</span>
<span class="n">router</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="sa">r</span><span class="s1">&#39;article&#39;</span><span class="p">,</span> <span class="n">ArticleViewSet</span><span class="p">)</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">path</span><span class="p">(</span><span class="s1">&#39;&#39;</span><span class="p">,</span> <span class="n">include</span><span class="p">(</span><span class="n">router</span><span class="o">.</span><span class="n">urls</span><span class="p">)),</span>
<span class="p">]</span>
</code></pre></div>

<p>Then, wire up the app URLs to the project URLs:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># core/urls.py</span>

<span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>
<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span><span class="p">,</span> <span class="n">include</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">path</span><span class="p">(</span><span class="s1">&#39;blog/&#39;</span><span class="p">,</span> <span class="n">include</span><span class="p">(</span><span class="s1">&#39;blog.urls&#39;</span><span class="p">)),</span>
<span class="n">path</span><span class="p">(</span><span class="s1">&#39;admin/&#39;</span><span class="p">,</span> <span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">urls</span><span class="p">),</span>
<span class="p">]</span>
</code></pre></div>

<p>Our app now has the following URLs:</p>
<ol>
<li><code>/blog/user/</code> lists all users</li>
<li><code>/blog/user/&lt;USER_ID&gt;/</code> fetches a specific user</li>
<li><code>/blog/category/</code> lists all categories</li>
<li><code>/blog/category/&lt;CATEGORY_ID&gt;/</code> fetches a specific category</li>
<li><code>/blog/article/</code> lists all articles</li>
<li><code>/blog/article/&lt;ARTICLE_ID&gt;/</code> fetches a specific article</li>
</ol>
<h3 id="testing">Testing</h3>
<p>Now that we've registered the URLs, we can test the endpoints to see if everything works correctly.</p>
<p>Run the development server:</p>
<div class="codehilite"><pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py runserver
</code></pre></div>

<p>Then, in your browser of choice, navigate to <a href="http://127.0.0.1:8000/blog/article/">http://127.0.0.1:8000/blog/article/</a>. The response should look something like this:</p>
<div class="codehilite"><pre><span></span><code><span class="p">{</span><span class="w"></span>
<span class="w">    </span><span class="nt">&quot;count&quot;</span><span class="p">:</span><span class="w"> </span><span class="mi">4</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="nt">&quot;next&quot;</span><span class="p">:</span><span class="w"> </span><span class="kc">null</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="nt">&quot;previous&quot;</span><span class="p">:</span><span class="w"> </span><span class="kc">null</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="nt">&quot;results&quot;</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w"></span>
<span class="w">        </span><span class="p">{</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;id&quot;</span><span class="p">:</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;author&quot;</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w"></span>
<span class="w">                </span><span class="nt">&quot;id&quot;</span><span class="p">:</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"></span>
<span class="w">                </span><span class="nt">&quot;username&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;jess_&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">                </span><span class="nt">&quot;first_name&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;Jess&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">                </span><span class="nt">&quot;last_name&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;Brown&quot;</span><span class="w"></span>
<span class="w">            </span><span class="p">},</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;categories&quot;</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w"></span>
<span class="w">                </span><span class="p">{</span><span class="w"></span>
<span class="w">                    </span><span class="nt">&quot;id&quot;</span><span class="p">:</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"></span>
<span class="w">                    </span><span class="nt">&quot;name&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;SEO optimization&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">                    </span><span class="nt">&quot;description&quot;</span><span class="p">:</span><span class="w"> </span><span class="kc">null</span><span class="w"></span>
<span class="w">                </span><span class="p">}</span><span class="w"></span>
<span class="w">            </span><span class="p">],</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;title&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;How to improve your Google rating?&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;type&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;TU&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;content&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;Firstly, add the correct SEO tags...&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;created_datetime&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;2021-08-12T17:34:31.271610Z&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;updated_datetime&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;2021-08-12T17:34:31.322165Z&quot;</span><span class="w"></span>
<span class="w">        </span><span class="p">},</span><span class="w"></span>
<span class="w">        </span><span class="p">{</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;id&quot;</span><span class="p">:</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;author&quot;</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w"></span>
<span class="w">                </span><span class="nt">&quot;id&quot;</span><span class="p">:</span><span class="w"> </span><span class="mi">4</span><span class="p">,</span><span class="w"></span>
<span class="w">                </span><span class="nt">&quot;username&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;johnny&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">                </span><span class="nt">&quot;first_name&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;Johnny&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">                </span><span class="nt">&quot;last_name&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;Davis&quot;</span><span class="w"></span>
<span class="w">            </span><span class="p">},</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;categories&quot;</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="w"></span>
<span class="w">                </span><span class="p">{</span><span class="w"></span>
<span class="w">                    </span><span class="nt">&quot;id&quot;</span><span class="p">:</span><span class="w"> </span><span class="mi">4</span><span class="p">,</span><span class="w"></span>
<span class="w">                    </span><span class="nt">&quot;name&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;Programming&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">                    </span><span class="nt">&quot;description&quot;</span><span class="p">:</span><span class="w"> </span><span class="kc">null</span><span class="w"></span>
<span class="w">                </span><span class="p">}</span><span class="w"></span>
<span class="w">            </span><span class="p">],</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;title&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;Installing latest version of Ubuntu&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;type&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;TU&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;content&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;In this tutorial, we&#39;ll take a look at how to setup the latest version of Ubuntu. Ubuntu (/ʊˈbʊntuː/ is a Linux distribution based on Debian and composed mostly of free and open-source software. Ubuntu is officially released in three editions: Desktop, Server, and Core for Internet of things devices and robots.&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;created_datetime&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;2021-08-12T17:34:31.540628Z&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">            </span><span class="nt">&quot;updated_datetime&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;2021-08-12T17:34:31.592555Z&quot;</span><span class="w"></span>
<span class="w">        </span><span class="p">},</span><span class="w"></span>
<span class="w">        </span><span class="err">...</span><span class="w"></span>
<span class="w">    </span><span class="p">]</span><span class="w"></span>
<span class="p">}</span><span class="w"></span>
</code></pre></div>

<p>Manually test the other endpoints as well.</p>
<h2 id="elasticsearch-setup">Elasticsearch Setup</h2>
<p>Start by installing and running Elasticsearch in the background.</p>

<p>To integrate Elasticsearch with Django, we need to install the following packages:</p>
<ol>
<li><a href="https://elasticsearch-py.readthedocs.io/en/7.x/">elasticsearch</a> - official low-level Python client for Elasticsearch</li>
<li><a href="https://elasticsearch-dsl.readthedocs.io/en/latest/">elasticsearch-dsl-py</a> - high-level library for writing and running queries against Elasticsearch</li>
<li><a href="https://django-elasticsearch-dsl.readthedocs.io/en/latest/">django-elasticsearch-dsl</a> - wrapper around elasticsearch-dsl-py that allows indexing Django models in Elasticsearch</li>
</ol>
<p>Install:</p>
<div class="codehilite"><pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ pip install <span class="nv">elasticsearch</span><span class="o">==</span><span class="m">7</span>.14.0
<span class="o">(</span>env<span class="o">)</span>$ pip install elasticsearch-dsl<span class="o">==</span><span class="m">7</span>.4.0
<span class="o">(</span>env<span class="o">)</span>$ pip install django-elasticsearch-dsl<span class="o">==</span><span class="m">7</span>.2.0
</code></pre></div>

<p>Start a new app called <code>search</code>, which will hold our Elasticsearch documents, indexes, and queries:</p>
<div class="codehilite"><pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py startapp search
</code></pre></div>

<p>Register the <code>search</code> and <code>django_elasticsearch_dsl</code> in <em>core/settings.py</em> under <code>INSTALLED_APPS</code>:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
<span class="s1">&#39;django.contrib.admin&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.auth&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.contenttypes&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.sessions&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.messages&#39;</span><span class="p">,</span>
<span class="s1">&#39;django.contrib.staticfiles&#39;</span><span class="p">,</span>
<span class="s1">&#39;django_elasticsearch_dsl&#39;</span><span class="p">,</span> <span class="c1"># new</span>
<span class="s1">&#39;blog.apps.BlogConfig&#39;</span><span class="p">,</span>
<span class="s1">&#39;search.apps.SearchConfig&#39;</span><span class="p">,</span> <span class="c1"># new</span>
<span class="s1">&#39;rest_framework&#39;</span><span class="p">,</span>
<span class="p">]</span>
</code></pre></div>

<p>Now we need to let Django know where Elasticsearch is running. We do that by adding the following to our <em>core/settings.py</em> file:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="c1"># Elasticsearch</span>
<span class="c1"># https://django-elasticsearch-dsl.readthedocs.io/en/latest/settings.html</span>

<span class="n">ELASTICSEARCH_DSL</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">&#39;default&#39;</span><span class="p">:</span> <span class="p">{</span>
<span class="s1">&#39;hosts&#39;</span><span class="p">:</span> <span class="s1">&#39;localhost:9200&#39;</span>
<span class="p">},</span>
<span class="p">}</span>
</code></pre></div>

<p>We can test if Django can connect to the Elasticsearch by starting our server:</p>
<div class="codehilite"><pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py runserver
</code></pre></div>

<p>If your Django server fails, Elasticsearch is probably not working correctly.</p>
<h2 id="creating-documents">Creating Documents</h2>
<p>Before creating the documents, we need to make sure all the data is going to get saved in the proper format. We're using <code>CharField(max_length=2)</code> for our article <code>type</code>, which by itself doesn't make much sense. This is why we'll transform it to human-readable text.</p>
<p>We'll achieve this by adding a <code>type_to_string()</code> method inside our model like so:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># blog/models.py</span>

<span class="k">class</span> <span class="nc">Article</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">title</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">256</span><span class="p">)</span>
<span class="n">author</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">ForeignKey</span><span class="p">(</span><span class="n">to</span><span class="o">=</span><span class="n">User</span><span class="p">,</span> <span class="n">on_delete</span><span class="o">=</span><span class="n">models</span><span class="o">.</span><span class="n">CASCADE</span><span class="p">)</span>
<span class="nb">type</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="n">ARTICLE_TYPES</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="s1">&#39;UN&#39;</span><span class="p">)</span>
<span class="n">categories</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">ManyToManyField</span><span class="p">(</span><span class="n">to</span><span class="o">=</span><span class="n">Category</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">related_name</span><span class="o">=</span><span class="s1">&#39;categories&#39;</span><span class="p">)</span>
<span class="n">content</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">TextField</span><span class="p">()</span>
<span class="n">created_datetime</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now_add</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="n">updated_datetime</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<span class="c1"># new</span>
<span class="k">def</span> <span class="nf">type_to_string</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">type</span> <span class="o">==</span> <span class="s1">&#39;UN&#39;</span><span class="p">:</span>
<span class="k">return</span> <span class="s1">&#39;Unspecified&#39;</span>
<span class="k">elif</span> <span class="bp">self</span><span class="o">.</span><span class="n">type</span> <span class="o">==</span> <span class="s1">&#39;TU&#39;</span><span class="p">:</span>
<span class="k">return</span> <span class="s1">&#39;Tutorial&#39;</span>
<span class="k">elif</span> <span class="bp">self</span><span class="o">.</span><span class="n">type</span> <span class="o">==</span> <span class="s1">&#39;RS&#39;</span><span class="p">:</span>
<span class="k">return</span> <span class="s1">&#39;Research&#39;</span>
<span class="k">elif</span> <span class="bp">self</span><span class="o">.</span><span class="n">type</span> <span class="o">==</span> <span class="s1">&#39;RW&#39;</span><span class="p">:</span>
<span class="k">return</span> <span class="s1">&#39;Review&#39;</span>

<span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">author</span><span class="si">}</span><span class="s1">: </span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">title</span><span class="si">}</span><span class="s1"> (</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">created_datetime</span><span class="o">.</span><span class="n">date</span><span class="p">()</span><span class="si">}</span><span class="s1">)&#39;</span>
</code></pre></div>

<p>Without <code>type_to_string()</code> our model would be serialized like this:</p>
<div class="codehilite"><pre><span></span><code><span class="p">{</span><span class="w"></span>
<span class="w">    </span><span class="nt">&quot;title&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;This is my article.&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="nt">&quot;type&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;TU&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="err">...</span><span class="w"></span>
<span class="p">}</span><span class="w"></span>
</code></pre></div>

<p>After implementing <code>type_to_string()</code> our model is serialized like this:</p>
<div class="codehilite"><pre><span></span><code><span class="p">{</span><span class="w"></span>
<span class="w">    </span><span class="nt">&quot;title&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;This is my article.&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="nt">&quot;type&quot;</span><span class="p">:</span><span class="w"> </span><span class="s2">&quot;Tutorial&quot;</span><span class="p">,</span><span class="w"></span>
<span class="w">    </span><span class="err">...</span><span class="w"></span>
<span class="p">}</span><span class="w"></span>
</code></pre></div>

<p>Now let's create the documents. Each document needs to have an <code>Index</code> and <code>Django</code> class. In the <code>Index</code> class, we need to provide the index name and <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-update-settings.html">Elasticsearch index settings</a>. In the <code>Django</code> class, we tell the document which Django model to associate it to and provide the fields we want to be indexed.</p>
<p><em>blog/documents.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># blog/documents.py</span>

<span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django_elasticsearch_dsl</span> <span class="kn">import</span> <span class="n">Document</span><span class="p">,</span> <span class="n">fields</span>
<span class="kn">from</span> <span class="nn">django_elasticsearch_dsl.registries</span> <span class="kn">import</span> <span class="n">registry</span>

<span class="kn">from</span> <span class="nn">blog.models</span> <span class="kn">import</span> <span class="n">Category</span><span class="p">,</span> <span class="n">Article</span>


<span class="nd">@registry</span><span class="o">.</span><span class="n">register_document</span>
<span class="k">class</span> <span class="nc">UserDocument</span><span class="p">(</span><span class="n">Document</span><span class="p">):</span>
<span class="k">class</span> <span class="nc">Index</span><span class="p">:</span>
<span class="n">name</span> <span class="o">=</span> <span class="s1">&#39;users&#39;</span>
<span class="n">settings</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">&#39;number_of_shards&#39;</span><span class="p">:</span> <span class="mi">1</span><span class="p">,</span>
<span class="s1">&#39;number_of_replicas&#39;</span><span class="p">:</span> <span class="mi">0</span><span class="p">,</span>
<span class="p">}</span>

<span class="k">class</span> <span class="nc">Django</span><span class="p">:</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">User</span>
<span class="n">fields</span> <span class="o">=</span> <span class="p">[</span>
<span class="s1">&#39;id&#39;</span><span class="p">,</span>
<span class="s1">&#39;first_name&#39;</span><span class="p">,</span>
<span class="s1">&#39;last_name&#39;</span><span class="p">,</span>
<span class="s1">&#39;username&#39;</span><span class="p">,</span>
<span class="p">]</span>


<span class="nd">@registry</span><span class="o">.</span><span class="n">register_document</span>
<span class="k">class</span> <span class="nc">CategoryDocument</span><span class="p">(</span><span class="n">Document</span><span class="p">):</span>
<span class="nb">id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">IntegerField</span><span class="p">()</span>

<span class="k">class</span> <span class="nc">Index</span><span class="p">:</span>
<span class="n">name</span> <span class="o">=</span> <span class="s1">&#39;categories&#39;</span>
<span class="n">settings</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">&#39;number_of_shards&#39;</span><span class="p">:</span> <span class="mi">1</span><span class="p">,</span>
<span class="s1">&#39;number_of_replicas&#39;</span><span class="p">:</span> <span class="mi">0</span><span class="p">,</span>
<span class="p">}</span>

<span class="k">class</span> <span class="nc">Django</span><span class="p">:</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Category</span>
<span class="n">fields</span> <span class="o">=</span> <span class="p">[</span>
<span class="s1">&#39;name&#39;</span><span class="p">,</span>
<span class="s1">&#39;description&#39;</span><span class="p">,</span>
<span class="p">]</span>


<span class="nd">@registry</span><span class="o">.</span><span class="n">register_document</span>
<span class="k">class</span> <span class="nc">ArticleDocument</span><span class="p">(</span><span class="n">Document</span><span class="p">):</span>
<span class="n">author</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">ObjectField</span><span class="p">(</span><span class="n">properties</span><span class="o">=</span><span class="p">{</span>
<span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">IntegerField</span><span class="p">(),</span>
<span class="s1">&#39;first_name&#39;</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">TextField</span><span class="p">(),</span>
<span class="s1">&#39;last_name&#39;</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">TextField</span><span class="p">(),</span>
<span class="s1">&#39;username&#39;</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">TextField</span><span class="p">(),</span>
<span class="p">})</span>
<span class="n">categories</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">ObjectField</span><span class="p">(</span><span class="n">properties</span><span class="o">=</span><span class="p">{</span>
<span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">IntegerField</span><span class="p">(),</span>
<span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">TextField</span><span class="p">(),</span>
<span class="s1">&#39;description&#39;</span><span class="p">:</span> <span class="n">fields</span><span class="o">.</span><span class="n">TextField</span><span class="p">(),</span>
<span class="p">})</span>
<span class="nb">type</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">TextField</span><span class="p">(</span><span class="n">attr</span><span class="o">=</span><span class="s1">&#39;type_to_string&#39;</span><span class="p">)</span>

<span class="k">class</span> <span class="nc">Index</span><span class="p">:</span>
<span class="n">name</span> <span class="o">=</span> <span class="s1">&#39;articles&#39;</span>
<span class="n">settings</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">&#39;number_of_shards&#39;</span><span class="p">:</span> <span class="mi">1</span><span class="p">,</span>
<span class="s1">&#39;number_of_replicas&#39;</span><span class="p">:</span> <span class="mi">0</span><span class="p">,</span>
<span class="p">}</span>

<span class="k">class</span> <span class="nc">Django</span><span class="p">:</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Article</span>
<span class="n">fields</span> <span class="o">=</span> <span class="p">[</span>
<span class="s1">&#39;title&#39;</span><span class="p">,</span>
<span class="s1">&#39;content&#39;</span><span class="p">,</span>
<span class="s1">&#39;created_datetime&#39;</span><span class="p">,</span>
<span class="s1">&#39;updated_datetime&#39;</span><span class="p">,</span>
<span class="p">]</span>
</code></pre></div>

<p>Notes:</p>
<ol>
<li>In order to transform the article type, we added the <code>type</code> attribute to the <code>ArticleDocument</code>.</li>
<li>Because our <code>Article</code> model is in a many-to-many (M:N) relationship with <code>Category</code> and a many-to-one (N:1) relationship with <code>User</code> we needed to take care of the relationships. We did that by adding <code>ObjectField</code> attributes.</li>
</ol>
<h3 id="populate-elasticsearch">Populate Elasticsearch</h3>
<p>To create and populate the Elasticsearch index and mapping, use the <code>search_index</code> command:</p>
<div class="codehilite"><pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py search_index --rebuild

Deleting index <span class="s1">&#39;users&#39;</span>
Deleting index <span class="s1">&#39;categories&#39;</span>
Deleting index <span class="s1">&#39;articles&#39;</span>
Creating index <span class="s1">&#39;users&#39;</span>
Creating index <span class="s1">&#39;categories&#39;</span>
Creating index <span class="s1">&#39;articles&#39;</span>
Indexing <span class="m">3</span> <span class="s1">&#39;User&#39;</span> objects
Indexing <span class="m">4</span> <span class="s1">&#39;Article&#39;</span> objects
Indexing <span class="m">4</span> <span class="s1">&#39;Category&#39;</span> objects
</code></pre></div>

<p>django-elasticsearch-dsl created the appropriate database signals so that your Elasticsearch storage gets updated every time an instance of a model is created, deleted, or edited.</p>
<h2 id="elasticsearch-queries">Elasticsearch Queries</h2>
<p>Before creating the appropriate views, let's look at how Elasticsearch queries work.</p>
<p>We first have to obtain the <code>Search</code> instance. We do that by calling <code>search()</code> on our Document like so:</p>
<div class="codehilite"><pre><span></span><code><span class="kn">from</span> <span class="nn">blog.documents</span> <span class="kn">import</span> <span class="n">ArticleDocument</span>

<span class="n">search</span> <span class="o">=</span> <span class="n">ArticleDocument</span><span class="o">.</span><span class="n">search</span><span class="p">()</span>
</code></pre></div>

<p>Once we have the <code>Search</code> instance we can pass queries to the <code>query()</code> method and fetch the response:</p>
<div class="codehilite"><pre><span></span><code><span class="kn">from</span> <span class="nn">elasticsearch_dsl</span> <span class="kn">import</span> <span class="n">Q</span>
<span class="kn">from</span> <span class="nn">blog.documents</span> <span class="kn">import</span> <span class="n">ArticleDocument</span>


<span class="c1"># Looks up all the articles that contain `How to` in the title.</span>
<span class="n">query</span> <span class="o">=</span> <span class="s1">&#39;How to&#39;</span>
<span class="n">q</span> <span class="o">=</span> <span class="n">Q</span><span class="p">(</span>
<span class="s1">&#39;multi_match&#39;</span><span class="p">,</span>
<span class="n">query</span><span class="o">=</span><span class="n">query</span><span class="p">,</span>
<span class="n">fields</span><span class="o">=</span><span class="p">[</span>
<span class="s1">&#39;title&#39;</span>
<span class="p">])</span>
<span class="n">search</span> <span class="o">=</span> <span class="n">ArticleDocument</span><span class="o">.</span><span class="n">search</span><span class="p">()</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="n">q</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">search</span><span class="o">.</span><span class="n">execute</span><span class="p">()</span>

<span class="c1"># print all the hits</span>
<span class="k">for</span> <span class="n">hit</span> <span class="ow">in</span> <span class="n">search</span><span class="p">:</span>
<span class="nb">print</span><span class="p">(</span><span class="n">hit</span><span class="o">.</span><span class="n">title</span><span class="p">)</span>
</code></pre></div>

<p>We can also combine multiple Q statements like so:</p>
<div class="codehilite"><pre><span></span><code><span class="kn">from</span> <span class="nn">elasticsearch_dsl</span> <span class="kn">import</span> <span class="n">Q</span>
<span class="kn">from</span> <span class="nn">blog.documents</span> <span class="kn">import</span> <span class="n">ArticleDocument</span>

<span class="sd">&quot;&quot;&quot;</span>
<span class="sd">Looks up all the articles that:</span>
<span class="sd">1) Contain &#39;language&#39; in the &#39;title&#39;</span>
<span class="sd">2) Don&#39;t contain &#39;ruby&#39; or &#39;javascript&#39; in the &#39;title&#39;</span>
<span class="sd">3) And contain the query either in the &#39;title&#39; or &#39;description&#39;</span>
<span class="sd">&quot;&quot;&quot;</span>
<span class="n">query</span> <span class="o">=</span> <span class="s1">&#39;programming&#39;</span>
<span class="n">q</span> <span class="o">=</span> <span class="n">Q</span><span class="p">(</span>
<span class="s1">&#39;bool&#39;</span><span class="p">,</span>
<span class="n">must</span><span class="o">=</span><span class="p">[</span>
<span class="n">Q</span><span class="p">(</span><span class="s1">&#39;match&#39;</span><span class="p">,</span> <span class="n">title</span><span class="o">=</span><span class="s1">&#39;language&#39;</span><span class="p">),</span>
<span class="p">],</span>
<span class="n">must_not</span><span class="o">=</span><span class="p">[</span>
<span class="n">Q</span><span class="p">(</span><span class="s1">&#39;match&#39;</span><span class="p">,</span> <span class="n">title</span><span class="o">=</span><span class="s1">&#39;ruby&#39;</span><span class="p">),</span>
<span class="n">Q</span><span class="p">(</span><span class="s1">&#39;match&#39;</span><span class="p">,</span> <span class="n">title</span><span class="o">=</span><span class="s1">&#39;javascript&#39;</span><span class="p">),</span>
<span class="p">],</span>
<span class="n">should</span><span class="o">=</span><span class="p">[</span>
<span class="n">Q</span><span class="p">(</span><span class="s1">&#39;match&#39;</span><span class="p">,</span> <span class="n">title</span><span class="o">=</span><span class="n">query</span><span class="p">),</span>
<span class="n">Q</span><span class="p">(</span><span class="s1">&#39;match&#39;</span><span class="p">,</span> <span class="n">description</span><span class="o">=</span><span class="n">query</span><span class="p">),</span>
<span class="p">],</span>
<span class="n">minimum_should_match</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
<span class="n">search</span> <span class="o">=</span> <span class="n">ArticleDocument</span><span class="o">.</span><span class="n">search</span><span class="p">()</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="n">q</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">search</span><span class="o">.</span><span class="n">execute</span><span class="p">()</span>

<span class="c1"># print all the hits</span>
<span class="k">for</span> <span class="n">hit</span> <span class="ow">in</span> <span class="n">search</span><span class="p">:</span>
<span class="nb">print</span><span class="p">(</span><span class="n">hit</span><span class="o">.</span><span class="n">title</span><span class="p">)</span>
</code></pre></div>

<p>Another important thing when working with Elasticsearch queries is fuzziness. Fuzzy queries are queries that allow us to handle typos. They use the <a href="https://en.wikipedia.org/wiki/Levenshtein_distance">Levenshtein Distance Algorithm</a> which calculates the distance between the result in our database and the query.</p>
<p>Let's look at an example.</p>
<p>By running the following query we won't get any results, because the user misspelled 'django'.</p>
<div class="codehilite"><pre><span></span><code><span class="kn">from</span> <span class="nn">elasticsearch_dsl</span> <span class="kn">import</span> <span class="n">Q</span>
<span class="kn">from</span> <span class="nn">blog.documents</span> <span class="kn">import</span> <span class="n">ArticleDocument</span>

<span class="n">query</span> <span class="o">=</span> <span class="s1">&#39;djengo&#39;</span>  <span class="c1"># notice the typo</span>
<span class="n">q</span> <span class="o">=</span> <span class="n">Q</span><span class="p">(</span>
<span class="s1">&#39;multi_match&#39;</span><span class="p">,</span>
<span class="n">query</span><span class="o">=</span><span class="n">query</span><span class="p">,</span>
<span class="n">fields</span><span class="o">=</span><span class="p">[</span>
<span class="s1">&#39;title&#39;</span>
<span class="p">])</span>
<span class="n">search</span> <span class="o">=</span> <span class="n">ArticleDocument</span><span class="o">.</span><span class="n">search</span><span class="p">()</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="n">q</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">search</span><span class="o">.</span><span class="n">execute</span><span class="p">()</span>

<span class="c1"># print all the hits</span>
<span class="k">for</span> <span class="n">hit</span> <span class="ow">in</span> <span class="n">search</span><span class="p">:</span>
<span class="nb">print</span><span class="p">(</span><span class="n">hit</span><span class="o">.</span><span class="n">title</span><span class="p">)</span>
</code></pre></div>

<p>If we enable fuzziness like so:</p>
<div class="codehilite"><pre><span></span><code><span class="kn">from</span> <span class="nn">elasticsearch_dsl</span> <span class="kn">import</span> <span class="n">Q</span>
<span class="kn">from</span> <span class="nn">blog.documents</span> <span class="kn">import</span> <span class="n">ArticleDocument</span>

<span class="n">query</span> <span class="o">=</span> <span class="s1">&#39;djengo&#39;</span>  <span class="c1"># notice the typo</span>
<span class="n">q</span> <span class="o">=</span> <span class="n">Q</span><span class="p">(</span>
<span class="s1">&#39;multi_match&#39;</span><span class="p">,</span>
<span class="n">query</span><span class="o">=</span><span class="n">query</span><span class="p">,</span>
<span class="n">fields</span><span class="o">=</span><span class="p">[</span>
<span class="s1">&#39;title&#39;</span>
<span class="p">],</span>
<span class="n">fuzziness</span><span class="o">=</span><span class="s1">&#39;auto&#39;</span><span class="p">)</span>
<span class="n">search</span> <span class="o">=</span> <span class="n">ArticleDocument</span><span class="o">.</span><span class="n">search</span><span class="p">()</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="n">q</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">search</span><span class="o">.</span><span class="n">execute</span><span class="p">()</span>

<span class="c1"># print all the hits</span>
<span class="k">for</span> <span class="n">hit</span> <span class="ow">in</span> <span class="n">search</span><span class="p">:</span>
<span class="nb">print</span><span class="p">(</span><span class="n">hit</span><span class="o">.</span><span class="n">title</span><span class="p">)</span>
</code></pre></div>

<p>The user will get the correct result.</p>
<p>Elasticsearch has a number of additional features. To get familiar with the API, try implementing:</p>
<ol>
<li>Your own <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html">analyzer</a>.</li>
<li><a href="https://www.elastic.co/guide/en/elasticsearch/reference/6.8/search-suggesters-completion.html">Completion suggester</a> - when a user queries 'j' your app should suggest 'johhny' or 'jess_'.</li>
<li><a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/highlighting.html">Highlighting</a> - when user makes a typo, highlight it (e.g., Linuks -&gt; <em>Linux</em>).</li>
</ol>
<p>You can see all the <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html">Elasticsearch Search APIs</a> here.</p>
<h2 id="search-views">Search Views</h2>
<p>With that, let's create sime views. To make our code more DRY we can use the following abstract class in <em>search/views.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># search/views.py</span>

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
<span class="sd">&quot;&quot;&quot;This method should be overridden</span>
<span class="sd">        and return a Q() expression.&quot;&quot;&quot;</span>

<span class="k">def</span> <span class="nf">get</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">request</span><span class="p">,</span> <span class="n">query</span><span class="p">):</span>
<span class="k">try</span><span class="p">:</span>
<span class="n">q</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">generate_q_expression</span><span class="p">(</span><span class="n">query</span><span class="p">)</span>
<span class="n">search</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">document_class</span><span class="o">.</span><span class="n">search</span><span class="p">()</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="n">q</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">search</span><span class="o">.</span><span class="n">execute</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;Found </span><span class="si">{</span><span class="n">response</span><span class="o">.</span><span class="n">hits</span><span class="o">.</span><span class="n">total</span><span class="o">.</span><span class="n">value</span><span class="si">}</span><span class="s1"> hit(s) for query: &quot;</span><span class="si">{</span><span class="n">query</span><span class="si">}</span><span class="s1">&quot;&#39;</span><span class="p">)</span>

<span class="n">results</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">paginate_queryset</span><span class="p">(</span><span class="n">response</span><span class="p">,</span> <span class="n">request</span><span class="p">,</span> <span class="n">view</span><span class="o">=</span><span class="bp">self</span><span class="p">)</span>
<span class="n">serializer</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">serializer_class</span><span class="p">(</span><span class="n">results</span><span class="p">,</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">get_paginated_response</span><span class="p">(</span><span class="n">serializer</span><span class="o">.</span><span class="n">data</span><span class="p">)</span>
<span class="k">except</span> <span class="ne">Exception</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span>
<span class="k">return</span> <span class="n">HttpResponse</span><span class="p">(</span><span class="n">e</span><span class="p">,</span> <span class="n">status</span><span class="o">=</span><span class="mi">500</span><span class="p">)</span>
</code></pre></div>

<p>Notes:</p>
<ol>
<li>To use the class, we have to provide our <code>serializer_class</code> and <code>document_class</code> and override <code>generate_q_expression()</code>.</li>
<li>The class does nothing else than run the <code>generate_q_expression()</code> query, fetch the response, paginate it, and return serialized data.</li>
</ol>
<p>All the views should now inherit from <code>PaginatedElasticSearchAPIView</code>:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># search/views.py</span>

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
<span class="sd">&quot;&quot;&quot;This method should be overridden</span>
<span class="sd">        and return a Q() expression.&quot;&quot;&quot;</span>

<span class="k">def</span> <span class="nf">get</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">request</span><span class="p">,</span> <span class="n">query</span><span class="p">):</span>
<span class="k">try</span><span class="p">:</span>
<span class="n">q</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">generate_q_expression</span><span class="p">(</span><span class="n">query</span><span class="p">)</span>
<span class="n">search</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">document_class</span><span class="o">.</span><span class="n">search</span><span class="p">()</span><span class="o">.</span><span class="n">query</span><span class="p">(</span><span class="n">q</span><span class="p">)</span>
<span class="n">response</span> <span class="o">=</span> <span class="n">search</span><span class="o">.</span><span class="n">execute</span><span class="p">()</span>

<span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;Found </span><span class="si">{</span><span class="n">response</span><span class="o">.</span><span class="n">hits</span><span class="o">.</span><span class="n">total</span><span class="o">.</span><span class="n">value</span><span class="si">}</span><span class="s1"> hit(s) for query: &quot;</span><span class="si">{</span><span class="n">query</span><span class="si">}</span><span class="s1">&quot;&#39;</span><span class="p">)</span>

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
<span class="k">return</span> <span class="n">Q</span><span class="p">(</span><span class="s1">&#39;bool&#39;</span><span class="p">,</span>
<span class="n">should</span><span class="o">=</span><span class="p">[</span>
<span class="n">Q</span><span class="p">(</span><span class="s1">&#39;match&#39;</span><span class="p">,</span> <span class="n">username</span><span class="o">=</span><span class="n">query</span><span class="p">),</span>
<span class="n">Q</span><span class="p">(</span><span class="s1">&#39;match&#39;</span><span class="p">,</span> <span class="n">first_name</span><span class="o">=</span><span class="n">query</span><span class="p">),</span>
<span class="n">Q</span><span class="p">(</span><span class="s1">&#39;match&#39;</span><span class="p">,</span> <span class="n">last_name</span><span class="o">=</span><span class="n">query</span><span class="p">),</span>
<span class="p">],</span> <span class="n">minimum_should_match</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>


<span class="k">class</span> <span class="nc">SearchCategories</span><span class="p">(</span><span class="n">PaginatedElasticSearchAPIView</span><span class="p">):</span>
<span class="n">serializer_class</span> <span class="o">=</span> <span class="n">CategorySerializer</span>
<span class="n">document_class</span> <span class="o">=</span> <span class="n">CategoryDocument</span>

<span class="k">def</span> <span class="nf">generate_q_expression</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">query</span><span class="p">):</span>
<span class="k">return</span> <span class="n">Q</span><span class="p">(</span>
<span class="s1">&#39;multi_match&#39;</span><span class="p">,</span> <span class="n">query</span><span class="o">=</span><span class="n">query</span><span class="p">,</span>
<span class="n">fields</span><span class="o">=</span><span class="p">[</span>
<span class="s1">&#39;name&#39;</span><span class="p">,</span>
<span class="s1">&#39;description&#39;</span><span class="p">,</span>
<span class="p">],</span> <span class="n">fuzziness</span><span class="o">=</span><span class="s1">&#39;auto&#39;</span><span class="p">)</span>


<span class="k">class</span> <span class="nc">SearchArticles</span><span class="p">(</span><span class="n">PaginatedElasticSearchAPIView</span><span class="p">):</span>
<span class="n">serializer_class</span> <span class="o">=</span> <span class="n">ArticleSerializer</span>
<span class="n">document_class</span> <span class="o">=</span> <span class="n">ArticleDocument</span>

<span class="k">def</span> <span class="nf">generate_q_expression</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">query</span><span class="p">):</span>
<span class="k">return</span> <span class="n">Q</span><span class="p">(</span>
<span class="s1">&#39;multi_match&#39;</span><span class="p">,</span> <span class="n">query</span><span class="o">=</span><span class="n">query</span><span class="p">,</span>
<span class="n">fields</span><span class="o">=</span><span class="p">[</span>
<span class="s1">&#39;title&#39;</span><span class="p">,</span>
<span class="s1">&#39;author&#39;</span><span class="p">,</span>
<span class="s1">&#39;type&#39;</span><span class="p">,</span>
<span class="s1">&#39;content&#39;</span>
<span class="p">],</span> <span class="n">fuzziness</span><span class="o">=</span><span class="s1">&#39;auto&#39;</span><span class="p">)</span>
</code></pre></div>

<h3 id="define-urls_1">Define URLs</h3>
<p>Lastly, let's create the URLs for our views:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># search.urls.py</span>

<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span>

<span class="kn">from</span> <span class="nn">search.views</span> <span class="kn">import</span> <span class="n">SearchArticles</span><span class="p">,</span> <span class="n">SearchCategories</span><span class="p">,</span> <span class="n">SearchUsers</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">path</span><span class="p">(</span><span class="s1">&#39;user/&lt;str:query&gt;/&#39;</span><span class="p">,</span> <span class="n">SearchUsers</span><span class="o">.</span><span class="n">as_view</span><span class="p">()),</span>
<span class="n">path</span><span class="p">(</span><span class="s1">&#39;category/&lt;str:query&gt;/&#39;</span><span class="p">,</span> <span class="n">SearchCategories</span><span class="o">.</span><span class="n">as_view</span><span class="p">()),</span>
<span class="n">path</span><span class="p">(</span><span class="s1">&#39;article/&lt;str:query&gt;/&#39;</span><span class="p">,</span> <span class="n">SearchArticles</span><span class="o">.</span><span class="n">as_view</span><span class="p">()),</span>
<span class="p">]</span>
</code></pre></div>

<p>Then, wire up the app URLs to the project URLs:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># core/urls.py</span>

<span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>
<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span><span class="p">,</span> <span class="n">include</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">path</span><span class="p">(</span><span class="s1">&#39;blog/&#39;</span><span class="p">,</span> <span class="n">include</span><span class="p">(</span><span class="s1">&#39;blog.urls&#39;</span><span class="p">)),</span>
<span class="n">path</span><span class="p">(</span><span class="s1">&#39;search/&#39;</span><span class="p">,</span> <span class="n">include</span><span class="p">(</span><span class="s1">&#39;search.urls&#39;</span><span class="p">)),</span> <span class="c1"># new</span>
<span class="n">path</span><span class="p">(</span><span class="s1">&#39;admin/&#39;</span><span class="p">,</span> <span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">urls</span><span class="p">),</span>
<span class="p">]</span>
</code></pre></div>

<h3 id="testing_1">Testing</h3>
<p>Our web application is done. We can test our search endpoints by visiting the following URLs:</p>
<table>
<thead>
<tr>
<th>URL</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="http://127.0.0.1:8000/search/user/mike/">http://127.0.0.1:8000/search/user/mike/</a></td>
<td>Returns user 'mike13'</td>
</tr>
<tr>
<td><a href="http://127.0.0.1:8000/search/user/jess_/">http://127.0.0.1:8000/search/user/jess_/</a></td>
<td>Returns user 'jess_'</td>
</tr>
<tr>
<td><a href="http://127.0.0.1:8000/search/category/seo/">http://127.0.0.1:8000/search/category/seo/</a></td>
<td>Returns category 'SEO optimization'</td>
</tr>
<tr>
<td><a href="http://127.0.0.1:8000/search/category/progreming/">http://127.0.0.1:8000/search/category/progreming/</a></td>
<td>Returns category 'Programming'</td>
</tr>
<tr>
<td><a href="http://127.0.0.1:8000/search/article/linux/">http://127.0.0.1:8000/search/article/linux/</a></td>
<td>Returns article 'Installing the latest version of Ubuntu'</td>
</tr>
<tr>
<td><a href="http://127.0.0.1:8000/search/article/java/">http://127.0.0.1:8000/search/article/java/</a></td>
<td>Returns article 'Which programming language is the best?'</td>
</tr>
</tbody>
</table>


</div> <!-- content -->
<div class="rtow">
</div>
</div> <!-- container -->
</body>
</html>