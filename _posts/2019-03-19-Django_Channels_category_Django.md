---
layout: post
title: Django Channels
date: 2019-03-19 16:20:23 +0900
category: Django
tag: Django
---


<h2 id="what-is-django-channels">Django Channels</h2>
<p>Check code <a href="https://github.com/ShihabYasin/simple-django-channels">here.</a> </p>
<p><a href="https://channels.readthedocs.io/en/stable/">Django Channels</a> (or just Channels) extends the built-in capabilities of <a href="https://www.djangoproject.com/">Django</a> allowing Django projects to handle not only HTTP but also protocols that require long-running connections, such as WebSockets, MQTT (IoT), chatbots, radios, and other real-time applications. On top of this, it provides support for a number of Django's core features like authentication and sessions.</p>

<p>To learn more about Channels, check out the <a href="https://channels.readthedocs.io/en/stable/introduction.html">Introduction</a> guide from the <a href="https://channels.readthedocs.io/">official documentation</a>.</p>
<h2 id="sync-vs-async">Sync vs Async</h2>
<p>Because of the differences between Channels and Django, we'll have to frequently switch between sync and async code execution. For example, the Django database needs to be accessed using synchronous code while the Channels channel layer needs to be accessed using asynchronous code.</p>
<p>The easiest way to switch between the two is by using the built-in Django <a href="https://github.com/django/asgiref">asgiref</a> (<code>asgrief.sync</code>) functions:</p>
<ol>
<li><code>sync_to_async</code> - takes a sync function and returns an async function that wraps it</li>
<li><code>async_to_sync</code> - takes an async function and returns a sync function</li>
</ol>
<li><code>sync_to_async</code> - takes a sync function and returns an async function that wraps it</li>
<li><code>async_to_sync</code> - takes an async function and returns a sync function</li>
<p>Don't worry about this just yet, we'll show a practical example later in the tutorial.</p>
<h2 id="project-setup">Project Setup</h2>
<p>Again, we'll be building a chat application. The app will have multiple rooms where Django authenticated users can chat. Each room will have a list of currently connected users. We'll also implement private, one-to-one messaging.</p>
<h3 id="django-project-setup">Django Project Setup</h3>
<p>Start by creating a new directory and setting up a new Django project:</p>
<pre><span></span><code>$ mkdir django-channels-example <span class="o">&amp;&amp;</span> <span class="nb">cd</span> django-channels-example
$ python3.9 -m venv env
$ <span class="nb">source</span> env/bin/activate

<span class="o">(</span>env<span class="o">)</span>$ pip install <span class="nv">django</span><span class="o">==</span><span class="m">4</span>.0
<span class="o">(</span>env<span class="o">)</span>$ django-admin startproject core .
</code></pre>
<p>After that, create a new Django app called <code>chat</code>:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py startapp chat
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
<span class="s1">'chat.apps.ChatConfig'</span><span class="p">,</span>  <span class="c1"># new</span>
<span class="p">]</span>
</code></pre>
<h3 id="create-database-models">Create Database Models</h3>
<p>Next, let's create two Django models, <code>Room</code> and <code>Message</code>, in <em>chat/models.py</em>:</p>
<pre><span></span><code><span class="c1"># chat/models.py</span>

<span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>


<span class="k">class</span> <span class="nc">Room</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">name</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">128</span><span class="p">)</span>
<span class="n">online</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">ManyToManyField</span><span class="p">(</span><span class="n">to</span><span class="o">=</span><span class="n">User</span><span class="p">,</span> <span class="n">blank</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<span class="k">def</span> <span class="nf">get_online_count</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">online</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>

<span class="k">def</span> <span class="nf">join</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">user</span><span class="p">):</span>
<span class="bp">self</span><span class="o">.</span><span class="n">online</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">user</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">save</span><span class="p">()</span>

<span class="k">def</span> <span class="nf">leave</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">user</span><span class="p">):</span>
<span class="bp">self</span><span class="o">.</span><span class="n">online</span><span class="o">.</span><span class="n">remove</span><span class="p">(</span><span class="n">user</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">save</span><span class="p">()</span>

<span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="sa">f</span><span class="s1">'</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">name</span><span class="si">}</span><span class="s1"> (</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">get_online_count</span><span class="p">()</span><span class="si">}</span><span class="s1">)'</span>


<span class="k">class</span> <span class="nc">Message</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">user</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">ForeignKey</span><span class="p">(</span><span class="n">to</span><span class="o">=</span><span class="n">User</span><span class="p">,</span> <span class="n">on_delete</span><span class="o">=</span><span class="n">models</span><span class="o">.</span><span class="n">CASCADE</span><span class="p">)</span>
<span class="n">room</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">ForeignKey</span><span class="p">(</span><span class="n">to</span><span class="o">=</span><span class="n">Room</span><span class="p">,</span> <span class="n">on_delete</span><span class="o">=</span><span class="n">models</span><span class="o">.</span><span class="n">CASCADE</span><span class="p">)</span>
<span class="n">content</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">512</span><span class="p">)</span>
<span class="n">timestamp</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now_add</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="sa">f</span><span class="s1">'</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">username</span><span class="si">}</span><span class="s1">: </span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">content</span><span class="si">}</span><span class="s1"> [</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">timestamp</span><span class="si">}</span><span class="s1">]'</span>
</code></pre>
<p>Notes:</p>
<ol>
<li><code>Room</code> represents a chat room. It contains an <code>online</code> field for tracking when users connect and disconnect from the chat room.</li>
<li><code>Message</code> represents a message sent to the chat room. We'll use this model to store all the messages sent in the chat.</li>
</ol>
<li><code>Room</code> represents a chat room. It contains an <code>online</code> field for tracking when users connect and disconnect from the chat room.</li>
<li><code>Message</code> represents a message sent to the chat room. We'll use this model to store all the messages sent in the chat.</li>
<p>Run the <code>makemigrations</code> and <code>migrate</code> commands to sync the database:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py makemigrations
<span class="o">(</span>env<span class="o">)</span>$ python manage.py migrate
</code></pre>
<p>Register the models in <em>chat/admin.py</em> so they're accessible from the Django admin panel:</p>
<pre><span></span><code><span class="c1"># chat/admin.py</span>

<span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>

<span class="kn">from</span> <span class="nn">chat.models</span> <span class="kn">import</span> <span class="n">Room</span><span class="p">,</span> <span class="n">Message</span>

<span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="n">Room</span><span class="p">)</span>
<span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="n">Message</span><span class="p">)</span>
</code></pre>
<h3 id="views-and-urls">Views and URLs</h3>
<p>The web application will have the following two URLs:</p>
<ol>
<li><code>/chat/</code> - chat room selector</li>
<li><code>/chat/&lt;ROOM_NAME&gt;/</code> - chat room</li>
</ol>
<li><code>/chat/</code> - chat room selector</li>
<li><code>/chat/&lt;ROOM_NAME&gt;/</code> - chat room</li>
<p>Add the following views to <em>chat/views.py</em>:</p>
<pre><span></span><code><span class="c1"># chat/views.py</span>

<span class="kn">from</span> <span class="nn">django.shortcuts</span> <span class="kn">import</span> <span class="n">render</span>

<span class="kn">from</span> <span class="nn">chat.models</span> <span class="kn">import</span> <span class="n">Room</span>


<span class="k">def</span> <span class="nf">index_view</span><span class="p">(</span><span class="n">request</span><span class="p">):</span>
<span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="s1">'index.html'</span><span class="p">,</span> <span class="p">{</span>
<span class="s1">'rooms'</span><span class="p">:</span> <span class="n">Room</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">(),</span>
<span class="p">})</span>


<span class="k">def</span> <span class="nf">room_view</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="n">room_name</span><span class="p">):</span>
<span class="n">chat_room</span><span class="p">,</span> <span class="n">created</span> <span class="o">=</span> <span class="n">Room</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">get_or_create</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="n">room_name</span><span class="p">)</span>
<span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="s1">'room.html'</span><span class="p">,</span> <span class="p">{</span>
<span class="s1">'room'</span><span class="p">:</span> <span class="n">chat_room</span><span class="p">,</span>
<span class="p">})</span>
</code></pre>
<p>Create a <em>urls.py</em> file within the <code>chat</code> app:</p>
<pre><span></span><code><span class="c1"># chat/urls.py</span>

<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span>

<span class="kn">from</span> <span class="nn">.</span> <span class="kn">import</span> <span class="n">views</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">path</span><span class="p">(</span><span class="s1">''</span><span class="p">,</span> <span class="n">views</span><span class="o">.</span><span class="n">index_view</span><span class="p">,</span> <span class="n">name</span><span class="o">=</span><span class="s1">'chat-index'</span><span class="p">),</span>
<span class="n">path</span><span class="p">(</span><span class="s1">'&lt;str:room_name&gt;/'</span><span class="p">,</span> <span class="n">views</span><span class="o">.</span><span class="n">room_view</span><span class="p">,</span> <span class="n">name</span><span class="o">=</span><span class="s1">'chat-room'</span><span class="p">),</span>
<span class="p">]</span>
</code></pre>
<p>Update the project-level <em>urls.py</em> file with the <code>chat</code> app as well:</p>
<pre><span></span><code><span class="c1"># core/urls.py</span>

<span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>
<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span><span class="p">,</span> <span class="n">include</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">path</span><span class="p">(</span><span class="s1">'chat/'</span><span class="p">,</span> <span class="n">include</span><span class="p">(</span><span class="s1">'chat.urls'</span><span class="p">)),</span>  <span class="c1"># new</span>
<span class="n">path</span><span class="p">(</span><span class="s1">'admin/'</span><span class="p">,</span> <span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">urls</span><span class="p">),</span>
<span class="p">]</span>
</code></pre>
<h3 id="templates-and-static-files">Templates and Static Files</h3>
<p>Create an <em>index.html</em> file inside a new folder called "templates" in "chat":</p>
<pre><span></span><code><span class="cm">&lt;!-- chat/templates/index.html --&gt;</span>

{% load static %}

<span class="cp">&lt;!DOCTYPE html&gt;</span>
<span class="p">&lt;</span><span class="nt">html</span> <span class="na">lang</span><span class="o">=</span><span class="s">"en"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">head</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">title</span><span class="p">&gt;</span>django-channels-chat<span class="p">&lt;/</span><span class="nt">title</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">link</span> <span class="na">rel</span><span class="o">=</span><span class="s">"stylesheet"</span> <span class="na">href</span><span class="o">=</span><span class="s">"https://cdn.jsdelivr.net/npm/<a class="__cf_email__" data-cfemail="03616c6c77707771627343362d322d30" href="/cdn-cgi/l/email-protection">[email protected]</a>/dist/css/bootstrap.min.css"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">"https://cdn.jsdelivr.net/npm/<a class="__cf_email__" data-cfemail="5b3934342f282f293a2b1b6e756a7568" href="/cdn-cgi/l/email-protection">[email protected]</a>/dist/js/bootstrap.min.js"</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">style</span><span class="p">&gt;</span><span class="w"></span>
<span class="w">            </span><span class="p">#</span><span class="nn">roomSelect</span><span class="w"> </span><span class="p">{</span><span class="w"></span>
<span class="w">                </span><span class="k">height</span><span class="p">:</span><span class="w"> </span><span class="mi">300</span><span class="kt">px</span><span class="p">;</span><span class="w"></span>
<span class="w">            </span><span class="p">}</span><span class="w"></span>
<span class="w">        </span><span class="p">&lt;/</span><span class="nt">style</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">head</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">body</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"container mt-3 p-5"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">h2</span><span class="p">&gt;</span>django-channels-chat<span class="p">&lt;/</span><span class="nt">h2</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"row"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"col-12 col-md-8"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"mb-2"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">label</span> <span class="na">for</span><span class="o">=</span><span class="s">"roomInput"</span><span class="p">&gt;</span>Enter a room name to connect to it:<span class="p">&lt;/</span><span class="nt">label</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">input</span> <span class="na">type</span><span class="o">=</span><span class="s">"text"</span> <span class="na">class</span><span class="o">=</span><span class="s">"form-control"</span> <span class="na">id</span><span class="o">=</span><span class="s">"roomInput"</span> <span class="na">placeholder</span><span class="o">=</span><span class="s">"Room name"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">small</span> <span class="na">id</span><span class="o">=</span><span class="s">"roomInputHelp"</span> <span class="na">class</span><span class="o">=</span><span class="s">"form-text text-muted"</span><span class="p">&gt;</span>If the room doesn't exist yet, it will be created for you.<span class="p">&lt;/</span><span class="nt">small</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">button</span> <span class="na">type</span><span class="o">=</span><span class="s">"button"</span> <span class="na">id</span><span class="o">=</span><span class="s">"roomConnect"</span> <span class="na">class</span><span class="o">=</span><span class="s">"btn btn-success"</span><span class="p">&gt;</span>Connect<span class="p">&lt;/</span><span class="nt">button</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"col-12 col-md-4"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">label</span> <span class="na">for</span><span class="o">=</span><span class="s">"roomSelect"</span><span class="p">&gt;</span>Active rooms<span class="p">&lt;/</span><span class="nt">label</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">select</span> <span class="na">multiple</span> <span class="na">class</span><span class="o">=</span><span class="s">"form-control"</span> <span class="na">id</span><span class="o">=</span><span class="s">"roomSelect"</span><span class="p">&gt;</span>
{% for room in rooms %}
<span class="p">&lt;</span><span class="nt">option</span><span class="p">&gt;</span>{{ room }}<span class="p">&lt;/</span><span class="nt">option</span><span class="p">&gt;</span>
{% endfor %}
<span class="p">&lt;/</span><span class="nt">select</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">"{% static 'index.js' %}"</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">body</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">html</span><span class="p">&gt;</span>
</code></pre>
<p>Next, add <em>room.html</em> inside the same folder:</p>
<pre><span></span><code><span class="cm">&lt;!-- chat/templates/room.html --&gt;</span>

{% load static %}

<span class="cp">&lt;!DOCTYPE html&gt;</span>
<span class="p">&lt;</span><span class="nt">html</span> <span class="na">lang</span><span class="o">=</span><span class="s">"en"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">head</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">title</span><span class="p">&gt;</span>django-channels-chat<span class="p">&lt;/</span><span class="nt">title</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">link</span> <span class="na">rel</span><span class="o">=</span><span class="s">"stylesheet"</span> <span class="na">href</span><span class="o">=</span><span class="s">"https://cdn.jsdelivr.net/npm/<a class="__cf_email__" data-cfemail="f6949999828582849786b6c3d8c7d8c5" href="/cdn-cgi/l/email-protection">[email protected]</a>/dist/css/bootstrap.min.css"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">"https://cdn.jsdelivr.net/npm/<a class="__cf_email__" data-cfemail="eb8984849f989f998a9babdec5dac5d8" href="/cdn-cgi/l/email-protection">[email protected]</a>/dist/js/bootstrap.min.js"</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">style</span><span class="p">&gt;</span><span class="w"></span>
<span class="w">            </span><span class="p">#</span><span class="nn">chatLog</span><span class="w"> </span><span class="p">{</span><span class="w"></span>
<span class="w">                </span><span class="k">height</span><span class="p">:</span><span class="w"> </span><span class="mi">300</span><span class="kt">px</span><span class="p">;</span><span class="w"></span>
<span class="w">                </span><span class="k">background-color</span><span class="p">:</span><span class="w"> </span><span class="mh">#FFFFFF</span><span class="p">;</span><span class="w"></span>
<span class="w">                </span><span class="k">resize</span><span class="p">:</span><span class="w"> </span><span class="kc">none</span><span class="p">;</span><span class="w"></span>
<span class="w">            </span><span class="p">}</span><span class="w"></span>

<span class="w">            </span><span class="p">#</span><span class="nn">onlineUsersSelector</span><span class="w"> </span><span class="p">{</span><span class="w"></span>
<span class="w">                </span><span class="k">height</span><span class="p">:</span><span class="w"> </span><span class="mi">300</span><span class="kt">px</span><span class="p">;</span><span class="w"></span>
<span class="w">            </span><span class="p">}</span><span class="w"></span>
<span class="w">        </span><span class="p">&lt;/</span><span class="nt">style</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">head</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">body</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"container mt-3 p-5"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">h2</span><span class="p">&gt;</span>django-channels-chat<span class="p">&lt;/</span><span class="nt">h2</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"row"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"col-12 col-md-8"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"mb-2"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">label</span> <span class="na">for</span><span class="o">=</span><span class="s">"chatLog"</span><span class="p">&gt;</span>Room: #{{ room.name }}<span class="p">&lt;/</span><span class="nt">label</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">textarea</span> <span class="na">class</span><span class="o">=</span><span class="s">"form-control"</span> <span class="na">id</span><span class="o">=</span><span class="s">"chatLog"</span> <span class="na">readonly</span><span class="p">&gt;&lt;/</span><span class="nt">textarea</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"input-group"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">input</span> <span class="na">type</span><span class="o">=</span><span class="s">"text"</span> <span class="na">class</span><span class="o">=</span><span class="s">"form-control"</span> <span class="na">id</span><span class="o">=</span><span class="s">"chatMessageInput"</span> <span class="na">placeholder</span><span class="o">=</span><span class="s">"Enter your chat message"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"input-group-append"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">button</span> <span class="na">class</span><span class="o">=</span><span class="s">"btn btn-success"</span> <span class="na">id</span><span class="o">=</span><span class="s">"chatMessageSend"</span> <span class="na">type</span><span class="o">=</span><span class="s">"button"</span><span class="p">&gt;</span>Send<span class="p">&lt;/</span><span class="nt">button</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"col-12 col-md-4"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">label</span> <span class="na">for</span><span class="o">=</span><span class="s">"onlineUsers"</span><span class="p">&gt;</span>Online users<span class="p">&lt;/</span><span class="nt">label</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">select</span> <span class="na">multiple</span> <span class="na">class</span><span class="o">=</span><span class="s">"form-control"</span> <span class="na">id</span><span class="o">=</span><span class="s">"onlineUsersSelector"</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">select</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
{{ room.name|json_script:"roomName" }}
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">"{% static 'room.js' %}"</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">body</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">html</span><span class="p">&gt;</span>
</code></pre>
<p>To make our code more readable, we'll include the JavaScript code in separate files -- <em>index.js</em> and <em>room.js</em>, respectively. Because we can't access the Django context in JavaScript, we can use the <a href="https://docs.djangoproject.com/en/4.0/ref/templates/builtins/#json-script">json_script</a> template tag to store <code>room.name</code> and then fetch it in the JavaScript file.</p>
<p>Inside "chat", create a folder called "static". Then, inside "static", create an <em>index.js</em> and a <em>room.js</em> file.</p>
<p><em>index.js</em>:</p>
<pre><span></span><code><span class="c1">// chat/static/index.js</span>

<span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">"Sanity check from index.js."</span><span class="p">);</span>

<span class="c1">// focus 'roomInput' when user opens the page</span>
<span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"#roomInput"</span><span class="p">).</span><span class="nx">focus</span><span class="p">();</span>

<span class="c1">// submit if the user presses the enter key</span>
<span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"#roomInput"</span><span class="p">).</span><span class="nx">onkeyup</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span>
<span class="k">if</span> <span class="p">(</span><span class="nx">e</span><span class="p">.</span><span class="nx">keyCode</span> <span class="o">===</span> <span class="mf">13</span><span class="p">)</span> <span class="p">{</span>  <span class="c1">// enter key</span>
<span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"#roomConnect"</span><span class="p">).</span><span class="nx">click</span><span class="p">();</span>
<span class="p">}</span>
<span class="p">};</span>

<span class="c1">// redirect to '/room/&lt;roomInput&gt;/'</span>
<span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"#roomConnect"</span><span class="p">).</span><span class="nx">onclick</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
<span class="kd">let</span> <span class="nx">roomName</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"#roomInput"</span><span class="p">).</span><span class="nx">value</span><span class="p">;</span>
<span class="nb">window</span><span class="p">.</span><span class="nx">location</span><span class="p">.</span><span class="nx">pathname</span> <span class="o">=</span> <span class="s2">"chat/"</span> <span class="o">+</span> <span class="nx">roomName</span> <span class="o">+</span> <span class="s2">"/"</span><span class="p">;</span>
<span class="p">}</span>

<span class="c1">// redirect to '/room/&lt;roomSelect&gt;/'</span>
<span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"#roomSelect"</span><span class="p">).</span><span class="nx">onchange</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
<span class="kd">let</span> <span class="nx">roomName</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"#roomSelect"</span><span class="p">).</span><span class="nx">value</span><span class="p">.</span><span class="nx">split</span><span class="p">(</span><span class="s2">" ("</span><span class="p">)[</span><span class="mf">0</span><span class="p">];</span>
<span class="nb">window</span><span class="p">.</span><span class="nx">location</span><span class="p">.</span><span class="nx">pathname</span> <span class="o">=</span> <span class="s2">"chat/"</span> <span class="o">+</span> <span class="nx">roomName</span> <span class="o">+</span> <span class="s2">"/"</span><span class="p">;</span>
<span class="p">}</span>
</code></pre>
<p><em>room.js</em>:</p>
<pre><span></span><code><span class="c1">// chat/static/room.js</span>

<span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">"Sanity check from room.js."</span><span class="p">);</span>

<span class="kd">const</span> <span class="nx">roomName</span> <span class="o">=</span> <span class="nb">JSON</span><span class="p">.</span><span class="nx">parse</span><span class="p">(</span><span class="nb">document</span><span class="p">.</span><span class="nx">getElementById</span><span class="p">(</span><span class="s1">'roomName'</span><span class="p">).</span><span class="nx">textContent</span><span class="p">);</span>

<span class="kd">let</span> <span class="nx">chatLog</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"#chatLog"</span><span class="p">);</span>
<span class="kd">let</span> <span class="nx">chatMessageInput</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"#chatMessageInput"</span><span class="p">);</span>
<span class="kd">let</span> <span class="nx">chatMessageSend</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"#chatMessageSend"</span><span class="p">);</span>
<span class="kd">let</span> <span class="nx">onlineUsersSelector</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"#onlineUsersSelector"</span><span class="p">);</span>

<span class="c1">// adds a new option to 'onlineUsersSelector'</span>
<span class="kd">function</span> <span class="nx">onlineUsersSelectorAdd</span><span class="p">(</span><span class="nx">value</span><span class="p">)</span> <span class="p">{</span>
<span class="k">if</span> <span class="p">(</span><span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"option[value='"</span> <span class="o">+</span> <span class="nx">value</span> <span class="o">+</span> <span class="s2">"']"</span><span class="p">))</span> <span class="k">return</span><span class="p">;</span>
<span class="kd">let</span> <span class="nx">newOption</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">createElement</span><span class="p">(</span><span class="s2">"option"</span><span class="p">);</span>
<span class="nx">newOption</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="nx">value</span><span class="p">;</span>
<span class="nx">newOption</span><span class="p">.</span><span class="nx">innerHTML</span> <span class="o">=</span> <span class="nx">value</span><span class="p">;</span>
<span class="nx">onlineUsersSelector</span><span class="p">.</span><span class="nx">appendChild</span><span class="p">(</span><span class="nx">newOption</span><span class="p">);</span>
<span class="p">}</span>

<span class="c1">// removes an option from 'onlineUsersSelector'</span>
<span class="kd">function</span> <span class="nx">onlineUsersSelectorRemove</span><span class="p">(</span><span class="nx">value</span><span class="p">)</span> <span class="p">{</span>
<span class="kd">let</span> <span class="nx">oldOption</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">"option[value='"</span> <span class="o">+</span> <span class="nx">value</span> <span class="o">+</span> <span class="s2">"']"</span><span class="p">);</span>
<span class="k">if</span> <span class="p">(</span><span class="nx">oldOption</span> <span class="o">!==</span> <span class="kc">null</span><span class="p">)</span> <span class="nx">oldOption</span><span class="p">.</span><span class="nx">remove</span><span class="p">();</span>
<span class="p">}</span>

<span class="c1">// focus 'chatMessageInput' when user opens the page</span>
<span class="nx">chatMessageInput</span><span class="p">.</span><span class="nx">focus</span><span class="p">();</span>

<span class="c1">// submit if the user presses the enter key</span>
<span class="nx">chatMessageInput</span><span class="p">.</span><span class="nx">onkeyup</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span>
<span class="k">if</span> <span class="p">(</span><span class="nx">e</span><span class="p">.</span><span class="nx">keyCode</span> <span class="o">===</span> <span class="mf">13</span><span class="p">)</span> <span class="p">{</span>  <span class="c1">// enter key</span>
<span class="nx">chatMessageSend</span><span class="p">.</span><span class="nx">click</span><span class="p">();</span>
<span class="p">}</span>
<span class="p">};</span>

<span class="c1">// clear the 'chatMessageInput' and forward the message</span>
<span class="nx">chatMessageSend</span><span class="p">.</span><span class="nx">onclick</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
<span class="k">if</span> <span class="p">(</span><span class="nx">chatMessageInput</span><span class="p">.</span><span class="nx">value</span><span class="p">.</span><span class="nx">length</span> <span class="o">===</span> <span class="mf">0</span><span class="p">)</span> <span class="k">return</span><span class="p">;</span>
<span class="c1">// TODO: forward the message to the WebSocket</span>
<span class="nx">chatMessageInput</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="s2">""</span><span class="p">;</span>
<span class="p">};</span>
</code></pre>
<p>Your final "chat" app directory structure should now look like this:</p>
<pre><span></span><code>chat
├── __init__.py
├── admin.py
├── apps.py
├── migrations
│   ├── 0001_initial.py
│   ├── __init__.py
├── models.py
├── static
│   ├── index.js
│   └── room.js
├── templates
│   ├── index.html
│   └── room.html
├── tests.py
├── urls.py
└── views.py
</code></pre>
<h3 id="testing">Testing</h3>
<p>With the basic project setup don, let's test things out in the browser.</p>
<p>Start the Django development server:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py runserver
</code></pre>

<p>To ensure that the static files are configured correctly, open the 'Developer Console'. You should see the sanity check:</p>
<pre><span></span><code>Sanity check from index.js.
</code></pre>
<p>Next, enter something in the 'Room name' text input and press enter. </p>

<p>These are just static templates. We'll implement the functionality for the chat and online users later.</p>
<h2 id="add-channels">Add Channels</h2>
<p>Next, let's wire up Django Channels.</p>
<p>Start by installing the package:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ pip install <span class="nv">channels</span><span class="o">==</span><span class="m">3</span>.0.4
</code></pre>
<p>Then, add <code>channels</code> to your <code>INSTALLED_APPS</code> inside <em>core/settings.py</em>:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
<span class="s1">'django.contrib.admin'</span><span class="p">,</span>
<span class="s1">'django.contrib.auth'</span><span class="p">,</span>
<span class="s1">'django.contrib.contenttypes'</span><span class="p">,</span>
<span class="s1">'django.contrib.sessions'</span><span class="p">,</span>
<span class="s1">'django.contrib.messages'</span><span class="p">,</span>
<span class="s1">'django.contrib.staticfiles'</span><span class="p">,</span>
<span class="s1">'chat.apps.ChatConfig'</span><span class="p">,</span>
<span class="s1">'channels'</span><span class="p">,</span>  <span class="c1"># new</span>
<span class="p">]</span>
</code></pre>
<p>Since we'll be using WebSockets instead of HTTP to communicate from the client to the server, we need to wrap our ASGI config with <a href="https://channels.readthedocs.io/en/latest/topics/routing.html#protocoltyperouter">ProtocolTypeRouter</a> in <em>core/asgi.py</em>:</p>
<pre><span></span><code><span class="c1"># core/asgi.py</span>

<span class="kn">import</span> <span class="nn">os</span>

<span class="kn">from</span> <span class="nn">channels.routing</span> <span class="kn">import</span> <span class="n">ProtocolTypeRouter</span>
<span class="kn">from</span> <span class="nn">django.core.asgi</span> <span class="kn">import</span> <span class="n">get_asgi_application</span>

<span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">setdefault</span><span class="p">(</span><span class="s1">'DJANGO_SETTINGS_MODULE'</span><span class="p">,</span> <span class="s1">'core.settings'</span><span class="p">)</span>

<span class="n">application</span> <span class="o">=</span> <span class="n">ProtocolTypeRouter</span><span class="p">({</span>
<span class="s1">'http'</span><span class="p">:</span> <span class="n">get_asgi_application</span><span class="p">(),</span>
<span class="p">})</span>
</code></pre>
<p>This router will route traffic to different parts of the web application depending on the protocol used.</p>
<p>Django versions &lt;= 2.2 don't have built-in ASGI support. In order to get <code>channels</code> running with older Django versions please refer to the <a href="https://channels.readthedocs.io/en/stable/installation.html">official installation guide</a>.</p>
<p>Next, we need to let Django know the location of our ASGI application. Add the following to your <em>core/settings.py</em> file, just below the <code>WSGI_APPLICATION</code> setting:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">WSGI_APPLICATION</span> <span class="o">=</span> <span class="s1">'core.wsgi.application'</span>
<span class="n">ASGI_APPLICATION</span> <span class="o">=</span> <span class="s1">'core.asgi.application'</span>  <span class="c1"># new</span>
</code></pre>
<p>When you run the development server now, you'll see that Channels is being used:</p>
<pre><span></span><code>Starting ASGI/Channels version 3.0.4 development server at http://127.0.0.1:8000/
</code></pre>
<h3 id="add-channel-layer">Add Channel Layer</h3>
<p>A <a href="https://channels.readthedocs.io/en/stable/topics/channel_layers.html">channel layer</a> is a kind of a communication system, which allows multiple parts of our application to exchange messages, without shuttling all the messages or events through the database.</p>
<p>We need a channel layer to give consumers (which we'll implement in the next step) the ability to talk to one another.</p>
<p>While we could use use the <a href="https://channels.readthedocs.io/en/stable/topics/channel_layers.html#in-memory-channel-layer">InMemoryChannelLayer</a> layer since we're in development mode, we'll use a production-ready layer, <a href="https://channels.readthedocs.io/en/stable/topics/channel_layers.html#redis-channel-layer">RedisChannelLayer</a>.</p>
<p>Since this layer requires <a href="https://redis.io/">Redis</a>, run the following command to get it up and running with <a href="https://www.docker.com/">Docker</a>:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ docker run -p <span class="m">6379</span>:6379 -d redis:5
</code></pre>
<p>This command downloads the image and spins up a Redis Docker container on port <code>6379</code>.</p>
<p>If you don't want to use Docker, feel free to download Redis directly from the <a href="https://redis.io/download">official website</a>.</p>
<p>To connect to Redis from Django, we need to install an additional package called <a href="https://github.com/django/channels_redis">channels_redis</a>:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ pip install <span class="nv">channels_redis</span><span class="o">==</span><span class="m">3</span>.3.1
</code></pre>
<p>After that, configure the layer in <em>core/settings.py</em> like so:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">CHANNEL_LAYERS</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">'default'</span><span class="p">:</span> <span class="p">{</span>
<span class="s1">'BACKEND'</span><span class="p">:</span> <span class="s1">'channels_redis.core.RedisChannelLayer'</span><span class="p">,</span>
<span class="s1">'CONFIG'</span><span class="p">:</span> <span class="p">{</span>
<span class="s2">"hosts"</span><span class="p">:</span> <span class="p">[(</span><span class="s1">'127.0.0.1'</span><span class="p">,</span> <span class="mi">6379</span><span class="p">)],</span>
<span class="p">},</span>
<span class="p">},</span>
<span class="p">}</span>
</code></pre>
<p>Here, we let channels_redis know where the Redis server is located.</p>
<p>To test if everything works as expected, open the Django shell:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py shell
</code></pre>
<p>Then run:</p>
<pre><span></span><code>&gt;&gt;&gt; import channels.layers
&gt;&gt;&gt; <span class="nv">channel_layer</span> <span class="o">=</span> channels.layers.get_channel_layer<span class="o">()</span>
&gt;&gt;&gt;
&gt;&gt;&gt; from asgiref.sync import async_to_sync
&gt;&gt;&gt; async_to_sync<span class="o">(</span>channel_layer.send<span class="o">)(</span><span class="s1">'test_channel'</span>, <span class="o">{</span><span class="s1">'type'</span>: <span class="s1">'hello'</span><span class="o">})</span>
&gt;&gt;&gt; async_to_sync<span class="o">(</span>channel_layer.receive<span class="o">)(</span><span class="s1">'test_channel'</span><span class="o">)</span>
<span class="o">{</span><span class="s1">'type'</span>: <span class="s1">'hello'</span><span class="o">}</span>
</code></pre>
<p>Here, we connected to the channel layer using the settings defined in <em>core/settings.py</em>. We then used <code>channel_layer.send</code> to send a message to the <code>test_channel</code> group and <code>channel_layer.receive</code> to read all the messages sent to the same group.</p>
<p>Take note that we wrapped all the function calls in <code>async_to_sync</code> because the channel layer is asynchronous.</p>
<p>Enter <code>quit()</code> to exit the shell.</p>
<h3 id="add-channels-consumer">Add Channels Consumer</h3>
<p>A <a href="https://channels.readthedocs.io/en/stable/topics/consumers.html">consumer</a> is the basic unit of Channels code. They are tiny ASGI applications, driven by events. They are akin to Django views. However, unlike Django views, consumers are long-running by default. A Django project can have multiple consumers that are combined using Channels routing (which we'll take a look at in the next section).</p>
<p>Each consumer has it's own scope, which is a set of details about a single incoming connection. They contain pieces of data like protocol type, path, headers, routing arguments, user agent, and more.</p>
<p>Create a new file called <em>consumers.py</em> inside "chat":</p>
<pre><span></span><code><span class="c1"># chat/consumers.py</span>

<span class="kn">import</span> <span class="nn">json</span>

<span class="kn">from</span> <span class="nn">asgiref.sync</span> <span class="kn">import</span> <span class="n">async_to_sync</span>
<span class="kn">from</span> <span class="nn">channels.generic.websocket</span> <span class="kn">import</span> <span class="n">WebsocketConsumer</span>

<span class="kn">from</span> <span class="nn">.models</span> <span class="kn">import</span> <span class="n">Room</span>


<span class="k">class</span> <span class="nc">ChatConsumer</span><span class="p">(</span><span class="n">WebsocketConsumer</span><span class="p">):</span>

<span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="n">args</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_name</span> <span class="o">=</span> <span class="kc">None</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span> <span class="o">=</span> <span class="kc">None</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room</span> <span class="o">=</span> <span class="kc">None</span>

<span class="k">def</span> <span class="nf">connect</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_name</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">scope</span><span class="p">[</span><span class="s1">'url_route'</span><span class="p">][</span><span class="s1">'kwargs'</span><span class="p">][</span><span class="s1">'room_name'</span><span class="p">]</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">'chat_</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">room_name</span><span class="si">}</span><span class="s1">'</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room</span> <span class="o">=</span> <span class="n">Room</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">room_name</span><span class="p">)</span>

<span class="c1"># connection has to be accepted</span>
<span class="bp">self</span><span class="o">.</span><span class="n">accept</span><span class="p">()</span>

<span class="c1"># join the room group</span>
<span class="n">async_to_sync</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">channel_layer</span><span class="o">.</span><span class="n">group_add</span><span class="p">)(</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span><span class="p">,</span>
<span class="bp">self</span><span class="o">.</span><span class="n">channel_name</span><span class="p">,</span>
<span class="p">)</span>

<span class="k">def</span> <span class="nf">disconnect</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">close_code</span><span class="p">):</span>
<span class="n">async_to_sync</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">channel_layer</span><span class="o">.</span><span class="n">group_discard</span><span class="p">)(</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span><span class="p">,</span>
<span class="bp">self</span><span class="o">.</span><span class="n">channel_name</span><span class="p">,</span>
<span class="p">)</span>

<span class="k">def</span> <span class="nf">receive</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">text_data</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">bytes_data</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
<span class="n">text_data_json</span> <span class="o">=</span> <span class="n">json</span><span class="o">.</span><span class="n">loads</span><span class="p">(</span><span class="n">text_data</span><span class="p">)</span>
<span class="n">message</span> <span class="o">=</span> <span class="n">text_data_json</span><span class="p">[</span><span class="s1">'message'</span><span class="p">]</span>

<span class="c1"># send chat message event to the room</span>
<span class="n">async_to_sync</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">channel_layer</span><span class="o">.</span><span class="n">group_send</span><span class="p">)(</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span><span class="p">,</span>
<span class="p">{</span>
<span class="s1">'type'</span><span class="p">:</span> <span class="s1">'chat_message'</span><span class="p">,</span>
<span class="s1">'message'</span><span class="p">:</span> <span class="n">message</span><span class="p">,</span>
<span class="p">}</span>
<span class="p">)</span>

<span class="k">def</span> <span class="nf">chat_message</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">event</span><span class="p">):</span>
<span class="bp">self</span><span class="o">.</span><span class="n">send</span><span class="p">(</span><span class="n">text_data</span><span class="o">=</span><span class="n">json</span><span class="o">.</span><span class="n">dumps</span><span class="p">(</span><span class="n">event</span><span class="p">))</span>
</code></pre>
<p>Here, we created a <code>ChatConsumer</code>, which inherits from <a href="https://channels.readthedocs.io/en/latest/topics/consumers.html#websocketconsumer">WebsocketConsumer</a>. <code>WebsocketConsumer</code> provides three methods, <code>connect()</code>, <code>disconnect()</code>, and <code>receive()</code>:</p>
<ol>
<li>Inside <code>connect()</code> we called <code>accept()</code> in order to accept the connection. After that, we added the user to the channel layer group.</li>
<li>Inside <code>disconnect()</code> we removed the user from the channel layer group.</li>
<li>Inside <code>receive()</code> we parsed the data to JSON and extracted the <code>message</code>. Then, we forwarded the <code>message</code> using <code>group_send</code> to <code>chat_message</code>.</li>
</ol>
<li>Inside <code>connect()</code> we called <code>accept()</code> in order to accept the connection. After that, we added the user to the channel layer group.</li>
<li>Inside <code>disconnect()</code> we removed the user from the channel layer group.</li>
<li>Inside <code>receive()</code> we parsed the data to JSON and extracted the <code>message</code>. Then, we forwarded the <code>message</code> using <code>group_send</code> to <code>chat_message</code>.</li>
<p>When using channel layer's <code>group_send</code>, your consumer has to have a method for every JSON message <code>type</code> you use. In our situation, <code>type</code> is equaled to <code>chat_message</code>. Thus, we added a method called <code>chat_message</code>.</p>
<p>If you use dots in your message types, Channels will automatically convert them to underscores when looking for a method -- e.g, <code>chat.message</code> will become <code>chat_message</code>.</p>
<p>Since <code>WebsocketConsumer</code> is a synchronous consumer, we had to call <code>async_to_sync</code> when working with the channel layer. We decided to go with a sync consumer since the chat app is closely connected to Django (which is sync by default). In other words, we wouldn't get a performance boost by using an async consumer.</p>
<p>You should use sync consumers by default. What's more, only use async consumers in cases where you're absolutely certain that you're doing something that would benefit from async handling (e.g., long-running tasks that could be done in parallel) and you're only using async-native libraries.</p>
<h3 id="add-channels-routing">Add Channels Routing</h3>
<p>Channels provides different <a href="https://channels.readthedocs.io/en/stable/topics/routing.html">routing</a> classes which allow us to combine and stack consumers. They are similar to Django's URLs.</p>
<p>Add a <em>routing.py</em> file to "chat":</p>
<pre><span></span><code><span class="c1"># chat/routing.py</span>

<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">re_path</span>

<span class="kn">from</span> <span class="nn">.</span> <span class="kn">import</span> <span class="n">consumers</span>

<span class="n">websocket_urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">re_path</span><span class="p">(</span><span class="sa">r</span><span class="s1">'ws/chat/(?P&lt;room_name&gt;\w+)/$'</span><span class="p">,</span> <span class="n">consumers</span><span class="o">.</span><span class="n">ChatConsumer</span><span class="o">.</span><span class="n">as_asgi</span><span class="p">()),</span>
<span class="p">]</span>
</code></pre>
<p>Register the <em>routing.py</em> file inside <em>core/asgi.py</em>:</p>
<pre><span></span><code><span class="c1"># core/asgi.py</span>

<span class="kn">import</span> <span class="nn">os</span>

<span class="kn">from</span> <span class="nn">channels.routing</span> <span class="kn">import</span> <span class="n">ProtocolTypeRouter</span><span class="p">,</span> <span class="n">URLRouter</span>
<span class="kn">from</span> <span class="nn">django.core.asgi</span> <span class="kn">import</span> <span class="n">get_asgi_application</span>

<span class="kn">import</span> <span class="nn">chat.routing</span>

<span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">setdefault</span><span class="p">(</span><span class="s1">'DJANGO_SETTINGS_MODULE'</span><span class="p">,</span> <span class="s1">'core.settings'</span><span class="p">)</span>

<span class="n">application</span> <span class="o">=</span> <span class="n">ProtocolTypeRouter</span><span class="p">({</span>
<span class="s1">'http'</span><span class="p">:</span> <span class="n">get_asgi_application</span><span class="p">(),</span>
<span class="s1">'websocket'</span><span class="p">:</span> <span class="n">URLRouter</span><span class="p">(</span>
<span class="n">chat</span><span class="o">.</span><span class="n">routing</span><span class="o">.</span><span class="n">websocket_urlpatterns</span>
<span class="p">),</span>
<span class="p">})</span>
</code></pre>
<h3 id="websockets-frontend">WebSockets (frontend)</h3>
<p>To communicate with Channels from the frontend, we'll use the <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSocket">WebSocket API</a>.</p>
<p>WebSockets are extremely easy to use. First, you need to establish a connection by providing a <code>url</code> and then you can listen for the following events:</p>
<ol>
<li><code>onopen</code> - called when a WebSocket connection is established</li>
<li><code>onclose</code> - called when a WebSocket connection is destroyed</li>
<li><code>onmessage</code> - called when a WebSocket receives a message</li>
<li><code>onerror</code> - called when a WebSocket encounters an error</li>
</ol>
<li><code>onopen</code> - called when a WebSocket connection is established</li>
<li><code>onclose</code> - called when a WebSocket connection is destroyed</li>
<li><code>onmessage</code> - called when a WebSocket receives a message</li>
<li><code>onerror</code> - called when a WebSocket encounters an error</li>
<p>To integrate WebSockets into the application, add the following to the bottom of <em>room.js</em>:</p>
<pre><span></span><code><span class="c1">// chat/static/room.js</span>

<span class="kd">let</span> <span class="nx">chatSocket</span> <span class="o">=</span> <span class="kc">null</span><span class="p">;</span>

<span class="kd">function</span> <span class="nx">connect</span><span class="p">()</span> <span class="p">{</span>
<span class="nx">chatSocket</span> <span class="o">=</span> <span class="ow">new</span> <span class="nx">WebSocket</span><span class="p">(</span><span class="s2">"ws://"</span> <span class="o">+</span> <span class="nb">window</span><span class="p">.</span><span class="nx">location</span><span class="p">.</span><span class="nx">host</span> <span class="o">+</span> <span class="s2">"/ws/chat/"</span> <span class="o">+</span> <span class="nx">roomName</span> <span class="o">+</span> <span class="s2">"/"</span><span class="p">);</span>

<span class="nx">chatSocket</span><span class="p">.</span><span class="nx">onopen</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span>
<span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">"Successfully connected to the WebSocket."</span><span class="p">);</span>
<span class="p">}</span>

<span class="nx">chatSocket</span><span class="p">.</span><span class="nx">onclose</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span>
<span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">"WebSocket connection closed unexpectedly. Trying to reconnect in 2s..."</span><span class="p">);</span>
<span class="nx">setTimeout</span><span class="p">(</span><span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
<span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">"Reconnecting..."</span><span class="p">);</span>
<span class="nx">connect</span><span class="p">();</span>
<span class="p">},</span> <span class="mf">2000</span><span class="p">);</span>
<span class="p">};</span>

<span class="nx">chatSocket</span><span class="p">.</span><span class="nx">onmessage</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span>
<span class="kd">const</span> <span class="nx">data</span> <span class="o">=</span> <span class="nb">JSON</span><span class="p">.</span><span class="nx">parse</span><span class="p">(</span><span class="nx">e</span><span class="p">.</span><span class="nx">data</span><span class="p">);</span>
<span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="nx">data</span><span class="p">);</span>

<span class="k">switch</span> <span class="p">(</span><span class="nx">data</span><span class="p">.</span><span class="nx">type</span><span class="p">)</span> <span class="p">{</span>
<span class="k">case</span> <span class="s2">"chat_message"</span><span class="o">:</span>
<span class="nx">chatLog</span><span class="p">.</span><span class="nx">value</span> <span class="o">+=</span> <span class="nx">data</span><span class="p">.</span><span class="nx">message</span> <span class="o">+</span> <span class="s2">"\n"</span><span class="p">;</span>
<span class="k">break</span><span class="p">;</span>
<span class="k">default</span><span class="o">:</span>
<span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">(</span><span class="s2">"Unknown message type!"</span><span class="p">);</span>
<span class="k">break</span><span class="p">;</span>
<span class="p">}</span>

<span class="c1">// scroll 'chatLog' to the bottom</span>
<span class="nx">chatLog</span><span class="p">.</span><span class="nx">scrollTop</span> <span class="o">=</span> <span class="nx">chatLog</span><span class="p">.</span><span class="nx">scrollHeight</span><span class="p">;</span>
<span class="p">};</span>

<span class="nx">chatSocket</span><span class="p">.</span><span class="nx">onerror</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span> <span class="p">{</span>
<span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">"WebSocket encountered an error: "</span> <span class="o">+</span> <span class="nx">err</span><span class="p">.</span><span class="nx">message</span><span class="p">);</span>
<span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">"Closing the socket."</span><span class="p">);</span>
<span class="nx">chatSocket</span><span class="p">.</span><span class="nx">close</span><span class="p">();</span>
<span class="p">}</span>
<span class="p">}</span>
<span class="nx">connect</span><span class="p">();</span>
</code></pre>
<p>After establishing the WebSocket connection, in the <code>onmessage</code> event, we determined the message type based on <code>data.type</code>. Take note how we wrapped the WebSocket inside the <code>connect()</code> method to have the ability to re-establish the connection in case it drops.</p>
<p>Lastly, change the TODO inside <code>chatMessageSend.onclickForm</code> to the following:</p>
<pre><span></span><code><span class="c1">// chat/static/room.js</span>

<span class="nx">chatSocket</span><span class="p">.</span><span class="nx">send</span><span class="p">(</span><span class="nb">JSON</span><span class="p">.</span><span class="nx">stringify</span><span class="p">({</span>
<span class="s2">"message"</span><span class="o">:</span> <span class="nx">chatMessageInput</span><span class="p">.</span><span class="nx">value</span><span class="p">,</span>
<span class="p">}));</span>
</code></pre>
<p>The full handler should now look like this:</p>
<pre><span></span><code><span class="c1">// chat/static/room.js</span>

<span class="nx">chatMessageSend</span><span class="p">.</span><span class="nx">onclick</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
<span class="k">if</span> <span class="p">(</span><span class="nx">chatMessageInput</span><span class="p">.</span><span class="nx">value</span><span class="p">.</span><span class="nx">length</span> <span class="o">===</span> <span class="mf">0</span><span class="p">)</span> <span class="k">return</span><span class="p">;</span>
<span class="nx">chatSocket</span><span class="p">.</span><span class="nx">send</span><span class="p">(</span><span class="nb">JSON</span><span class="p">.</span><span class="nx">stringify</span><span class="p">({</span>
<span class="s2">"message"</span><span class="o">:</span> <span class="nx">chatMessageInput</span><span class="p">.</span><span class="nx">value</span><span class="p">,</span>
<span class="p">}));</span>
<span class="nx">chatMessageInput</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="s2">""</span><span class="p">;</span>
<span class="p">};</span>
</code></pre>
<p>The first version of the chat is done.</p>
<p>To test, run the development server. Then, open two private/incognito browser windows and, in each, navigate to <a href="http://localhost:8000/chat/default/">http://localhost:8000/chat/default/</a>. You should be able to send a messages.</p>
<p>That's it for the basic functionality. Next, we'll look at authentication.</p>
<h2 id="authentication">Authentication</h2>
<h3 id="backend">Backend</h3>
<p>Channels comes with a built-in class for Django session and <a href="https://channels.readthedocs.io/en/latest/topics/authentication.html">authentication</a> management called <code>AuthMiddlewareStack</code>.</p>
<p>To use it, the only thing we have to do is to wrap <code>URLRouter</code> inside <em>core/asgi.py</em> like so:</p>
<pre><span></span><code><span class="c1"># core/asgi.py</span>

<span class="kn">import</span> <span class="nn">os</span>

<span class="kn">from</span> <span class="nn">channels.auth</span> <span class="kn">import</span> <span class="n">AuthMiddlewareStack</span>  <span class="c1"># new import</span>
<span class="kn">from</span> <span class="nn">channels.routing</span> <span class="kn">import</span> <span class="n">ProtocolTypeRouter</span><span class="p">,</span> <span class="n">URLRouter</span>
<span class="kn">from</span> <span class="nn">django.core.asgi</span> <span class="kn">import</span> <span class="n">get_asgi_application</span>

<span class="kn">import</span> <span class="nn">chat.routing</span>

<span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">setdefault</span><span class="p">(</span><span class="s1">'DJANGO_SETTINGS_MODULE'</span><span class="p">,</span> <span class="s1">'core.settings'</span><span class="p">)</span>

<span class="n">application</span> <span class="o">=</span> <span class="n">ProtocolTypeRouter</span><span class="p">({</span>
<span class="s1">'http'</span><span class="p">:</span> <span class="n">get_asgi_application</span><span class="p">(),</span>
<span class="s1">'websocket'</span><span class="p">:</span> <span class="n">AuthMiddlewareStack</span><span class="p">(</span>  <span class="c1"># new</span>
<span class="n">URLRouter</span><span class="p">(</span>
<span class="n">chat</span><span class="o">.</span><span class="n">routing</span><span class="o">.</span><span class="n">websocket_urlpatterns</span>
<span class="p">)</span>
<span class="p">),</span>  <span class="c1"># new</span>
<span class="p">})</span>
</code></pre>
<p>Now, whenever an authenticated client joins, the user object will be added to the scope. It can accessed like so:</p>
<pre><span></span><code><span class="n">user</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">scope</span><span class="p">[</span><span class="s1">'user'</span><span class="p">]</span>
</code></pre>
<p>If you want to run Channels with a frontend JavaScript framework (like Angular, React, or Vue), you'll have to use a different authentication system (e.g., token authentication). If you want to learn how to use token authentication with Channels, check out the following courses:</p>
<ol>
<li><a href="/courses/real-time-app-with-django-channels-and-angular/">Developing a Real-Time Taxi App with Django Channels and Angular</a></li>
<li><a href="/courses/taxi-react/">Developing a Real-Time Taxi App with Django Channels and React</a></li>
</ol>
<li><a href="/courses/real-time-app-with-django-channels-and-angular/">Developing a Real-Time Taxi App with Django Channels and Angular</a></li>
<li><a href="/courses/taxi-react/">Developing a Real-Time Taxi App with Django Channels and React</a></li>
<p>Let's modify the <code>ChatConsumer</code> to block non-authenticated users from talking and to display the user's username with the message.</p>
<p>Change <em>chat/consumers.py</em> to the following:</p>
<pre><span></span><code><span class="c1"># chat/consumers.py</span>

<span class="kn">import</span> <span class="nn">json</span>

<span class="kn">from</span> <span class="nn">asgiref.sync</span> <span class="kn">import</span> <span class="n">async_to_sync</span>
<span class="kn">from</span> <span class="nn">channels.generic.websocket</span> <span class="kn">import</span> <span class="n">WebsocketConsumer</span>

<span class="kn">from</span> <span class="nn">.models</span> <span class="kn">import</span> <span class="n">Room</span><span class="p">,</span> <span class="n">Message</span>  <span class="c1"># new import</span>


<span class="k">class</span> <span class="nc">ChatConsumer</span><span class="p">(</span><span class="n">WebsocketConsumer</span><span class="p">):</span>

<span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="n">args</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_name</span> <span class="o">=</span> <span class="kc">None</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span> <span class="o">=</span> <span class="kc">None</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room</span> <span class="o">=</span> <span class="kc">None</span>
<span class="bp">self</span><span class="o">.</span><span class="n">user</span> <span class="o">=</span> <span class="kc">None</span>  <span class="c1"># new</span>

<span class="k">def</span> <span class="nf">connect</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_name</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">scope</span><span class="p">[</span><span class="s1">'url_route'</span><span class="p">][</span><span class="s1">'kwargs'</span><span class="p">][</span><span class="s1">'room_name'</span><span class="p">]</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">'chat_</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">room_name</span><span class="si">}</span><span class="s1">'</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room</span> <span class="o">=</span> <span class="n">Room</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">room_name</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">user</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">scope</span><span class="p">[</span><span class="s1">'user'</span><span class="p">]</span>  <span class="c1"># new</span>

<span class="c1"># connection has to be accepted</span>
<span class="bp">self</span><span class="o">.</span><span class="n">accept</span><span class="p">()</span>

<span class="c1"># join the room group</span>
<span class="n">async_to_sync</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">channel_layer</span><span class="o">.</span><span class="n">group_add</span><span class="p">)(</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span><span class="p">,</span>
<span class="bp">self</span><span class="o">.</span><span class="n">channel_name</span><span class="p">,</span>
<span class="p">)</span>

<span class="k">def</span> <span class="nf">disconnect</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">close_code</span><span class="p">):</span>
<span class="n">async_to_sync</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">channel_layer</span><span class="o">.</span><span class="n">group_discard</span><span class="p">)(</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span><span class="p">,</span>
<span class="bp">self</span><span class="o">.</span><span class="n">channel_name</span><span class="p">,</span>
<span class="p">)</span>

<span class="k">def</span> <span class="nf">receive</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">text_data</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">bytes_data</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
<span class="n">text_data_json</span> <span class="o">=</span> <span class="n">json</span><span class="o">.</span><span class="n">loads</span><span class="p">(</span><span class="n">text_data</span><span class="p">)</span>
<span class="n">message</span> <span class="o">=</span> <span class="n">text_data_json</span><span class="p">[</span><span class="s1">'message'</span><span class="p">]</span>

<span class="k">if</span> <span class="ow">not</span> <span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">is_authenticated</span><span class="p">:</span>  <span class="c1"># new</span>
<span class="k">return</span>                          <span class="c1"># new</span>

<span class="c1"># send chat message event to the room</span>
<span class="n">async_to_sync</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">channel_layer</span><span class="o">.</span><span class="n">group_send</span><span class="p">)(</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span><span class="p">,</span>
<span class="p">{</span>
<span class="s1">'type'</span><span class="p">:</span> <span class="s1">'chat_message'</span><span class="p">,</span>
<span class="s1">'user'</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">username</span><span class="p">,</span>  <span class="c1"># new</span>
<span class="s1">'message'</span><span class="p">:</span> <span class="n">message</span><span class="p">,</span>
<span class="p">}</span>
<span class="p">)</span>
<span class="n">Message</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">create</span><span class="p">(</span><span class="n">user</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="p">,</span> <span class="n">room</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">room</span><span class="p">,</span> <span class="n">content</span><span class="o">=</span><span class="n">message</span><span class="p">)</span>  <span class="c1"># new</span>

<span class="k">def</span> <span class="nf">chat_message</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">event</span><span class="p">):</span>
<span class="bp">self</span><span class="o">.</span><span class="n">send</span><span class="p">(</span><span class="n">text_data</span><span class="o">=</span><span class="n">json</span><span class="o">.</span><span class="n">dumps</span><span class="p">(</span><span class="n">event</span><span class="p">))</span>
</code></pre>
<h3 id="frontend">Frontend</h3>
<p>Next, let's modify <em>room.js</em> to display the user's username. Inside <code>chatSocket.onMessage</code>, add the following:</p>
<pre><span></span><code><span class="c1">// chat/static/room.js</span>

<span class="nx">chatSocket</span><span class="p">.</span><span class="nx">onmessage</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span>
<span class="kd">const</span> <span class="nx">data</span> <span class="o">=</span> <span class="nb">JSON</span><span class="p">.</span><span class="nx">parse</span><span class="p">(</span><span class="nx">e</span><span class="p">.</span><span class="nx">data</span><span class="p">);</span>
<span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="nx">data</span><span class="p">);</span>

<span class="k">switch</span> <span class="p">(</span><span class="nx">data</span><span class="p">.</span><span class="nx">type</span><span class="p">)</span> <span class="p">{</span>
<span class="k">case</span> <span class="s2">"chat_message"</span><span class="o">:</span>
<span class="nx">chatLog</span><span class="p">.</span><span class="nx">value</span> <span class="o">+=</span> <span class="nx">data</span><span class="p">.</span><span class="nx">user</span> <span class="o">+</span> <span class="s2">": "</span> <span class="o">+</span> <span class="nx">data</span><span class="p">.</span><span class="nx">message</span> <span class="o">+</span> <span class="s2">"\n"</span><span class="p">;</span>  <span class="c1">// new</span>
<span class="k">break</span><span class="p">;</span>
<span class="k">default</span><span class="o">:</span>
<span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">(</span><span class="s2">"Unknown message type!"</span><span class="p">);</span>
<span class="k">break</span><span class="p">;</span>
<span class="p">}</span>

<span class="c1">// scroll 'chatLog' to the bottom</span>
<span class="nx">chatLog</span><span class="p">.</span><span class="nx">scrollTop</span> <span class="o">=</span> <span class="nx">chatLog</span><span class="p">.</span><span class="nx">scrollHeight</span><span class="p">;</span>
<span class="p">};</span>
</code></pre>
<h3 id="testing_1">Testing</h3>
<p>Create a superuser, which you'll use for testing:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py createsuperuser
</code></pre>
<p>Run the server:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>Open the browser and log in using the Django admin login at <a href="http://localhost:8000/admin">http://localhost:8000/admin</a>.</p>
<p>Then navigate to <a href="http://localhost:8000/chat/default">http://localhost:8000/chat/default</a>.</p>

<p>Log out of the Django admin. Navigate to <a href="http://localhost:8000/chat/default">http://localhost:8000/chat/default</a>. What happens when you try to post a message?</p>
<h2 id="user-messages">User Messages</h2>
<p>Next, we'll add the following three message types:</p>
<ol>
<li><code>user_list</code> - sent to the newly joined user (<code>data.users</code> = list of online users)</li>
<li><code>user_join</code> - sent when a user joins a chat room</li>
<li><code>user_leave</code> - sent when a user leaves a chat room</li>
</ol>
<li><code>user_list</code> - sent to the newly joined user (<code>data.users</code> = list of online users)</li>
<li><code>user_join</code> - sent when a user joins a chat room</li>
<li><code>user_leave</code> - sent when a user leaves a chat room</li>
<h3 id="backend_1">Backend</h3>
<p>At the end of the <code>connect</code> method in <code>ChatConsumer</code> add:</p>
<pre><span></span><code><span class="c1"># chat/consumers.py</span>

<span class="k">def</span> <span class="nf">connect</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="c1"># ...</span>

<span class="c1"># send the user list to the newly joined user</span>
<span class="bp">self</span><span class="o">.</span><span class="n">send</span><span class="p">(</span><span class="n">json</span><span class="o">.</span><span class="n">dumps</span><span class="p">({</span>
<span class="s1">'type'</span><span class="p">:</span> <span class="s1">'user_list'</span><span class="p">,</span>
<span class="s1">'users'</span><span class="p">:</span> <span class="p">[</span><span class="n">user</span><span class="o">.</span><span class="n">username</span> <span class="k">for</span> <span class="n">user</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">room</span><span class="o">.</span><span class="n">online</span><span class="o">.</span><span class="n">all</span><span class="p">()],</span>
<span class="p">}))</span>

<span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">is_authenticated</span><span class="p">:</span>
<span class="c1"># send the join event to the room</span>
<span class="n">async_to_sync</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">channel_layer</span><span class="o">.</span><span class="n">group_send</span><span class="p">)(</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span><span class="p">,</span>
<span class="p">{</span>
<span class="s1">'type'</span><span class="p">:</span> <span class="s1">'user_join'</span><span class="p">,</span>
<span class="s1">'user'</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">username</span><span class="p">,</span>
<span class="p">}</span>
<span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room</span><span class="o">.</span><span class="n">online</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="p">)</span>
</code></pre>
<p>At the end of the <code>disconnect</code> method in <code>ChatConsumer</code> add:</p>
<pre><span></span><code><span class="c1"># chat/consumers.py</span>

<span class="k">def</span> <span class="nf">disconnect</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">close_code</span><span class="p">):</span>
<span class="c1"># ...</span>

<span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">is_authenticated</span><span class="p">:</span>
<span class="c1"># send the leave event to the room</span>
<span class="n">async_to_sync</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">channel_layer</span><span class="o">.</span><span class="n">group_send</span><span class="p">)(</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span><span class="p">,</span>
<span class="p">{</span>
<span class="s1">'type'</span><span class="p">:</span> <span class="s1">'user_leave'</span><span class="p">,</span>
<span class="s1">'user'</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">username</span><span class="p">,</span>
<span class="p">}</span>
<span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room</span><span class="o">.</span><span class="n">online</span><span class="o">.</span><span class="n">remove</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="p">)</span>
</code></pre>
<p>Because we added new message types, we also need to add the methods for the channel layer. At the end of <em>chat/consumers.py</em> add:</p>
<pre><span></span><code><span class="c1"># chat/consumers.py</span>

<span class="k">def</span> <span class="nf">user_join</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">event</span><span class="p">):</span>
<span class="bp">self</span><span class="o">.</span><span class="n">send</span><span class="p">(</span><span class="n">text_data</span><span class="o">=</span><span class="n">json</span><span class="o">.</span><span class="n">dumps</span><span class="p">(</span><span class="n">event</span><span class="p">))</span>

<span class="k">def</span> <span class="nf">user_leave</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">event</span><span class="p">):</span>
<span class="bp">self</span><span class="o">.</span><span class="n">send</span><span class="p">(</span><span class="n">text_data</span><span class="o">=</span><span class="n">json</span><span class="o">.</span><span class="n">dumps</span><span class="p">(</span><span class="n">event</span><span class="p">))</span>
</code></pre>
<p>Your <em>consumers.py</em> after this step should look like this: <a href="https://gist.github.com/duplxey/095d2abd25cef0b58c4aa724bab6fb70">consumers.py</a>.</p>
<h3 id="frontend_1">Frontend</h3>
<p>To handle the messages from the frontend add the following cases to the switch statement in the <code>chatSocket.onmessage</code> handler:</p>
<pre><span></span><code><span class="c1">// chat/static/room.js</span>

<span class="k">switch</span> <span class="p">(</span><span class="nx">data</span><span class="p">.</span><span class="nx">type</span><span class="p">)</span> <span class="p">{</span>
<span class="c1">// ...</span>
<span class="k">case</span> <span class="s2">"user_list"</span><span class="o">:</span>
<span class="k">for</span> <span class="p">(</span><span class="kd">let</span> <span class="nx">i</span> <span class="o">=</span> <span class="mf">0</span><span class="p">;</span> <span class="nx">i</span> <span class="o">&lt;</span> <span class="nx">data</span><span class="p">.</span><span class="nx">users</span><span class="p">.</span><span class="nx">length</span><span class="p">;</span> <span class="nx">i</span><span class="o">++</span><span class="p">)</span> <span class="p">{</span>
<span class="nx">onlineUsersSelectorAdd</span><span class="p">(</span><span class="nx">data</span><span class="p">.</span><span class="nx">users</span><span class="p">[</span><span class="nx">i</span><span class="p">]);</span>
<span class="p">}</span>
<span class="k">break</span><span class="p">;</span>
<span class="k">case</span> <span class="s2">"user_join"</span><span class="o">:</span>
<span class="nx">chatLog</span><span class="p">.</span><span class="nx">value</span> <span class="o">+=</span> <span class="nx">data</span><span class="p">.</span><span class="nx">user</span> <span class="o">+</span> <span class="s2">" joined the room.\n"</span><span class="p">;</span>
<span class="nx">onlineUsersSelectorAdd</span><span class="p">(</span><span class="nx">data</span><span class="p">.</span><span class="nx">user</span><span class="p">);</span>
<span class="k">break</span><span class="p">;</span>
<span class="k">case</span> <span class="s2">"user_leave"</span><span class="o">:</span>
<span class="nx">chatLog</span><span class="p">.</span><span class="nx">value</span> <span class="o">+=</span> <span class="nx">data</span><span class="p">.</span><span class="nx">user</span> <span class="o">+</span> <span class="s2">" left the room.\n"</span><span class="p">;</span>
<span class="nx">onlineUsersSelectorRemove</span><span class="p">(</span><span class="nx">data</span><span class="p">.</span><span class="nx">user</span><span class="p">);</span>
<span class="k">break</span><span class="p">;</span>
<span class="c1">// ...</span>
</code></pre>
<h4 id="testing_2">Testing</h4>
<p>Run the server again, log in, and visit <a href="http://localhost:8000/chat/default">http://localhost:8000/chat/default</a>.</p>

<p>You should now be able to see join and leave messages. The user list should be populated as well.</p>
<h2 id="private-messaging">Private Messaging</h2>
<p>The Channels package doesn't allow direct filtering, so there's no built-in method for sending messages from a client to another client. With Channels you can either send a message to:</p>
<ol>
<li>The consumer's client (<code>self.send</code>)</li>
<li>A channel layer group (<code>self.channel_layer.group_send</code>)</li>
</ol>
<li>The consumer's client (<code>self.send</code>)</li>
<li>A channel layer group (<code>self.channel_layer.group_send</code>)</li>
<p>Thus, in order to implement private messaging, we'll:</p>
<ol>
<li>Create a new group called <code>inbox_%USERNAME%</code> every time a client joins.</li>
<li>Add the client to their own inbox group (<code>inbox_%USERNAME%</code>).</li>
<li>Remove the client from their inbox group (<code>inbox_%USERNAME%</code>) when they disconnect.</li>
</ol>
<li>Create a new group called <code>inbox_%USERNAME%</code> every time a client joins.</li>
<li>Add the client to their own inbox group (<code>inbox_%USERNAME%</code>).</li>
<li>Remove the client from their inbox group (<code>inbox_%USERNAME%</code>) when they disconnect.</li>
<p>Once implemented, each client will have their own inbox for private messages. Other clients can then send private messages to <code>inbox_%TARGET_USERNAME%</code>.</p>
<h3 id="backend_2">Backend</h3>
<p>Modify <em>chat/consumers.py</em>.</p>
<pre><span></span><code><span class="c1"># chat/consumers.py</span>

<span class="k">class</span> <span class="nc">ChatConsumer</span><span class="p">(</span><span class="n">WebsocketConsumer</span><span class="p">):</span>

<span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
<span class="c1"># ...</span>
<span class="bp">self</span><span class="o">.</span><span class="n">user_inbox</span> <span class="o">=</span> <span class="kc">None</span>  <span class="c1"># new</span>

<span class="k">def</span> <span class="nf">connect</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="c1"># ...</span>
<span class="bp">self</span><span class="o">.</span><span class="n">user_inbox</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">'inbox_</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">username</span><span class="si">}</span><span class="s1">'</span>  <span class="c1"># new</span>

<span class="c1"># accept the incoming connection</span>
<span class="bp">self</span><span class="o">.</span><span class="n">accept</span><span class="p">()</span>

<span class="c1"># ...</span>

<span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">is_authenticated</span><span class="p">:</span>
<span class="c1"># -------------------- new --------------------</span>
<span class="c1"># create a user inbox for private messages</span>
<span class="n">async_to_sync</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">channel_layer</span><span class="o">.</span><span class="n">group_add</span><span class="p">)(</span>
<span class="bp">self</span><span class="o">.</span><span class="n">user_inbox</span><span class="p">,</span>
<span class="bp">self</span><span class="o">.</span><span class="n">channel_name</span><span class="p">,</span>
<span class="p">)</span>
<span class="c1"># ---------------- end of new ----------------</span>
<span class="c1"># ...</span>

<span class="k">def</span> <span class="nf">disconnect</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">close_code</span><span class="p">):</span>
<span class="c1"># ...</span>

<span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">is_authenticated</span><span class="p">:</span>
<span class="c1"># -------------------- new --------------------</span>
<span class="c1"># delete the user inbox for private messages</span>
<span class="n">async_to_sync</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">channel_layer</span><span class="o">.</span><span class="n">group_add</span><span class="p">)(</span>
<span class="bp">self</span><span class="o">.</span><span class="n">user_inbox</span><span class="p">,</span>
<span class="bp">self</span><span class="o">.</span><span class="n">channel_name</span><span class="p">,</span>
<span class="p">)</span>
<span class="c1"># ---------------- end of new ----------------</span>
<span class="c1"># ...</span>
</code></pre>
<p>So, we:</p>
<ol>
<li>Added <code>user_inbox</code> to <code>ChatConsumer</code> and initialized it on <code>connect()</code>.</li>
<li>Added the user to the <code>user_inbox</code> group when they connect.</li>
<li>Removed the user from the <code>user_inbox</code> group when they disconnect.</li>
</ol>
<li>Added <code>user_inbox</code> to <code>ChatConsumer</code> and initialized it on <code>connect()</code>.</li>
<li>Added the user to the <code>user_inbox</code> group when they connect.</li>
<li>Removed the user from the <code>user_inbox</code> group when they disconnect.</li>
<p>Next, modify <code>receive()</code> to handle private messages:</p>
<pre><span></span><code><span class="c1"># chat/consumers.py</span>

<span class="k">def</span> <span class="nf">receive</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">text_data</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">bytes_data</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
<span class="n">text_data_json</span> <span class="o">=</span> <span class="n">json</span><span class="o">.</span><span class="n">loads</span><span class="p">(</span><span class="n">text_data</span><span class="p">)</span>
<span class="n">message</span> <span class="o">=</span> <span class="n">text_data_json</span><span class="p">[</span><span class="s1">'message'</span><span class="p">]</span>

<span class="k">if</span> <span class="ow">not</span> <span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">is_authenticated</span><span class="p">:</span>
<span class="k">return</span>

<span class="c1"># -------------------- new --------------------</span>
<span class="k">if</span> <span class="n">message</span><span class="o">.</span><span class="n">startswith</span><span class="p">(</span><span class="s1">'/pm '</span><span class="p">):</span>
<span class="n">split</span> <span class="o">=</span> <span class="n">message</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s1">' '</span><span class="p">,</span> <span class="mi">2</span><span class="p">)</span>
<span class="n">target</span> <span class="o">=</span> <span class="n">split</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span>
<span class="n">target_msg</span> <span class="o">=</span> <span class="n">split</span><span class="p">[</span><span class="mi">2</span><span class="p">]</span>

<span class="c1"># send private message to the target</span>
<span class="n">async_to_sync</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">channel_layer</span><span class="o">.</span><span class="n">group_send</span><span class="p">)(</span>
<span class="sa">f</span><span class="s1">'inbox_</span><span class="si">{</span><span class="n">target</span><span class="si">}</span><span class="s1">'</span><span class="p">,</span>
<span class="p">{</span>
<span class="s1">'type'</span><span class="p">:</span> <span class="s1">'private_message'</span><span class="p">,</span>
<span class="s1">'user'</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">username</span><span class="p">,</span>
<span class="s1">'message'</span><span class="p">:</span> <span class="n">target_msg</span><span class="p">,</span>
<span class="p">}</span>
<span class="p">)</span>
<span class="c1"># send private message delivered to the user</span>
<span class="bp">self</span><span class="o">.</span><span class="n">send</span><span class="p">(</span><span class="n">json</span><span class="o">.</span><span class="n">dumps</span><span class="p">({</span>
<span class="s1">'type'</span><span class="p">:</span> <span class="s1">'private_message_delivered'</span><span class="p">,</span>
<span class="s1">'target'</span><span class="p">:</span> <span class="n">target</span><span class="p">,</span>
<span class="s1">'message'</span><span class="p">:</span> <span class="n">target_msg</span><span class="p">,</span>
<span class="p">}))</span>
<span class="k">return</span>
<span class="c1"># ---------------- end of new ----------------</span>

<span class="c1"># send chat message event to the room</span>
<span class="n">async_to_sync</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">channel_layer</span><span class="o">.</span><span class="n">group_send</span><span class="p">)(</span>
<span class="bp">self</span><span class="o">.</span><span class="n">room_group_name</span><span class="p">,</span>
<span class="p">{</span>
<span class="s1">'type'</span><span class="p">:</span> <span class="s1">'chat_message'</span><span class="p">,</span>
<span class="s1">'user'</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="o">.</span><span class="n">username</span><span class="p">,</span>
<span class="s1">'message'</span><span class="p">:</span> <span class="n">message</span><span class="p">,</span>
<span class="p">}</span>
<span class="p">)</span>
<span class="n">Message</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">create</span><span class="p">(</span><span class="n">user</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">user</span><span class="p">,</span> <span class="n">room</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">room</span><span class="p">,</span> <span class="n">content</span><span class="o">=</span><span class="n">message</span><span class="p">)</span>
</code></pre>
<p>Add the following methods at the end of <em>chat/consumers.py</em>:</p>
<pre><span></span><code><span class="c1"># chat/consumers.py</span>

<span class="k">def</span> <span class="nf">private_message</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">event</span><span class="p">):</span>
<span class="bp">self</span><span class="o">.</span><span class="n">send</span><span class="p">(</span><span class="n">text_data</span><span class="o">=</span><span class="n">json</span><span class="o">.</span><span class="n">dumps</span><span class="p">(</span><span class="n">event</span><span class="p">))</span>

<span class="k">def</span> <span class="nf">private_message_delivered</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">event</span><span class="p">):</span>
<span class="bp">self</span><span class="o">.</span><span class="n">send</span><span class="p">(</span><span class="n">text_data</span><span class="o">=</span><span class="n">json</span><span class="o">.</span><span class="n">dumps</span><span class="p">(</span><span class="n">event</span><span class="p">))</span>
</code></pre>
<p>Your final <em>chat/consumers.py</em> file should be equal to this one: <a href="https://gist.github.com/duplxey/3efe783a9c4b7c12e9211c07063a3492">consumers.py</a></p>
<h3 id="frontend_2">Frontend</h3>
<p>To handle private messages in the frontend, add <code>private_message</code> and <code>private_message_delivered</code> cases inside the <code>switch(data.type)</code> statement:</p>
<pre><span></span><code><span class="c1">// chat/static/room.js</span>

<span class="k">switch</span> <span class="p">(</span><span class="nx">data</span><span class="p">.</span><span class="nx">type</span><span class="p">)</span> <span class="p">{</span>
<span class="c1">// ...</span>
<span class="k">case</span> <span class="s2">"private_message"</span><span class="o">:</span>
<span class="nx">chatLog</span><span class="p">.</span><span class="nx">value</span> <span class="o">+=</span> <span class="s2">"PM from "</span> <span class="o">+</span> <span class="nx">data</span><span class="p">.</span><span class="nx">user</span> <span class="o">+</span> <span class="s2">": "</span> <span class="o">+</span> <span class="nx">data</span><span class="p">.</span><span class="nx">message</span> <span class="o">+</span> <span class="s2">"\n"</span><span class="p">;</span>
<span class="k">break</span><span class="p">;</span>
<span class="k">case</span> <span class="s2">"private_message_delivered"</span><span class="o">:</span>
<span class="nx">chatLog</span><span class="p">.</span><span class="nx">value</span> <span class="o">+=</span> <span class="s2">"PM to "</span> <span class="o">+</span> <span class="nx">data</span><span class="p">.</span><span class="nx">target</span> <span class="o">+</span> <span class="s2">": "</span> <span class="o">+</span> <span class="nx">data</span><span class="p">.</span><span class="nx">message</span> <span class="o">+</span> <span class="s2">"\n"</span><span class="p">;</span>
<span class="k">break</span><span class="p">;</span>
<span class="c1">// ...</span>
<span class="p">}</span>
</code></pre>
<p>To make the chat a bit more convenient, we can change the message input to <code>pm %USERNAME%</code> when the user clicks one of the online users in the <code>onlineUsersSelector</code>. Add the following handler to the bottom:</p>
<pre><span></span><code><span class="c1">// chat/static/room.js</span>

<span class="nx">onlineUsersSelector</span><span class="p">.</span><span class="nx">onchange</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
<span class="nx">chatMessageInput</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="s2">"/pm "</span> <span class="o">+</span> <span class="nx">onlineUsersSelector</span><span class="p">.</span><span class="nx">value</span> <span class="o">+</span> <span class="s2">" "</span><span class="p">;</span>
<span class="nx">onlineUsersSelector</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="kc">null</span><span class="p">;</span>
<span class="nx">chatMessageInput</span><span class="p">.</span><span class="nx">focus</span><span class="p">();</span>
<span class="p">};</span>
</code></pre>
<h3 id="testing_3">Testing</h3>

<p>Create two superusers for testing, and then run the server.</p>
<p>Open two different private/incognito browsers, logging into both at <a href="http://localhost:8000/admin">http://localhost:8000/admin</a>.</p>
<p>Then navigate to <a href="http://localhost:8000/chat/default">http://localhost:8000/chat/default</a> in both browsers. Click on one of the connected users to send them a private message:</p>

