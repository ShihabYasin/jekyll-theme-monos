---
layout: post
title: Sending Confirmation Emails with Flask, Redis Queue, and Amazon SES
date: 2019-04-12 16:20:23 +0900
category: AWS
tag: AWS
---


<h1>Sending Confirmation Emails with Flask, Redis Queue, and Amazon SES</h1>

<h2 id="project-setup">Project Setup</h2>

<p>Quickly review the code and overall project structure:</p>
<pre><span></span><code>├── Dockerfile
├── docker-compose.yml
├── manage.py
├── project
│   ├── __init__.py
│   ├── client
│   │   ├── static
│   │   │   ├── main.css
│   │   │   └── main.js
│   │   └── templates
│   │       ├── _base.html
│   │       ├── footer.html
│   │       └── home.html
│   ├── db
│   │   ├── Dockerfile
│   │   └── create.sql
│   ├── server
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── main
│   │   │   ├── __init__.py
│   │   │   ├── forms.py
│   │   │   └── views.py
│   │   └── models.py
│   └── tests
│       ├── __init__.py
│       ├── base.py
│       ├── helpers.py
│       ├── test__config.py
│       └── test_main.py
└── requirements.txt
</code></pre>
<p>Then, spin up the app:</p>
<pre><span></span><code>$ docker-compose up -d --build
</code></pre>
<p>This tutorial uses Docker version 20.10.10.</p>
<p>Create the database tables:</p>
<pre><span></span><code>$ docker-compose run users python manage.py create_db
</code></pre>
<p>Navigate to <a href="http://localhost:5003">http://localhost:5003</a> in your browser. </p>

<pre><span></span><code>$ docker-compose run users python manage.py <span class="nb">test</span>

----------------------------------------------------------------------
Ran <span class="m">8</span> tests <span class="k">in</span> <span class="m">0</span>.225s

OK
</code></pre>
<h2 id="workflow">Workflow</h2>
<p>Here's the workflow we'll be using:</p>
<ol>
<li>A new user submits the registration form, which sends a POST request to the server-side.</li>
<li>Within the Flask view, after a new user is successfully added to the database, a new task is added to the queue and a response is sent back to the end user indicating that they need to confirm their registration via email.</li>
<li>In the background, a worker process picks up the task, generates a unique link, and sends a request to Amazon SES to send the confirmation email.</li>
<li>The end user can then confirm the email, from his or her mailbox, by clicking the unique link.</li>
<li>When the user clicks the link, a GET request is sent to the server-side, which updates the user record in the database.</li>
</ol>
<li>A new user submits the registration form, which sends a POST request to the server-side.</li>
<li>Within the Flask view, after a new user is successfully added to the database, a new task is added to the queue and a response is sent back to the end user indicating that they need to confirm their registration via email.</li>
<li>In the background, a worker process picks up the task, generates a unique link, and sends a request to Amazon SES to send the confirmation email.</li>
<li>The end user can then confirm the email, from his or her mailbox, by clicking the unique link.</li>
<li>When the user clicks the link, a GET request is sent to the server-side, which updates the user record in the database.</li>
<p>If you're trying to incorporate email confirmation into an existing application, the above workflow will vary based on your app's flow. </p>



<h2 id="redis-queue">Redis Queue</h2>
<p>First, let's wire up the task queue!</p>
<h3 id="docker">Docker</h3>
<p>Start by spinning up two new processes: Redis and a worker. Update the <em>docker-compose.yml</em> file like so:</p>
<pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">'3.8'</span><span class="w"></span>

<span class="nt">services</span><span class="p">:</span><span class="w"></span>

<span class="w">  </span><span class="nt">users</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">.</span><span class="w"></span>
<span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">users</span><span class="w"></span>
<span class="w">    </span><span class="nt">container_name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">users</span><span class="w"></span>
<span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">5003:5000</span><span class="w"></span>
<span class="w">    </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">python manage.py run -h 0.0.0.0</span><span class="w"></span>
<span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">.:/usr/src/app</span><span class="w"></span>
<span class="w">    </span><span class="nt">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">FLASK_DEBUG=1</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">APP_SETTINGS=project.server.config.DevelopmentConfig</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">DATABASE_URL=postgresql://postgres:<a class="__cf_email__" data-cfemail="b2c2ddc1c6d5c0d7c1f2c7c1d7c0c19fd6d0" href="/cdn-cgi/l/email-protection">[email protected]</a>:5432/users_dev</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">DATABASE_TEST_URL=postgresql://postgres:<a class="__cf_email__" data-cfemail="4a3a25393e2d382f390a3f392f3839672e28" href="/cdn-cgi/l/email-protection">[email protected]</a>:5432/users_test</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SECRET_KEY=my_precious</span><span class="w"></span>
<span class="w">    </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">users-db</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">redis</span><span class="w"></span>

<span class="w">  </span><span class="nt">users-db</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">container_name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">users-db</span><span class="w"></span>
<span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./project/db</span><span class="w"></span>
<span class="w">      </span><span class="nt">dockerfile</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Dockerfile</span><span class="w"></span>
<span class="w">    </span><span class="nt">expose</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">5432</span><span class="w"></span>
<span class="w">    </span><span class="nt">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">POSTGRES_USER=postgres</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">POSTGRES_PASSWORD=postgres</span><span class="w"></span>

<span class="w">  </span><span class="nt">worker</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">users</span><span class="w"></span>
<span class="w">    </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">python manage.py run_worker</span><span class="w"></span>
<span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">.:/usr/src/app</span><span class="w"></span>
<span class="w">    </span><span class="nt">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">FLASK_DEBUG=1</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">APP_SETTINGS=project.server.config.DevelopmentConfig</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">DATABASE_URL=postgresql://postgres:<a class="__cf_email__" data-cfemail="8bfbe4f8ffecf9eef8cbfef8eef9f8a6efe9" href="/cdn-cgi/l/email-protection">[email protected]</a>:5432/users_dev</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">DATABASE_TEST_URL=postgresql://postgres:<a class="__cf_email__" data-cfemail="7e0e110d0a190c1b0d3e0b0d1b0c0d531a1c" href="/cdn-cgi/l/email-protection">[email protected]</a>:5432/users_test</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SECRET_KEY=my_precious</span><span class="w"></span>
<span class="w">    </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">users-db</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">redis</span><span class="w"></span>

<span class="w">  </span><span class="nt">redis</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">redis:6-alpine</span><span class="w"></span>
</code></pre>
<p>Add the dependencies to <em>requirements.txt</em>:</p>
<pre><span></span><code><span class="nv">redis</span><span class="o">==</span><span class="m">4</span>.0.2
<span class="nv">rq</span><span class="o">==</span><span class="m">1</span>.10.0
</code></pre>
<h3 id="task">Task</h3>
<p>Add a new task to a file called <em>tasks.py</em> in "project/server/main":</p>
<pre><span></span><code><span class="c1"># project/server/main/tasks.py</span>


<span class="kn">import</span> <span class="nn">time</span>

<span class="kn">from</span> <span class="nn">project.server</span> <span class="kn">import</span> <span class="n">db</span>
<span class="kn">from</span> <span class="nn">project.server.models</span> <span class="kn">import</span> <span class="n">User</span>


<span class="k">def</span> <span class="nf">send_email</span><span class="p">(</span><span class="n">email</span><span class="p">):</span>
<span class="n">time</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span>  <span class="c1"># simulate long-running process</span>
<span class="n">user</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">query</span><span class="o">.</span><span class="n">filter_by</span><span class="p">(</span><span class="n">email</span><span class="o">=</span><span class="n">email</span><span class="p">)</span><span class="o">.</span><span class="n">first</span><span class="p">()</span>
<span class="n">user</span><span class="o">.</span><span class="n">email_sent</span> <span class="o">=</span> <span class="kc">True</span>
<span class="n">db</span><span class="o">.</span><span class="n">session</span><span class="o">.</span><span class="n">commit</span><span class="p">()</span>
<span class="k">return</span> <span class="kc">True</span>
</code></pre>
<p>Here, we simulated a long-running process and then updated the <code>email_sent</code> field in the <code>User</code> model to <code>True</code>. We'll replace <code>time.sleep(10)</code> with the actual functionality to send an email shortly.</p>
<p>After <code>email_sent</code> is set to <code>True</code>, the user is technically registered but "unconfirmed". At this point, what is that user allowed to do? In other words, does that user have full access to your app, some form of limited or restricted access, or simply no access at all? Think about how you'd handle this in your app.</p>
<p>Update the view to connect to Redis and enqueue a task:</p>
<pre><span></span><code><span class="nd">@main_blueprint</span><span class="o">.</span><span class="n">route</span><span class="p">(</span><span class="s1">'/'</span><span class="p">,</span> <span class="n">methods</span><span class="o">=</span><span class="p">[</span><span class="s1">'GET'</span><span class="p">,</span> <span class="s1">'POST'</span><span class="p">])</span>
<span class="k">def</span> <span class="nf">home</span><span class="p">():</span>
<span class="n">form</span> <span class="o">=</span> <span class="n">RegisterForm</span><span class="p">(</span><span class="n">request</span><span class="o">.</span><span class="n">form</span><span class="p">)</span>
<span class="k">if</span> <span class="n">request</span><span class="o">.</span><span class="n">method</span> <span class="o">==</span> <span class="s1">'POST'</span><span class="p">:</span>
<span class="k">if</span> <span class="n">form</span><span class="o">.</span><span class="n">validate_on_submit</span><span class="p">():</span>
<span class="k">try</span><span class="p">:</span>
<span class="n">user</span> <span class="o">=</span> <span class="n">User</span><span class="p">(</span><span class="n">email</span><span class="o">=</span><span class="n">form</span><span class="o">.</span><span class="n">email</span><span class="o">.</span><span class="n">data</span><span class="p">)</span>
<span class="n">db</span><span class="o">.</span><span class="n">session</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">user</span><span class="p">)</span>
<span class="n">db</span><span class="o">.</span><span class="n">session</span><span class="o">.</span><span class="n">commit</span><span class="p">()</span>
<span class="n">redis_url</span> <span class="o">=</span> <span class="n">current_app</span><span class="o">.</span><span class="n">config</span><span class="p">[</span><span class="s1">'REDIS_URL'</span><span class="p">]</span>
<span class="k">with</span> <span class="n">Connection</span><span class="p">(</span><span class="n">redis</span><span class="o">.</span><span class="n">from_url</span><span class="p">(</span><span class="n">redis_url</span><span class="p">)):</span>
<span class="n">q</span> <span class="o">=</span> <span class="n">Queue</span><span class="p">()</span>
<span class="n">q</span><span class="o">.</span><span class="n">enqueue</span><span class="p">(</span><span class="n">send_email</span><span class="p">,</span> <span class="n">user</span><span class="o">.</span><span class="n">email</span><span class="p">)</span>
<span class="n">flash</span><span class="p">(</span><span class="s1">'Thank you for registering.'</span><span class="p">,</span> <span class="s1">'success'</span><span class="p">)</span>
<span class="k">return</span> <span class="n">redirect</span><span class="p">(</span><span class="n">url_for</span><span class="p">(</span><span class="s2">"main.home"</span><span class="p">))</span>
<span class="k">except</span> <span class="n">IntegrityError</span><span class="p">:</span>
<span class="n">db</span><span class="o">.</span><span class="n">session</span><span class="o">.</span><span class="n">rollback</span><span class="p">()</span>
<span class="n">flash</span><span class="p">(</span><span class="s1">'Sorry. That email already exists.'</span><span class="p">,</span> <span class="s1">'danger'</span><span class="p">)</span>
<span class="n">users</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">query</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>
<span class="k">return</span> <span class="n">render_template</span><span class="p">(</span><span class="s1">'home.html'</span><span class="p">,</span> <span class="n">form</span><span class="o">=</span><span class="n">form</span><span class="p">,</span> <span class="n">users</span><span class="o">=</span><span class="n">users</span><span class="p">)</span>
</code></pre>
<p>Update the imports:</p>
<pre><span></span><code><span class="kn">import</span> <span class="nn">redis</span>
<span class="kn">from</span> <span class="nn">flask</span> <span class="kn">import</span> <span class="n">render_template</span><span class="p">,</span> <span class="n">Blueprint</span><span class="p">,</span> <span class="n">url_for</span><span class="p">,</span> \
<span class="n">redirect</span><span class="p">,</span> <span class="n">flash</span><span class="p">,</span> <span class="n">request</span><span class="p">,</span> <span class="n">current_app</span>
<span class="kn">from</span> <span class="nn">rq</span> <span class="kn">import</span> <span class="n">Queue</span><span class="p">,</span> <span class="n">Connection</span>
<span class="kn">from</span> <span class="nn">sqlalchemy.exc</span> <span class="kn">import</span> <span class="n">IntegrityError</span>

<span class="kn">from</span> <span class="nn">project.server</span> <span class="kn">import</span> <span class="n">db</span>
<span class="kn">from</span> <span class="nn">project.server.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">project.server.main.forms</span> <span class="kn">import</span> <span class="n">RegisterForm</span>
<span class="kn">from</span> <span class="nn">project.server.main.tasks</span> <span class="kn">import</span> <span class="n">send_email</span>
</code></pre>
<p>Add the config to the <code>BaseConfig</code> in <em>project/server/config.py</em>:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">BaseConfig</span><span class="p">(</span><span class="nb">object</span><span class="p">):</span>
<span class="sd">"""Base configuration."""</span>
<span class="n">SECRET_KEY</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">'SECRET_KEY'</span><span class="p">)</span>
<span class="n">SQLALCHEMY_TRACK_MODIFICATIONS</span> <span class="o">=</span> <span class="kc">False</span>
<span class="n">WTF_CSRF_ENABLED</span> <span class="o">=</span> <span class="kc">False</span>
<span class="n">REDIS_URL</span> <span class="o">=</span> <span class="s1">'redis://redis:6379/0'</span>
<span class="n">QUEUES</span> <span class="o">=</span> <span class="p">[</span><span class="s1">'default'</span><span class="p">]</span>
</code></pre>
<p>Note that we referenced the <code>redis</code> service in the <code>REDIS_URL</code>, defined in <em>docker-compose.yml</em>, rather than <code>localhost</code>. Review the Docker Compose <a href="https://docs.docker.com/compose/networking/">docs</a> for more info on connecting to other services via the hostname alias.</p>
<h3 id="worker">Worker</h3>
<p>Next, let's add a custom CLI command to <em>manage.py</em> to fire the worker process, which is used to process the task we added to the queue:</p>
<pre><span></span><code><span class="nd">@cli</span><span class="o">.</span><span class="n">command</span><span class="p">(</span><span class="s1">'run_worker'</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">run_worker</span><span class="p">():</span>
<span class="n">redis_url</span> <span class="o">=</span> <span class="n">app</span><span class="o">.</span><span class="n">config</span><span class="p">[</span><span class="s1">'REDIS_URL'</span><span class="p">]</span>
<span class="n">redis_connection</span> <span class="o">=</span> <span class="n">redis</span><span class="o">.</span><span class="n">from_url</span><span class="p">(</span><span class="n">redis_url</span><span class="p">)</span>
<span class="k">with</span> <span class="n">Connection</span><span class="p">(</span><span class="n">redis_connection</span><span class="p">):</span>
<span class="n">worker</span> <span class="o">=</span> <span class="n">Worker</span><span class="p">(</span><span class="n">app</span><span class="o">.</span><span class="n">config</span><span class="p">[</span><span class="s1">'QUEUES'</span><span class="p">])</span>
<span class="n">worker</span><span class="o">.</span><span class="n">work</span><span class="p">()</span>
</code></pre>
<p>Don't forget the imports:</p>
<pre><span></span><code><span class="kn">import</span> <span class="nn">redis</span>
<span class="kn">from</span> <span class="nn">rq</span> <span class="kn">import</span> <span class="n">Connection</span><span class="p">,</span> <span class="n">Worker</span>
</code></pre>
<h3 id="test">Test</h3>
<p>Spin up the new containers:</p>
<pre><span></span><code>$ docker-compose up -d --build
</code></pre>
<p>To trigger a new task, register a new user. <code>Confirm Email Sent?</code> should be <code>False</code>:</p>

<p>Then, refresh the page after ten seconds. <code>Confirm Email Sent?</code> should now be <code>True</code> since the task finished and the database was updated.</p>

<h2 id="email-confirmation">Email Confirmation</h2>
<p>Moving right along, let's add the logic for confirming an email address, starting with the template.</p>
<h3 id="email-template">Email template</h3>
<p>We can use <a href="http://jinja.pocoo.org/">Jinja</a> to generate the template on the server.</p>
<pre><span></span><code><span class="x">Thanks for signing up. Please follow the link to activate your account.</span>
<span class="cp">{{</span> <span class="nv">confirm_url</span> <span class="cp">}}</span><span class="x"></span>

<span class="x">Cheers!</span>
</code></pre>
<p>Save the above text to a new file called <em>email.txt</em> in "project/client/templates".</p>
<p>For now, we'll just be sending a plain-text email. Feel free to add HTML (basic and/or rich) on your own.</p>
<h3 id="unique-url">Unique URL</h3>
<p>Next, let's add a few helper functions to encode and decode a token, which will set the base for generating a unique confirmation URL.</p>
<p>Add a new file called <em>utils.py</em> to "project/server/main":</p>
<pre><span></span><code><span class="c1"># project/server/main/utils.py</span>


<span class="kn">from</span> <span class="nn">itsdangerous</span> <span class="kn">import</span> <span class="n">URLSafeTimedSerializer</span>
<span class="kn">from</span> <span class="nn">flask</span> <span class="kn">import</span> <span class="n">current_app</span><span class="p">,</span> <span class="n">url_for</span>


<span class="k">def</span> <span class="nf">encode_token</span><span class="p">(</span><span class="n">email</span><span class="p">):</span>
<span class="n">serializer</span> <span class="o">=</span> <span class="n">URLSafeTimedSerializer</span><span class="p">(</span><span class="n">current_app</span><span class="o">.</span><span class="n">config</span><span class="p">[</span><span class="s1">'SECRET_KEY'</span><span class="p">])</span>
<span class="k">return</span> <span class="n">serializer</span><span class="o">.</span><span class="n">dumps</span><span class="p">(</span><span class="n">email</span><span class="p">,</span> <span class="n">salt</span><span class="o">=</span><span class="s1">'email-confirm-salt'</span><span class="p">)</span>


<span class="k">def</span> <span class="nf">decode_token</span><span class="p">(</span><span class="n">token</span><span class="p">,</span> <span class="n">expiration</span><span class="o">=</span><span class="mi">3600</span><span class="p">):</span>
<span class="n">serializer</span> <span class="o">=</span> <span class="n">URLSafeTimedSerializer</span><span class="p">(</span><span class="n">current_app</span><span class="o">.</span><span class="n">config</span><span class="p">[</span><span class="s1">'SECRET_KEY'</span><span class="p">])</span>
<span class="k">try</span><span class="p">:</span>
<span class="n">email</span> <span class="o">=</span> <span class="n">serializer</span><span class="o">.</span><span class="n">loads</span><span class="p">(</span>
<span class="n">token</span><span class="p">,</span>
<span class="n">salt</span><span class="o">=</span><span class="s1">'email-confirm-salt'</span><span class="p">,</span>
<span class="n">max_age</span><span class="o">=</span><span class="n">expiration</span>
<span class="p">)</span>
<span class="k">return</span> <span class="n">email</span>
<span class="k">except</span> <span class="ne">Exception</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span>
<span class="k">return</span> <span class="kc">False</span>

<span class="k">def</span> <span class="nf">generate_url</span><span class="p">(</span><span class="n">endpoint</span><span class="p">,</span> <span class="n">token</span><span class="p">):</span>
<span class="k">return</span> <span class="n">url_for</span><span class="p">(</span><span class="n">endpoint</span><span class="p">,</span> <span class="n">token</span><span class="o">=</span><span class="n">token</span><span class="p">,</span> <span class="n">_external</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
</code></pre>
<p>What's happening here?</p>
<ol>
<li><code>encode_token</code> utilizes the <code>URLSafeTimedSerializer</code> class from the <a href="https://itsdangerous.palletsprojects.com/">itsdangerous</a> package to encode the email address and a timestamp in a token.</li>
<li><code>decode_token</code> then decodes the token and returns the email address as long as the token is not older than 3600 seconds (one hour).</li>
<li><code>generate_url</code> takes an endpoint and an encoded token and then returns a unique URL. (Yes, this is a single-line function! It makes testing much easier.)</li>
</ol>
<li><code>encode_token</code> utilizes the <code>URLSafeTimedSerializer</code> class from the <a href="https://itsdangerous.palletsprojects.com/">itsdangerous</a> package to encode the email address and a timestamp in a token.</li>
<li><code>decode_token</code> then decodes the token and returns the email address as long as the token is not older than 3600 seconds (one hour).</li>
<li><code>generate_url</code> takes an endpoint and an encoded token and then returns a unique URL. (Yes, this is a single-line function! It makes testing much easier.)</li>
<p>Since, by default, <code>url_for</code> creates relative URLs, we set <code>_external</code> to <code>True</code> to generate an absolute URL. If this were created outside the Flask request context you would need to define a <code>SERVER_NAME</code> in the app config <em>and</em> provide access to the application context to use an absolute URL. Once a <code>SERVER_NAME</code> is set, Flask can <em>only</em> serve requests from that domain, though. Review the following <a href="https://github.com/pallets/flask/issues/998">issue</a> for more info.</p>
<p>Let's add a few quick tests to ensure the encoding and decoding of the token along with the unique URL generation work as expected.</p>
<p><em>test_utils.py</em>:</p>
<pre><span></span><code><span class="c1"># project/server/tests/test_utils.py</span>


<span class="kn">import</span> <span class="nn">time</span>
<span class="kn">import</span> <span class="nn">unittest</span>

<span class="kn">from</span> <span class="nn">base</span> <span class="kn">import</span> <span class="n">BaseTestCase</span>
<span class="kn">from</span> <span class="nn">project.server.main.utils</span> <span class="kn">import</span> <span class="n">encode_token</span><span class="p">,</span> <span class="n">decode_token</span><span class="p">,</span> <span class="n">generate_url</span>
<span class="kn">from</span> <span class="nn">project.server.models</span> <span class="kn">import</span> <span class="n">User</span>



<span class="k">class</span> <span class="nc">TestUtils</span><span class="p">(</span><span class="n">BaseTestCase</span><span class="p">):</span>

<span class="k">def</span> <span class="nf">test_verify_token</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="c1"># Ensure encode and decode behave correctly.</span>
<span class="n">token</span> <span class="o">=</span> <span class="n">encode_token</span><span class="p">(</span><span class="s1">'<a class="__cf_email__" data-cfemail="6602130b0b1f26030b070f0a4805090b" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span><span class="p">)</span>
<span class="n">email</span> <span class="o">=</span> <span class="n">decode_token</span><span class="p">(</span><span class="n">token</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertEqual</span><span class="p">(</span><span class="n">email</span><span class="p">,</span> <span class="s1">'<a class="__cf_email__" data-cfemail="badecfd7d7c3fadfd7dbd3d694d9d5d7" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span><span class="p">)</span>

<span class="k">def</span> <span class="nf">test_verify_invalid_token</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="c1"># Ensure encode and decode behave correctly when token is invalid.</span>
<span class="n">token</span> <span class="o">=</span> <span class="s1">'invalid'</span>
<span class="n">email</span> <span class="o">=</span> <span class="n">decode_token</span><span class="p">(</span><span class="n">token</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertEqual</span><span class="p">(</span><span class="n">email</span><span class="p">,</span> <span class="kc">False</span><span class="p">)</span>

<span class="k">def</span> <span class="nf">test_verify_expired_token</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="c1"># Ensure encode and decode behave correctly when token has expired.</span>
<span class="n">token</span> <span class="o">=</span> <span class="n">encode_token</span><span class="p">(</span><span class="s1">'<a class="__cf_email__" data-cfemail="7a1e0f1717033a1f171b131654191517" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span><span class="p">)</span>
<span class="n">time</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
<span class="n">email</span> <span class="o">=</span> <span class="n">decode_token</span><span class="p">(</span><span class="n">token</span><span class="p">,</span> <span class="mi">0</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertEqual</span><span class="p">(</span><span class="n">email</span><span class="p">,</span> <span class="kc">False</span><span class="p">)</span>

<span class="k">def</span> <span class="nf">test_token_is_unique</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="c1"># Ensure tokens are unique.</span>
<span class="n">token1</span> <span class="o">=</span> <span class="n">encode_token</span><span class="p">(</span><span class="s1">'<a class="__cf_email__" data-cfemail="c9adbca4a4b089aca4a8a0a5e7aaa6a4" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span><span class="p">)</span>
<span class="n">token2</span> <span class="o">=</span> <span class="n">encode_token</span><span class="p">(</span><span class="s1">'<a class="__cf_email__" data-cfemail="3d59485050447d58505c54510f135e5250" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertNotEqual</span><span class="p">(</span><span class="n">token1</span><span class="p">,</span> <span class="n">token2</span><span class="p">)</span>

<span class="k">def</span> <span class="nf">test_generate_url</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="c1"># Ensure generate_url behaves as expected.</span>
<span class="n">token</span> <span class="o">=</span> <span class="n">encode_token</span><span class="p">(</span><span class="s1">'<a class="__cf_email__" data-cfemail="e4809189899da48189858d88ca878b89" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span><span class="p">)</span>
<span class="n">url</span> <span class="o">=</span> <span class="n">generate_url</span><span class="p">(</span><span class="s1">'main.home'</span><span class="p">,</span> <span class="n">token</span><span class="p">)</span>
<span class="n">url_token</span> <span class="o">=</span> <span class="n">url</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s1">'='</span><span class="p">)[</span><span class="mi">1</span><span class="p">]</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertEqual</span><span class="p">(</span><span class="n">token</span><span class="p">,</span> <span class="n">url_token</span><span class="p">)</span>
<span class="n">email</span> <span class="o">=</span> <span class="n">decode_token</span><span class="p">(</span><span class="n">url_token</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertEqual</span><span class="p">(</span><span class="n">email</span><span class="p">,</span> <span class="s1">'<a class="__cf_email__" data-cfemail="3155445c5c4871545c50585d1f525e5c" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span><span class="p">)</span>


<span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s1">'__main__'</span><span class="p">:</span>
<span class="n">unittest</span><span class="o">.</span><span class="n">main</span><span class="p">()</span>
</code></pre>
<p>Run the tests:</p>
<pre><span></span><code>$ docker-compose run users python manage.py <span class="nb">test</span>

----------------------------------------------------------------------
Ran <span class="m">13</span> tests <span class="k">in</span> <span class="m">1</span>.305s

OK
</code></pre>
<p>Are we missing any tests? Add them now. How would you mock the test that uses <code>sleep(1)</code>? Check out <a href="https://github.com/spulec/freezegun">FreezeGun</a>!</p>
<p>Next, make a few updates to the view:</p>
<pre><span></span><code><span class="nd">@main_blueprint</span><span class="o">.</span><span class="n">route</span><span class="p">(</span><span class="s1">'/'</span><span class="p">,</span> <span class="n">methods</span><span class="o">=</span><span class="p">[</span><span class="s1">'GET'</span><span class="p">,</span> <span class="s1">'POST'</span><span class="p">])</span>
<span class="k">def</span> <span class="nf">home</span><span class="p">():</span>
<span class="n">form</span> <span class="o">=</span> <span class="n">RegisterForm</span><span class="p">(</span><span class="n">request</span><span class="o">.</span><span class="n">form</span><span class="p">)</span>
<span class="k">if</span> <span class="n">request</span><span class="o">.</span><span class="n">method</span> <span class="o">==</span> <span class="s1">'POST'</span><span class="p">:</span>
<span class="k">if</span> <span class="n">form</span><span class="o">.</span><span class="n">validate_on_submit</span><span class="p">():</span>
<span class="k">try</span><span class="p">:</span>
<span class="c1"># add user to the db</span>
<span class="n">user</span> <span class="o">=</span> <span class="n">User</span><span class="p">(</span><span class="n">email</span><span class="o">=</span><span class="n">form</span><span class="o">.</span><span class="n">email</span><span class="o">.</span><span class="n">data</span><span class="p">)</span>
<span class="n">db</span><span class="o">.</span><span class="n">session</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">user</span><span class="p">)</span>
<span class="n">db</span><span class="o">.</span><span class="n">session</span><span class="o">.</span><span class="n">commit</span><span class="p">()</span>
<span class="c1"># generate token, confirm url, and template</span>
<span class="n">token</span> <span class="o">=</span> <span class="n">encode_token</span><span class="p">(</span><span class="n">user</span><span class="o">.</span><span class="n">email</span><span class="p">)</span>
<span class="n">confirm_url</span> <span class="o">=</span> <span class="n">generate_url</span><span class="p">(</span><span class="s1">'main.confirm_email'</span><span class="p">,</span> <span class="n">token</span><span class="p">)</span>
<span class="n">body</span> <span class="o">=</span> <span class="n">render_template</span><span class="p">(</span><span class="s1">'email.txt'</span><span class="p">,</span> <span class="n">confirm_url</span><span class="o">=</span><span class="n">confirm_url</span><span class="p">)</span>
<span class="c1"># enqueue</span>
<span class="n">redis_url</span> <span class="o">=</span> <span class="n">current_app</span><span class="o">.</span><span class="n">config</span><span class="p">[</span><span class="s1">'REDIS_URL'</span><span class="p">]</span>
<span class="k">with</span> <span class="n">Connection</span><span class="p">(</span><span class="n">redis</span><span class="o">.</span><span class="n">from_url</span><span class="p">(</span><span class="n">redis_url</span><span class="p">)):</span>
<span class="n">q</span> <span class="o">=</span> <span class="n">Queue</span><span class="p">()</span>
<span class="n">q</span><span class="o">.</span><span class="n">enqueue</span><span class="p">(</span><span class="n">send_email</span><span class="p">,</span> <span class="n">user</span><span class="o">.</span><span class="n">email</span><span class="p">,</span> <span class="n">body</span><span class="p">)</span>
<span class="n">flash</span><span class="p">(</span><span class="s1">'Thank you for registering.'</span><span class="p">,</span> <span class="s1">'success'</span><span class="p">)</span>
<span class="k">return</span> <span class="n">redirect</span><span class="p">(</span><span class="n">url_for</span><span class="p">(</span><span class="s2">"main.home"</span><span class="p">))</span>
<span class="k">except</span> <span class="n">IntegrityError</span><span class="p">:</span>
<span class="n">db</span><span class="o">.</span><span class="n">session</span><span class="o">.</span><span class="n">rollback</span><span class="p">()</span>
<span class="n">flash</span><span class="p">(</span><span class="s1">'Sorry. That email already exists.'</span><span class="p">,</span> <span class="s1">'danger'</span><span class="p">)</span>
<span class="n">users</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">query</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>
<span class="k">return</span> <span class="n">render_template</span><span class="p">(</span><span class="s1">'home.html'</span><span class="p">,</span> <span class="n">form</span><span class="o">=</span><span class="n">form</span><span class="p">,</span> <span class="n">users</span><span class="o">=</span><span class="n">users</span><span class="p">)</span>
</code></pre>
<p>Make sure to import <code>encode_token</code> and <code>generate_url</code>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">project.server.main.utils</span> <span class="kn">import</span> <span class="n">encode_token</span><span class="p">,</span> <span class="n">generate_url</span>
</code></pre>
<p>So, after adding the user to the database, we created a token, a unique URL (which we still need to create the view for), and a template.</p>
<p>Finally, add <code>body</code> as a parameter to <code>send_email</code>:</p>
<pre><span></span><code><span class="k">def</span> <span class="nf">send_email</span><span class="p">(</span><span class="n">email</span><span class="p">,</span> <span class="n">body</span><span class="p">):</span>
<span class="n">time</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">10</span><span class="p">)</span>  <span class="c1"># simulate long-running process</span>
<span class="n">user</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">query</span><span class="o">.</span><span class="n">filter_by</span><span class="p">(</span><span class="n">email</span><span class="o">=</span><span class="n">email</span><span class="p">)</span><span class="o">.</span><span class="n">first</span><span class="p">()</span>
<span class="n">user</span><span class="o">.</span><span class="n">email_sent</span> <span class="o">=</span> <span class="kc">True</span>
<span class="n">db</span><span class="o">.</span><span class="n">session</span><span class="o">.</span><span class="n">commit</span><span class="p">()</span>
<span class="k">return</span> <span class="kc">True</span>
</code></pre>
<p>We'll use this shortly.</p>
<h3 id="view">View</h3>
<p>Next, let's add the <code>confirm_email</code> view to process the token and, if appropriate, update the user model:</p>
<pre><span></span><code><span class="nd">@main_blueprint</span><span class="o">.</span><span class="n">route</span><span class="p">(</span><span class="s1">'/confirm/&lt;token&gt;'</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">confirm_email</span><span class="p">(</span><span class="n">token</span><span class="p">):</span>
<span class="n">email</span> <span class="o">=</span> <span class="n">decode_token</span><span class="p">(</span><span class="n">token</span><span class="p">)</span>
<span class="k">if</span> <span class="ow">not</span> <span class="n">email</span><span class="p">:</span>
<span class="n">flash</span><span class="p">(</span><span class="s1">'The confirmation link is invalid or has expired.'</span><span class="p">,</span> <span class="s1">'danger'</span><span class="p">)</span>
<span class="k">return</span> <span class="n">redirect</span><span class="p">(</span><span class="n">url_for</span><span class="p">(</span><span class="s1">'main.home'</span><span class="p">))</span>
<span class="n">user</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">query</span><span class="o">.</span><span class="n">filter_by</span><span class="p">(</span><span class="n">email</span><span class="o">=</span><span class="n">email</span><span class="p">)</span><span class="o">.</span><span class="n">first</span><span class="p">()</span>
<span class="k">if</span> <span class="n">user</span><span class="o">.</span><span class="n">confirmed</span><span class="p">:</span>
<span class="n">flash</span><span class="p">(</span><span class="s1">'Account already confirmed.'</span><span class="p">,</span> <span class="s1">'success'</span><span class="p">)</span>
<span class="k">return</span> <span class="n">redirect</span><span class="p">(</span><span class="n">url_for</span><span class="p">(</span><span class="s1">'main.home'</span><span class="p">))</span>
<span class="n">user</span><span class="o">.</span><span class="n">confirmed</span> <span class="o">=</span> <span class="kc">True</span>
<span class="n">db</span><span class="o">.</span><span class="n">session</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">user</span><span class="p">)</span>
<span class="n">db</span><span class="o">.</span><span class="n">session</span><span class="o">.</span><span class="n">commit</span><span class="p">()</span>
<span class="n">flash</span><span class="p">(</span><span class="s1">'You have confirmed your account. Thanks!'</span><span class="p">,</span> <span class="s1">'success'</span><span class="p">)</span>
<span class="k">return</span> <span class="n">redirect</span><span class="p">(</span><span class="n">url_for</span><span class="p">(</span><span class="s1">'main.home'</span><span class="p">))</span>
</code></pre>
<p>Import <code>decode_token</code>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">project.server.main.utils</span> <span class="kn">import</span> <span class="n">encode_token</span><span class="p">,</span> <span class="n">generate_url</span><span class="p">,</span> <span class="n">decode_token</span>
</code></pre>
<p>So, if the decode is successful, the <code>confirmed</code> field is updated to <code>True</code> for the database record and the user is redirected back to the homepage with a success message.</p>
<h3 id="test_1">Test</h3>
<p>To manually test, first bring down the containers and volumes. Then, spin the containers back up, create the database tables, and open the Docker logs for the <code>worker</code>:</p>
<pre><span></span><code>$ docker-compose down -v
$ docker-compose up -d --build
$ docker-compose run users python manage.py create_db
$ docker-compose logs -f worker
</code></pre>
<p>Then, from the browser, add a new email address. You should see the task start and finish successfully:</p>
<pre><span></span><code><span class="m">21</span>:16:49 default: project.server.main.tasks.send_email<span class="o">(</span>
<span class="s1">'<a class="__cf_email__" data-cfemail="b2dfdbd1dad3d7def2dfdad7c0dfd3dc9cddc0d5" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span>,
<span class="err">'</span>Thanks <span class="k">for</span> signing up. Please follow the link to activate your account.<span class="se">\n</span>h...
<span class="o">)</span> <span class="o">(</span>af8974f4-c4b7-4db1-ba15-7e2bc57ee058<span class="o">)</span>
<span class="m">21</span>:16:59 default: Job OK <span class="o">(</span>af8974f4-c4b7-4db1-ba15-7e2bc57ee058<span class="o">)</span>
<span class="m">21</span>:16:59 Result is kept <span class="k">for</span> <span class="m">500</span> seconds
</code></pre>
<h2 id="amazon-ses">Amazon SES</h2>
<p>First off, why would you want to use a transactional email service (like <a href="https://aws.amazon.com/ses/">Amazon SES</a>, <a href="https://mailchimp.com/features/transactional-email/">Mailchimp Transactional Email</a> (formerly Mandrill), or <a href="https://www.mailgun.com/">Mailgun</a>) over Gmail or your own email server?</p>
<ol>
<li><em>Rate limiting</em>: Email service providers -- e.g., Gmail, Yahoo, Outlook -- have hourly or daily email sending limits. Transactional email service providers have limits as well, but they are much, much higher.</li>
<li><em>Deliverability</em>: Most email service providers do not allow messages from unknown IP addresses. Such emails are marked as spam and generally don't reach the inbox. So if you're sending transactional emails from your own email server, on a shared server, those emails will most likely never be seen by your users. Transactional email services set up relationships with internet service providers and email service providers to ensure that emails are delivered smoothly and promptly.</li>
<li><em>Analytics</em>: Transactional email services provide detailed statistics and analytics to help you improve email open and click rates.</li>
</ol>
<li><em>Rate limiting</em>: Email service providers -- e.g., Gmail, Yahoo, Outlook -- have hourly or daily email sending limits. Transactional email service providers have limits as well, but they are much, much higher.</li>
<li><em>Deliverability</em>: Most email service providers do not allow messages from unknown IP addresses. Such emails are marked as spam and generally don't reach the inbox. So if you're sending transactional emails from your own email server, on a shared server, those emails will most likely never be seen by your users. Transactional email services set up relationships with internet service providers and email service providers to ensure that emails are delivered smoothly and promptly.</li>
<li><em>Analytics</em>: Transactional email services provide detailed statistics and analytics to help you improve email open and click rates.</li>
<p><a href="https://aws.amazon.com/ses/">Amazon SES</a> is a cost-effective email service designed for sending both bulk and transactional emails. Emails can be sent directly from the SES console, via the Simple Mail Transfer Protocol (SMTP) interface, or through the API.</p>
<p>In this tutorial, we'll use <a href="https://github.com/boto/boto3">Boto3</a>, a Python-based AWS SDK, to make calls to the API.</p>
<h3 id="setup">Setup</h3>
<p><a href="https://docs.aws.amazon.com/ses/latest/DeveloperGuide/sign-up-for-aws.html">Sign up</a> for an AWS account if you don’t already have one.</p>
<p>Before you can send emails with SES, you must first <a href="https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html">verify</a> that you own the email address that you wish to send from. Navigate to <a href="https://console.aws.amazon.com/ses">Amazon SES</a>, click "Verified identities" in the sidebar, and then click the "Create identity" button.</p>

<p>To help prevent fraud, new accounts are automatically placed in a sandbox mode where you can only send emails to addresses that you have personally verified with Amazon. Fortunately, this is enough for us to wire everything together.</p>
<p>You must make a request to Amazon to move out of the sandbox mode. This can take a day or two, so get this started as soon as possible. Review <a href="https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html">Moving Out of the Amazon SES Sandbox</a> for more on this.</p>
<h3 id="email">Email</h3>
<p>Back in the code, add <code>boto3</code> to the requirements file:</p>
<pre><span></span><code><span class="nv">boto3</span><span class="o">==</span><span class="m">1</span>.20.11
</code></pre>
<p>Update <code>send_email</code>:</p>
<pre><span></span><code><span class="k">def</span> <span class="nf">send_email</span><span class="p">(</span><span class="n">email</span><span class="p">,</span> <span class="n">body</span><span class="p">):</span>
<span class="c1"># time.sleep(10)  # simulate long-running process</span>
<span class="n">ses</span> <span class="o">=</span> <span class="n">boto3</span><span class="o">.</span><span class="n">client</span><span class="p">(</span>
<span class="s1">'ses'</span><span class="p">,</span>
<span class="n">region_name</span><span class="o">=</span><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'SES_REGION'</span><span class="p">),</span>
<span class="n">aws_access_key_id</span><span class="o">=</span><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'AWS_ACCESS_KEY_ID'</span><span class="p">),</span>
<span class="n">aws_secret_access_key</span><span class="o">=</span><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'AWS_SECRET_ACCESS_KEY'</span><span class="p">)</span>
<span class="p">)</span>
<span class="n">ses</span><span class="o">.</span><span class="n">send_email</span><span class="p">(</span>
<span class="n">Source</span><span class="o">=</span><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'SES_EMAIL_SOURCE'</span><span class="p">),</span>
<span class="n">Destination</span><span class="o">=</span><span class="p">{</span><span class="s1">'ToAddresses'</span><span class="p">:</span> <span class="p">[</span><span class="n">email</span><span class="p">]},</span>
<span class="n">Message</span><span class="o">=</span><span class="p">{</span>
<span class="s1">'Subject'</span><span class="p">:</span> <span class="p">{</span><span class="s1">'Data'</span><span class="p">:</span> <span class="s1">'Confirm Your Account'</span><span class="p">},</span>
<span class="s1">'Body'</span><span class="p">:</span> <span class="p">{</span>
<span class="s1">'Text'</span><span class="p">:</span> <span class="p">{</span><span class="s1">'Data'</span><span class="p">:</span> <span class="n">body</span><span class="p">}</span>
<span class="p">}</span>
<span class="p">}</span>
<span class="p">)</span>
<span class="n">user</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">query</span><span class="o">.</span><span class="n">filter_by</span><span class="p">(</span><span class="n">email</span><span class="o">=</span><span class="n">email</span><span class="p">)</span><span class="o">.</span><span class="n">first</span><span class="p">()</span>
<span class="n">user</span><span class="o">.</span><span class="n">email_sent</span> <span class="o">=</span> <span class="kc">True</span>
<span class="n">db</span><span class="o">.</span><span class="n">session</span><span class="o">.</span><span class="n">commit</span><span class="p">()</span>
<span class="k">return</span> <span class="kc">True</span>
</code></pre>
<p>Here, we created a new SES client resource and then attempted to send an email.</p>
<p>Import <code>os</code> and <code>boto3</code>:</p>
<pre><span></span><code><span class="kn">import</span> <span class="nn">os</span>
<span class="kn">import</span> <span class="nn">boto3</span>
</code></pre>
<p>Update the environment variables for the <code>worker</code> in <em>docker-compose.yml</em>, making sure to update the values:</p>
<pre><span></span><code><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SES_REGION=us-east-2</span><span class="w"></span>
<span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SES_EMAIL_SOURCE=your_email</span><span class="w"></span>
<span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">AWS_ACCESS_KEY_ID=your_access_key_id</span><span class="w"></span>
<span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">AWS_SECRET_ACCESS_KEY=your_secret_access_key</span><span class="w"></span>
</code></pre>
<p>It's worth noting that by default, <code>Boto3</code> will check the <code>AWS_ACCESS_KEY_ID</code> and <code>AWS_SECRET_ACCESS_KEY</code> environment variables for credentials. So, we didn't need to explicitly pass them in when creating the SES client resource. In other words, as long as those environment variables are defined, we can simplify the code:
</p>
<pre><span></span><span class="n">ses</span> <span class="o">=</span> <span class="n">boto3</span><span class="o">.</span><span class="n">client</span><span class="p">(</span><span class="s1">'ses'</span><span class="p">,</span> <span class="n">region_name</span><span class="o">=</span><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'SES_REGION'</span><span class="p">))</span>
</pre>
<p>For more on this, review the official Boto3 <a href="https://boto3.readthedocs.io/en/latest/guide/configuration.html">docs</a>.</p>
<h3 id="test_2">Test</h3>
<p>Update the containers:</p>
<pre><span></span><code>$ docker-compose up -d --build
</code></pre>
<p>Then, register a user from the browser, making sure to use the same email that you used with SES. You should see a confirmation email in your inbox. Click the link and you should be redirected back to <a href="http://localhost:5003">http://localhost:5003</a>.</p>

<p>Remember: If you're still in sandbox mode, you can only send emails to verified addresses. If you try to send an email to an unverified address, the task will fail:</p>
<pre><span></span><code>raise error_class<span class="o">(</span>parsed_response, operation_name<span class="o">)</span>
botocore.errorfactory.MessageRejected: An error occurred <span class="o">(</span>MessageRejected<span class="o">)</span> when calling the SendEmail operation:
Email address is not verified. The following identities failed the check <span class="k">in</span> region US-EAST-2: <a class="__cf_email__" data-cfemail="0266676f6d42777167702c616d6f" href="/cdn-cgi/l/email-protection">[email protected]</a>
</code></pre>
<p>Also, since you're probably testing with a single email address, you may want to remove the unique constraint on the model. Otherwise, you will need to remove the user from the database between tests.</p>
<pre><span></span><code><span class="n">email</span> <span class="o">=</span> <span class="n">db</span><span class="o">.</span><span class="n">Column</span><span class="p">(</span><span class="n">db</span><span class="o">.</span><span class="n">String</span><span class="p">(</span><span class="mi">255</span><span class="p">),</span> <span class="n">unique</span><span class="o">=</span><span class="kc">False</span><span class="p">,</span> <span class="n">nullable</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</code></pre>
<p>While the unique constraint is <code>False</code>, you may also want to ensure the following code from the <code>confirm_email</code> view works:</p>
<pre><span></span><code><span class="k">if</span> <span class="n">user</span><span class="o">.</span><span class="n">confirmed</span><span class="p">:</span>
<span class="n">flash</span><span class="p">(</span><span class="s1">'Account already confirmed.'</span><span class="p">,</span> <span class="s1">'success'</span><span class="p">)</span>
<span class="k">return</span> <span class="n">redirect</span><span class="p">(</span><span class="n">url_for</span><span class="p">(</span><span class="s1">'main.home'</span><span class="p">))</span>
</code></pre>

