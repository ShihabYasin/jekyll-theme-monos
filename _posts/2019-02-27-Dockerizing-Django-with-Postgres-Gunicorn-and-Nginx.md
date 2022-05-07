---
layout: post
title: Dockerizing-Django-with-Postgres-Gunicorn-and-Nginx
date: 2019-02-27 16:20:23 +0900
category: Python
tag: Python
---

<main>
  <div class="container blog-container" style="padding-top: 0;">
    <div class="row">

  <div class="blog-content long-content" data-local-nav-source>
    <p>Configure Django to run on Docker with Postgres. For production environments, we'll add on Nginx and Gunicorn. We'll also take a look at how to serve Django static and media files via Nginx.</p>
<p><em>Dependencies</em>:</p>
<ol>
<li>Django v3.2.6</li>
<li>Docker v20.10.8</li>
<li>Python v3.9.6</li>
</ol>


</div>
<h2 id="project-setup">Project Setup</h2>
<p>Create a new project directory along with a new Django project:</p>
<div class="codehilite"><pre><span></span><code>$ mkdir django-on-docker <span class="o">&amp;&amp;</span> <span class="nb">cd</span> django-on-docker
$ mkdir app <span class="o">&amp;&amp;</span> <span class="nb">cd</span> app
$ python3.9 -m venv env
$ <span class="nb">source</span> env/bin/activate
<span class="o">(</span>env<span class="o">)</span>$

<span class="o">(</span>env<span class="o">)</span>$ pip install <span class="nv">django</span><span class="o">==</span><span class="m">3</span>.2.6
<span class="o">(</span>env<span class="o">)</span>$ django-admin.py startproject hello_django .
<span class="o">(</span>env<span class="o">)</span>$ python manage.py migrate
<span class="o">(</span>env<span class="o">)</span>$ python manage.py runserver
</code></pre></div>


<p>Navigate to <a href="http://localhost:8000/">http://localhost:8000/</a> to view the Django welcome screen. Kill the server once done. Then, exit from and remove the virtual environment. We now have a simple Django project to work with.</p>
<p>Create a <em>requirements.txt</em> file in the "app" directory and add Django as a dependency:</p>
<div class="codehilite"><pre><span></span><code>Django==3.2.6
</code></pre></div>

<p>Since we'll be moving to Postgres, go ahead and remove the <em>db.sqlite3</em> file from the "app" directory.</p>
<p>Your project directory should look like:</p>
<div class="codehilite"><pre><span></span><code>└── app
    ├── hello_django
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py
    └── requirements.txt
</code></pre></div>

<h2 id="docker">Docker</h2>
<p>Install <a href="https://docs.docker.com/install/">Docker</a>, if you don't already have it, then add a <em>Dockerfile</em> to the "app" directory:</p>
<div class="codehilite"><pre><span></span><code><span class="c"># pull official base image</span>
<span class="k">FROM</span><span class="w"> </span><span class="s">python:3.9.6-alpine</span>

<span class="c"># set work directory</span>
<span class="k">WORKDIR</span><span class="w"> </span><span class="s">/usr/src/app</span>

<span class="c"># set environment variables</span>
<span class="k">ENV</span><span class="w"> </span>PYTHONDONTWRITEBYTECODE <span class="m">1</span>
<span class="k">ENV</span><span class="w"> </span>PYTHONUNBUFFERED <span class="m">1</span>

<span class="c"># install dependencies</span>
<span class="k">RUN</span><span class="w"> </span>pip install --upgrade pip
<span class="k">COPY</span><span class="w"> </span>./requirements.txt .
<span class="k">RUN</span><span class="w"> </span>pip install -r requirements.txt

<span class="c"># copy project</span>
<span class="k">COPY</span><span class="w"> </span>. .
</code></pre></div>

<p>So, we started with an <a href="https://github.com/gliderlabs/docker-alpine">Alpine</a>-based <a href="https://hub.docker.com/_/python/">Docker image</a> for Python 3.9.6. We then set a <a href="https://docs.docker.com/engine/reference/builder/#workdir">working directory</a> along with two environment variables:</p>
<ol>
<li><code>PYTHONDONTWRITEBYTECODE</code>: Prevents Python from writing pyc files to disc (equivalent to <code>python -B</code> <a href="https://docs.python.org/3/using/cmdline.html#id1">option</a>)</li>
<li><code>PYTHONUNBUFFERED</code>: Prevents Python from buffering stdout and stderr (equivalent to <code>python -u</code> <a href="https://docs.python.org/3/using/cmdline.html#cmdoption-u">option</a>)</li>
</ol>
<p>Finally, we updated Pip, copied over the <em>requirements.txt</em> file, installed the dependencies, and copied over the Django project itself.</p>

<p>Next, add a <em>docker-compose.yml</em> file to the project root:</p>
<div class="codehilite"><pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">&#39;3.8&#39;</span><span class="w"></span>

<span class="nt">services</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">web</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./app</span><span class="w"></span>
<span class="w">    </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">python manage.py runserver 0.0.0.0:8000</span><span class="w"></span>
<span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./app/:/usr/src/app/</span><span class="w"></span>
<span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">8000:8000</span><span class="w"></span>
<span class="w">    </span><span class="nt">env_file</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./.env.dev</span><span class="w"></span>
</code></pre></div>


<p>Update the <code>SECRET_KEY</code>, <code>DEBUG</code>, and <code>ALLOWED_HOSTS</code> variables in <em>settings.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="n">SECRET_KEY</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;SECRET_KEY&quot;</span><span class="p">)</span>

<span class="n">DEBUG</span> <span class="o">=</span> <span class="nb">int</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;DEBUG&quot;</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="mi">0</span><span class="p">))</span>

<span class="c1"># &#39;DJANGO_ALLOWED_HOSTS&#39; should be a single string of hosts with a space between each.</span>
<span class="c1"># For example: &#39;DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]&#39;</span>
<span class="n">ALLOWED_HOSTS</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;DJANGO_ALLOWED_HOSTS&quot;</span><span class="p">)</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s2">&quot; &quot;</span><span class="p">)</span>
</code></pre></div>

<p>Make sure to add the import to the top:</p>
<div class="codehilite"><pre><span></span><code><span class="kn">import</span> <span class="nn">os</span>
</code></pre></div>

<p>Then, create a <em>.env.dev</em> file in the project root to store environment variables for development:</p>
<div class="codehilite"><pre><span></span><code>DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
</code></pre></div>

<p>Build the image:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose build
</code></pre></div>

<p>Once the image is built, run the container:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose up -d
</code></pre></div>

<p>Navigate to <a href="http://localhost:8000/">http://localhost:8000/</a> to again view the welcome screen.</p>

<h2 id="postgres">Postgres</h2>
<p>To configure Postgres, we'll need to add a new service to the <em>docker-compose.yml</em> file, update the Django settings, and install <a href="http://initd.org/psycopg/">Psycopg2</a>.</p>
<p>First, add a new service called <code>db</code> to <em>docker-compose.yml</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">&#39;3.8&#39;</span><span class="w"></span>

<span class="nt">services</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">web</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./app</span><span class="w"></span>
<span class="w">    </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">python manage.py runserver 0.0.0.0:8000</span><span class="w"></span>
<span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./app/:/usr/src/app/</span><span class="w"></span>
<span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">8000:8000</span><span class="w"></span>
<span class="w">    </span><span class="nt">env_file</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./.env.dev</span><span class="w"></span>
<span class="w">    </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">db</span><span class="w"></span>
<span class="w">  </span><span class="nt">db</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">postgres:13.0-alpine</span><span class="w"></span>
<span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">postgres_data:/var/lib/postgresql/data/</span><span class="w"></span>
<span class="w">    </span><span class="nt">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">POSTGRES_USER=hello_django</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">POSTGRES_PASSWORD=hello_django</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">POSTGRES_DB=hello_django_dev</span><span class="w"></span>

<span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">postgres_data</span><span class="p">:</span><span class="w"></span>
</code></pre></div>

<p>To persist the data beyond the life of the container we configured a volume. This config will bind <code>postgres_data</code> to the "/var/lib/postgresql/data/" directory in the container.</p>
<p>We also added an environment key to define a name for the default database and set a username and password.</p>

<p>We'll need some new environment variables for the <code>web</code> service as well, so update <em>.env.dev</em> like so:</p>
<div class="codehilite"><pre><span></span><code>DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
</code></pre></div>

<p>Update the <code>DATABASES</code> dict in <em>settings.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="n">DATABASES</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s2">&quot;default&quot;</span><span class="p">:</span> <span class="p">{</span>
        <span class="s2">&quot;ENGINE&quot;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;SQL_ENGINE&quot;</span><span class="p">,</span> <span class="s2">&quot;django.db.backends.sqlite3&quot;</span><span class="p">),</span>
        <span class="s2">&quot;NAME&quot;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;SQL_DATABASE&quot;</span><span class="p">,</span> <span class="n">BASE_DIR</span> <span class="o">/</span> <span class="s2">&quot;db.sqlite3&quot;</span><span class="p">),</span>
        <span class="s2">&quot;USER&quot;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;SQL_USER&quot;</span><span class="p">,</span> <span class="s2">&quot;user&quot;</span><span class="p">),</span>
        <span class="s2">&quot;PASSWORD&quot;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;SQL_PASSWORD&quot;</span><span class="p">,</span> <span class="s2">&quot;password&quot;</span><span class="p">),</span>
        <span class="s2">&quot;HOST&quot;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;SQL_HOST&quot;</span><span class="p">,</span> <span class="s2">&quot;localhost&quot;</span><span class="p">),</span>
        <span class="s2">&quot;PORT&quot;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">&quot;SQL_PORT&quot;</span><span class="p">,</span> <span class="s2">&quot;5432&quot;</span><span class="p">),</span>
    <span class="p">}</span>
<span class="p">}</span>
</code></pre></div>

<p>Here, the database is configured based on the environment variables that we just defined. Take note of the default values.</p>
<p>Update the Dockerfile to install the appropriate packages required for Psycopg2:</p>
<div class="codehilite"><pre><span></span><code><span class="c"># pull official base image</span>
<span class="k">FROM</span><span class="w"> </span><span class="s">python:3.9.6-alpine</span>

<span class="c"># set work directory</span>
<span class="k">WORKDIR</span><span class="w"> </span><span class="s">/usr/src/app</span>

<span class="c"># set environment variables</span>
<span class="k">ENV</span><span class="w"> </span>PYTHONDONTWRITEBYTECODE <span class="m">1</span>
<span class="k">ENV</span><span class="w"> </span>PYTHONUNBUFFERED <span class="m">1</span>

<span class="c"># install psycopg2 dependencies</span>
<span class="k">RUN</span><span class="w"> </span>apk update <span class="se">\</span>
    <span class="o">&amp;&amp;</span> apk add postgresql-dev gcc python3-dev musl-dev

<span class="c"># install dependencies</span>
<span class="k">RUN</span><span class="w"> </span>pip install --upgrade pip
<span class="k">COPY</span><span class="w"> </span>./requirements.txt .
<span class="k">RUN</span><span class="w"> </span>pip install -r requirements.txt

<span class="c"># copy project</span>
<span class="k">COPY</span><span class="w"> </span>. .
</code></pre></div>

<p>Add Psycopg2 to <em>requirements.txt</em>:</p>
<div class="codehilite"><pre><span></span><code>Django==3.2.6
psycopg2-binary==2.9.1
</code></pre></div>


<p>Build the new image and spin up the two containers:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose up -d --build
</code></pre></div>

<p>Run the migrations:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py migrate --noinput
</code></pre></div>



<p>Ensure the default Django tables were created:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose <span class="nb">exec</span> db psql --username<span class="o">=</span>hello_django --dbname<span class="o">=</span>hello_django_dev

psql <span class="o">(</span><span class="m">13</span>.0<span class="o">)</span>
Type <span class="s2">&quot;help&quot;</span> <span class="k">for</span> help.

<span class="nv">hello_django_dev</span><span class="o">=</span><span class="c1"># \l</span>
                                          List of databases
       Name       <span class="p">|</span>    Owner     <span class="p">|</span> Encoding <span class="p">|</span>  Collate   <span class="p">|</span>   Ctype    <span class="p">|</span>       Access privileges
------------------+--------------+----------+------------+------------+-------------------------------
 hello_django_dev <span class="p">|</span> hello_django <span class="p">|</span> UTF8     <span class="p">|</span> en_US.utf8 <span class="p">|</span> en_US.utf8 <span class="p">|</span>
 postgres         <span class="p">|</span> hello_django <span class="p">|</span> UTF8     <span class="p">|</span> en_US.utf8 <span class="p">|</span> en_US.utf8 <span class="p">|</span>
 template0        <span class="p">|</span> hello_django <span class="p">|</span> UTF8     <span class="p">|</span> en_US.utf8 <span class="p">|</span> en_US.utf8 <span class="p">|</span> <span class="o">=</span>c/hello_django              +
                  <span class="p">|</span>              <span class="p">|</span>          <span class="p">|</span>            <span class="p">|</span>            <span class="p">|</span> <span class="nv">hello_django</span><span class="o">=</span>CTc/hello_django
 template1        <span class="p">|</span> hello_django <span class="p">|</span> UTF8     <span class="p">|</span> en_US.utf8 <span class="p">|</span> en_US.utf8 <span class="p">|</span> <span class="o">=</span>c/hello_django              +
                  <span class="p">|</span>              <span class="p">|</span>          <span class="p">|</span>            <span class="p">|</span>            <span class="p">|</span> <span class="nv">hello_django</span><span class="o">=</span>CTc/hello_django
<span class="o">(</span><span class="m">4</span> rows<span class="o">)</span>

<span class="nv">hello_django_dev</span><span class="o">=</span><span class="c1"># \c hello_django_dev</span>
You are now connected to database <span class="s2">&quot;hello_django_dev&quot;</span> as user <span class="s2">&quot;hello_django&quot;</span>.

<span class="nv">hello_django_dev</span><span class="o">=</span><span class="c1"># \dt</span>
                     List of relations
 Schema <span class="p">|</span>            Name            <span class="p">|</span> Type  <span class="p">|</span>    Owner
--------+----------------------------+-------+--------------
 public <span class="p">|</span> auth_group                 <span class="p">|</span> table <span class="p">|</span> hello_django
 public <span class="p">|</span> auth_group_permissions     <span class="p">|</span> table <span class="p">|</span> hello_django
 public <span class="p">|</span> auth_permission            <span class="p">|</span> table <span class="p">|</span> hello_django
 public <span class="p">|</span> auth_user                  <span class="p">|</span> table <span class="p">|</span> hello_django
 public <span class="p">|</span> auth_user_groups           <span class="p">|</span> table <span class="p">|</span> hello_django
 public <span class="p">|</span> auth_user_user_permissions <span class="p">|</span> table <span class="p">|</span> hello_django
 public <span class="p">|</span> django_admin_log           <span class="p">|</span> table <span class="p">|</span> hello_django
 public <span class="p">|</span> django_content_type        <span class="p">|</span> table <span class="p">|</span> hello_django
 public <span class="p">|</span> django_migrations          <span class="p">|</span> table <span class="p">|</span> hello_django
 public <span class="p">|</span> django_session             <span class="p">|</span> table <span class="p">|</span> hello_django
<span class="o">(</span><span class="m">10</span> rows<span class="o">)</span>

<span class="nv">hello_django_dev</span><span class="o">=</span><span class="c1"># \q</span>
</code></pre></div>

<p>You can check that the volume was created as well by running:</p>
<div class="codehilite"><pre><span></span><code>$ docker volume inspect django-on-docker_postgres_data
</code></pre></div>

<p>You should see something similar to:</p>
<div class="codehilite"><pre><span></span><code><span class="o">[</span>
    <span class="o">{</span>
        <span class="s2">&quot;CreatedAt&quot;</span>: <span class="s2">&quot;2021-08-23T15:49:08Z&quot;</span>,
        <span class="s2">&quot;Driver&quot;</span>: <span class="s2">&quot;local&quot;</span>,
        <span class="s2">&quot;Labels&quot;</span>: <span class="o">{</span>
            <span class="s2">&quot;com.docker.compose.project&quot;</span>: <span class="s2">&quot;django-on-docker&quot;</span>,
            <span class="s2">&quot;com.docker.compose.version&quot;</span>: <span class="s2">&quot;1.29.2&quot;</span>,
            <span class="s2">&quot;com.docker.compose.volume&quot;</span>: <span class="s2">&quot;postgres_data&quot;</span>
        <span class="o">}</span>,
        <span class="s2">&quot;Mountpoint&quot;</span>: <span class="s2">&quot;/var/lib/docker/volumes/django-on-docker_postgres_data/_data&quot;</span>,
        <span class="s2">&quot;Name&quot;</span>: <span class="s2">&quot;django-on-docker_postgres_data&quot;</span>,
        <span class="s2">&quot;Options&quot;</span>: null,
        <span class="s2">&quot;Scope&quot;</span>: <span class="s2">&quot;local&quot;</span>
    <span class="o">}</span>
<span class="o">]</span>
</code></pre></div>

<p>Next, add an <em>entrypoint.sh</em> file to the "app" directory to verify that Postgres is healthy <em>before</em> applying the migrations and running the Django development server:</p>
<div class="codehilite"><pre><span></span><code><span class="ch">#!/bin/sh</span>

<span class="k">if</span> <span class="o">[</span> <span class="s2">&quot;</span><span class="nv">$DATABASE</span><span class="s2">&quot;</span> <span class="o">=</span> <span class="s2">&quot;postgres&quot;</span> <span class="o">]</span>
<span class="k">then</span>
    <span class="nb">echo</span> <span class="s2">&quot;Waiting for postgres...&quot;</span>

<span class="k">while</span> ! nc -z <span class="nv">$SQL_HOST</span> <span class="nv">$SQL_PORT</span><span class="p">;</span> <span class="k">do</span>
      sleep <span class="m">0</span>.1
    <span class="k">done</span>

<span class="nb">echo</span> <span class="s2">&quot;PostgreSQL started&quot;</span>
<span class="k">fi</span>

python manage.py flush --no-input
python manage.py migrate

<span class="nb">exec</span> <span class="s2">&quot;</span><span class="nv"><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="4a6e0a">[email&#160;protected]</a></span><span class="s2">&quot;</span>
</code></pre></div>

<p>Update the file permissions locally:</p>
<div class="codehilite"><pre><span></span><code>$ chmod +x app/entrypoint.sh
</code></pre></div>

<p>Then, update the Dockerfile to copy over the <em>entrypoint.sh</em> file and run it as the Docker <a href="https://docs.docker.com/engine/reference/builder/#entrypoint">entrypoint</a> command:</p>
<div class="codehilite"><pre><span></span><code><span class="c"># pull official base image</span>
<span class="k">FROM</span><span class="w"> </span><span class="s">python:3.9.6-alpine</span>

<span class="c"># set work directory</span>
<span class="k">WORKDIR</span><span class="w"> </span><span class="s">/usr/src/app</span>

<span class="c"># set environment variables</span>
<span class="k">ENV</span><span class="w"> </span>PYTHONDONTWRITEBYTECODE <span class="m">1</span>
<span class="k">ENV</span><span class="w"> </span>PYTHONUNBUFFERED <span class="m">1</span>

<span class="c"># install psycopg2 dependencies</span>
<span class="k">RUN</span><span class="w"> </span>apk update <span class="se">\</span>
    <span class="o">&amp;&amp;</span> apk add postgresql-dev gcc python3-dev musl-dev

<span class="c"># install dependencies</span>
<span class="k">RUN</span><span class="w"> </span>pip install --upgrade pip
<span class="k">COPY</span><span class="w"> </span>./requirements.txt .
<span class="k">RUN</span><span class="w"> </span>pip install -r requirements.txt

<span class="c"># copy entrypoint.sh</span>
<span class="k">COPY</span><span class="w"> </span>./entrypoint.sh .
<span class="k">RUN</span><span class="w"> </span>sed -i <span class="s1">&#39;s/\r$//g&#39;</span> /usr/src/app/entrypoint.sh
<span class="k">RUN</span><span class="w"> </span>chmod +x /usr/src/app/entrypoint.sh

<span class="c"># copy project</span>
<span class="k">COPY</span><span class="w"> </span>. .

<span class="c"># run entrypoint.sh</span>
<span class="k">ENTRYPOINT</span><span class="w"> </span><span class="p">[</span><span class="s2">&quot;/usr/src/app/entrypoint.sh&quot;</span><span class="p">]</span>
</code></pre></div>

<p>Add the <code>DATABASE</code> environment variable to <em>.env.dev</em>:</p>
<div class="codehilite"><pre><span></span><code>DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
</code></pre></div>

<p>Test it out again:</p>
<ol>
<li>Re-build the images</li>
<li>Run the containers</li>
<li>Try <a href="http://localhost:8000/">http://localhost:8000/</a></li>
</ol>
<h3 id="notes">Notes</h3>
<p>First, despite adding Postgres, we can still create an independent Docker image for Django as long as the <code>DATABASE</code> environment variable is not set to <code>postgres</code>. To test, build a new image and then run a new container:</p>
<div class="codehilite"><pre><span></span><code>$ docker build -f ./app/Dockerfile -t hello_django:latest ./app
$ docker run -d <span class="se">\</span>
    -p <span class="m">8006</span>:8000 <span class="se">\</span>
    -e <span class="s2">&quot;SECRET_KEY=please_change_me&quot;</span> -e <span class="s2">&quot;DEBUG=1&quot;</span> -e <span class="s2">&quot;DJANGO_ALLOWED_HOSTS=*&quot;</span> <span class="se">\</span>
    hello_django python /usr/src/app/manage.py runserver <span class="m">0</span>.0.0.0:8000
</code></pre></div>

<p>You should be able to view the welcome page at <a href="http://localhost:8006">http://localhost:8006</a></p>
<p>Second, you may want to comment out the database flush and migrate commands in the <em>entrypoint.sh</em> script so they don't run on every container start or re-start:</p>
<div class="codehilite"><pre><span></span><code><span class="ch">#!/bin/sh</span>

<span class="k">if</span> <span class="o">[</span> <span class="s2">&quot;</span><span class="nv">$DATABASE</span><span class="s2">&quot;</span> <span class="o">=</span> <span class="s2">&quot;postgres&quot;</span> <span class="o">]</span>
<span class="k">then</span>
    <span class="nb">echo</span> <span class="s2">&quot;Waiting for postgres...&quot;</span>

<span class="k">while</span> ! nc -z <span class="nv">$SQL_HOST</span> <span class="nv">$SQL_PORT</span><span class="p">;</span> <span class="k">do</span>
      sleep <span class="m">0</span>.1
    <span class="k">done</span>

<span class="nb">echo</span> <span class="s2">&quot;PostgreSQL started&quot;</span>
<span class="k">fi</span>

<span class="c1"># python manage.py flush --no-input</span>
<span class="c1"># python manage.py migrate</span>

<span class="nb">exec</span> <span class="s2">&quot;</span><span class="nv"><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="82a6c2">[email&#160;protected]</a></span><span class="s2">&quot;</span>
</code></pre></div>

<p>Instead, you can run them manually, after the containers spin up, like so:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py flush --no-input
$ docker-compose <span class="nb">exec</span> web python manage.py migrate
</code></pre></div>

<h2 id="gunicorn">Gunicorn</h2>
<p>Moving along, for production environments, let's add <a href="https://gunicorn.org/">Gunicorn</a>, a production-grade WSGI server, to the requirements file:</p>
<div class="codehilite"><pre><span></span><code>Django==3.2.6
gunicorn==20.1.0
psycopg2-binary==2.9.1
</code></pre></div>


<p>Since we still want to use Django's built-in server in development, create a new compose file called <em>docker-compose.prod.yml</em> for production:</p>
<div class="codehilite"><pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">&#39;3.8&#39;</span><span class="w"></span>

<span class="nt">services</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">web</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./app</span><span class="w"></span>
<span class="w">    </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000</span><span class="w"></span>
<span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">8000:8000</span><span class="w"></span>
<span class="w">    </span><span class="nt">env_file</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./.env.prod</span><span class="w"></span>
<span class="w">    </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">db</span><span class="w"></span>
<span class="w">  </span><span class="nt">db</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">postgres:13.0-alpine</span><span class="w"></span>
<span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">postgres_data:/var/lib/postgresql/data/</span><span class="w"></span>
<span class="w">    </span><span class="nt">env_file</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./.env.prod.db</span><span class="w"></span>

<span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">postgres_data</span><span class="p">:</span><span class="w"></span>
</code></pre></div>


<p>Take note of the default <code>command</code>. We're running Gunicorn rather than the Django development server. We also removed the volume from the <code>web</code> service since we don't need it in production. Finally, we're using <a href="https://docs.docker.com/compose/env-file/">separate environment variable files</a> to define environment variables for both services that will be passed to the container at runtime.</p>
<p><em>.env.prod</em>:</p>
<div class="codehilite"><pre><span></span><code>DEBUG=0
SECRET_KEY=change_me
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_prod
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
</code></pre></div>

<p><em>.env.prod.db</em>:</p>
<div class="codehilite"><pre><span></span><code>POSTGRES_USER=hello_django
POSTGRES_PASSWORD=hello_django
POSTGRES_DB=hello_django_prod
</code></pre></div>

<p>Add the two files to the project root. You'll probably want to keep them out of version control, so add them to a <em>.gitignore</em> file.</p>
<p>Bring <a href="https://docs.docker.com/compose/reference/down/">down</a> the development containers (and the associated volumes with the <code>-v</code> flag):</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose down -v
</code></pre></div>

<p>Then, build the production images and spin up the containers:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose -f docker-compose.prod.yml up -d --build
</code></pre></div>

<p>Verify that the <code>hello_django_prod</code> database was created along with the default Django tables. Test out the admin page at <a href="http://localhost:8000/admin">http://localhost:8000/admin</a>. The static files are not being loaded anymore. This is expected since Debug mode is off. We'll fix this shortly.</p>

<h2 id="production-dockerfile">Production Dockerfile</h2>
<p>Did you notice that we're still running the database <a href="https://docs.djangoproject.com/en/2.2/ref/django-admin/#flush">flush</a> (which clears out the database) and migrate commands every time the container is run? This is fine in development, but let's create a new entrypoint file for production.</p>
<p><em>entrypoint.prod.sh</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="ch">#!/bin/sh</span>

<span class="k">if</span> <span class="o">[</span> <span class="s2">&quot;</span><span class="nv">$DATABASE</span><span class="s2">&quot;</span> <span class="o">=</span> <span class="s2">&quot;postgres&quot;</span> <span class="o">]</span>
<span class="k">then</span>
    <span class="nb">echo</span> <span class="s2">&quot;Waiting for postgres...&quot;</span>

<span class="k">while</span> ! nc -z <span class="nv">$SQL_HOST</span> <span class="nv">$SQL_PORT</span><span class="p">;</span> <span class="k">do</span>
      sleep <span class="m">0</span>.1
    <span class="k">done</span>

<span class="nb">echo</span> <span class="s2">&quot;PostgreSQL started&quot;</span>
<span class="k">fi</span>

<span class="nb">exec</span> <span class="s2">&quot;</span><span class="nv"><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="8fabcf">[email&#160;protected]</a></span><span class="s2">&quot;</span>
</code></pre></div>

<p>Update the file permissions locally:</p>
<div class="codehilite"><pre><span></span><code>$ chmod +x app/entrypoint.prod.sh
</code></pre></div>

<p>To use this file, create a new Dockerfile called <em>Dockerfile.prod</em> for use with production builds:</p>
<div class="codehilite"><pre><span></span><code><span class="c">###########</span>
<span class="c"># BUILDER #</span>
<span class="c">###########</span>

<span class="c"># pull official base image</span>
<span class="k">FROM</span><span class="w"> </span><span class="s">python:3.9.6-alpine</span><span class="w"> </span><span class="k">as</span><span class="w"> </span><span class="s">builder</span>

<span class="c"># set work directory</span>
<span class="k">WORKDIR</span><span class="w"> </span><span class="s">/usr/src/app</span>

<span class="c"># set environment variables</span>
<span class="k">ENV</span><span class="w"> </span>PYTHONDONTWRITEBYTECODE <span class="m">1</span>
<span class="k">ENV</span><span class="w"> </span>PYTHONUNBUFFERED <span class="m">1</span>

<span class="c"># install psycopg2 dependencies</span>
<span class="k">RUN</span><span class="w"> </span>apk update <span class="se">\</span>
    <span class="o">&amp;&amp;</span> apk add postgresql-dev gcc python3-dev musl-dev

<span class="c"># lint</span>
<span class="k">RUN</span><span class="w"> </span>pip install --upgrade pip
<span class="k">RUN</span><span class="w"> </span>pip install <span class="nv">flake8</span><span class="o">==</span><span class="m">3</span>.9.2
<span class="k">COPY</span><span class="w"> </span>. .
<span class="k">RUN</span><span class="w"> </span>flake8 --ignore<span class="o">=</span>E501,F401 .

<span class="c"># install dependencies</span>
<span class="k">COPY</span><span class="w"> </span>./requirements.txt .
<span class="k">RUN</span><span class="w"> </span>pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


<span class="c">#########</span>
<span class="c"># FINAL #</span>
<span class="c">#########</span>

<span class="c"># pull official base image</span>
<span class="k">FROM</span><span class="w"> </span><span class="s">python:3.9.6-alpine</span>

<span class="c"># create directory for the app user</span>
<span class="k">RUN</span><span class="w"> </span>mkdir -p /home/app

<span class="c"># create the app user</span>
<span class="k">RUN</span><span class="w"> </span>addgroup -S app <span class="o">&amp;&amp;</span> adduser -S app -G app

<span class="c"># create the appropriate directories</span>
<span class="k">ENV</span><span class="w"> </span><span class="nv">HOME</span><span class="o">=</span>/home/app
<span class="k">ENV</span><span class="w"> </span><span class="nv">APP_HOME</span><span class="o">=</span>/home/app/web
<span class="k">RUN</span><span class="w"> </span>mkdir <span class="nv">$APP_HOME</span>
<span class="k">WORKDIR</span><span class="w"> </span><span class="s">$APP_HOME</span>

<span class="c"># install dependencies</span>
<span class="k">RUN</span><span class="w"> </span>apk update <span class="o">&amp;&amp;</span> apk add libpq
<span class="k">COPY</span><span class="w"> </span>--from<span class="o">=</span>builder /usr/src/app/wheels /wheels
<span class="k">COPY</span><span class="w"> </span>--from<span class="o">=</span>builder /usr/src/app/requirements.txt .
<span class="k">RUN</span><span class="w"> </span>pip install --no-cache /wheels/*

<span class="c"># copy entrypoint.prod.sh</span>
<span class="k">COPY</span><span class="w"> </span>./entrypoint.prod.sh .
<span class="k">RUN</span><span class="w"> </span>sed -i <span class="s1">&#39;s/\r$//g&#39;</span>  <span class="nv">$APP_HOME</span>/entrypoint.prod.sh
<span class="k">RUN</span><span class="w"> </span>chmod +x  <span class="nv">$APP_HOME</span>/entrypoint.prod.sh

<span class="c"># copy project</span>
<span class="k">COPY</span><span class="w"> </span>. <span class="nv">$APP_HOME</span>

<span class="c"># chown all the files to the app user</span>
<span class="k">RUN</span><span class="w"> </span>chown -R app:app <span class="nv">$APP_HOME</span>

<span class="c"># change to the app user</span>
<span class="k">USER</span><span class="w"> </span><span class="s">app</span>

<span class="c"># run entrypoint.prod.sh</span>
<span class="k">ENTRYPOINT</span><span class="w"> </span><span class="p">[</span><span class="s2">&quot;/home/app/web/entrypoint.prod.sh&quot;</span><span class="p">]</span>
</code></pre></div>

<p>Here, we used a Docker <a href="https://docs.docker.com/develop/develop-images/multistage-build/">multi-stage build</a> to reduce the final image size. Essentially, <code>builder</code> is a temporary image that's used for building the Python wheels. The wheels are then copied over to the final production image and the <code>builder</code> image is discarded.</p>

<p>Did you notice that we created a non-root user? By default, Docker runs container processes as root inside of a container. This is a bad practice since attackers can gain root access to the Docker host if they manage to break out of the container. If you're root in the container, you'll be root on the host.</p>
<p>Update the <code>web</code> service within the <em>docker-compose.prod.yml</em> file to build with <em>Dockerfile.prod</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="nt">web</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./app</span><span class="w"></span>
<span class="w">    </span><span class="nt">dockerfile</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Dockerfile.prod</span><span class="w"></span>
<span class="w">  </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000</span><span class="w"></span>
<span class="w">  </span><span class="nt">ports</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">8000:8000</span><span class="w"></span>
<span class="w">  </span><span class="nt">env_file</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./.env.prod</span><span class="w"></span>
<span class="w">  </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">db</span><span class="w"></span>
</code></pre></div>

<p>Try it out:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose -f docker-compose.prod.yml down -v
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml <span class="nb">exec</span> web python manage.py migrate --noinput
</code></pre></div>

<h2 id="nginx">Nginx</h2>
<p>Next, let's add Nginx into the mix to act as a <a href="https://www.nginx.com/resources/glossary/reverse-proxy-server/">reverse proxy</a> for Gunicorn to handle client requests as well as serve up static files.</p>
<p>Add the service to <em>docker-compose.prod.yml</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="nt">nginx</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./nginx</span><span class="w"></span>
<span class="w">  </span><span class="nt">ports</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1337:80</span><span class="w"></span>
<span class="w">  </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">web</span><span class="w"></span>
</code></pre></div>

<p>Then, in the local project root, create the following files and folders:</p>
<div class="codehilite"><pre><span></span><code>└── nginx
    ├── Dockerfile
    └── nginx.conf
</code></pre></div>

<p><em>Dockerfile</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="k">FROM</span><span class="w"> </span><span class="s">nginx:1.21-alpine</span>

<span class="k">RUN</span><span class="w"> </span>rm /etc/nginx/conf.d/default.conf
<span class="k">COPY</span><span class="w"> </span>nginx.conf /etc/nginx/conf.d
</code></pre></div>

<p><em>nginx.conf</em>:</p>
<div class="codehilite"><pre><span></span><code>upstream hello_django <span class="o">{</span>
    server web:8000<span class="p">;</span>
<span class="o">}</span>

server <span class="o">{</span>

listen <span class="m">80</span><span class="p">;</span>

location / <span class="o">{</span>
        proxy_pass http://hello_django<span class="p">;</span>
        proxy_set_header X-Forwarded-For <span class="nv">$proxy_add_x_forwarded_for</span><span class="p">;</span>
        proxy_set_header Host <span class="nv">$host</span><span class="p">;</span>
        proxy_redirect off<span class="p">;</span>
    <span class="o">}</span>

<span class="o">}</span>
</code></pre></div>


<p>Then, update the <code>web</code> service, in <em>docker-compose.prod.yml</em>, replacing <code>ports</code> with <code>expose</code>:</p>
<div class="codehilite"><pre><span></span><code><span class="nt">web</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./app</span><span class="w"></span>
<span class="w">    </span><span class="nt">dockerfile</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Dockerfile.prod</span><span class="w"></span>
<span class="w">  </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000</span><span class="w"></span>
<span class="w">  </span><span class="nt">expose</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">8000</span><span class="w"></span>
<span class="w">  </span><span class="nt">env_file</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./.env.prod</span><span class="w"></span>
<span class="w">  </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">db</span><span class="w"></span>
</code></pre></div>

<p>Now, port 8000 is only exposed internally, to other Docker services. The port will no longer be published to the host machine.</p>

<p>Test it out again.</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose -f docker-compose.prod.yml down -v
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml <span class="nb">exec</span> web python manage.py migrate --noinput
</code></pre></div>

<p>Ensure the app is up and running at <a href="http://localhost:1337">http://localhost:1337</a>.</p>
<p>Your project structure should now look like:</p>
<div class="codehilite"><pre><span></span><code>├── .env.dev
├── .env.prod
├── .env.prod.db
├── .gitignore
├── app
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── entrypoint.prod.sh
│   ├── entrypoint.sh
│   ├── hello_django
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── requirements.txt
├── docker-compose.prod.yml
├── docker-compose.yml
└── nginx
    ├── Dockerfile
    └── nginx.conf
</code></pre></div>

<p>Bring the containers down once done:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose -f docker-compose.prod.yml down -v
</code></pre></div>

<p>Since Gunicorn is an application server, it will not serve up static files. So, how should both static and media files be handled in this particular configuration?</p>
<h2 id="static-files">Static Files</h2>
<p>Update <em>settings.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="nv">STATIC_URL</span> <span class="o">=</span> <span class="s2">&quot;/static/&quot;</span>
<span class="nv">STATIC_ROOT</span> <span class="o">=</span> BASE_DIR / <span class="s2">&quot;staticfiles&quot;</span>
</code></pre></div>

<h3 id="development">Development</h3>
<p>Now, any request to <code>http://localhost:8000/static/*</code> will be served from the "staticfiles" directory.</p>
<p>To test, first re-build the images and spin up the new containers per usual. Ensure static files are still being served correctly at <a href="http://localhost:8000/admin">http://localhost:8000/admin</a>.</p>
<h3 id="production">Production</h3>
<p>For production, add a volume to the <code>web</code> and <code>nginx</code> services in <em>docker-compose.prod.yml</em> so that each container will share a directory named "staticfiles":</p>
<div class="codehilite"><pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">&#39;3.8&#39;</span><span class="w"></span>

<span class="nt">services</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">web</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./app</span><span class="w"></span>
<span class="w">      </span><span class="nt">dockerfile</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Dockerfile.prod</span><span class="w"></span>
<span class="w">    </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000</span><span class="w"></span>
<span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">static_volume:/home/app/web/staticfiles</span><span class="w"></span>
<span class="w">    </span><span class="nt">expose</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">8000</span><span class="w"></span>
<span class="w">    </span><span class="nt">env_file</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./.env.prod</span><span class="w"></span>
<span class="w">    </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">db</span><span class="w"></span>
<span class="w">  </span><span class="nt">db</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">postgres:13.0-alpine</span><span class="w"></span>
<span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">postgres_data:/var/lib/postgresql/data/</span><span class="w"></span>
<span class="w">    </span><span class="nt">env_file</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./.env.prod.db</span><span class="w"></span>
<span class="w">  </span><span class="nt">nginx</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./nginx</span><span class="w"></span>
<span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">static_volume:/home/app/web/staticfiles</span><span class="w"></span>
<span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1337:80</span><span class="w"></span>
<span class="w">    </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">web</span><span class="w"></span>

<span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">postgres_data</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">static_volume</span><span class="p">:</span><span class="w"></span>
</code></pre></div>

<p>We need to also create the "/home/app/web/staticfiles" folder in <em>Dockerfile.prod</em>:</p>
<div class="codehilite"><pre><span></span><code>...

<span class="c"># create the appropriate directories</span>
<span class="k">ENV</span><span class="w"> </span><span class="nv">HOME</span><span class="o">=</span>/home/app
<span class="k">ENV</span><span class="w"> </span><span class="nv">APP_HOME</span><span class="o">=</span>/home/app/web
<span class="k">RUN</span><span class="w"> </span>mkdir <span class="nv">$APP_HOME</span>
<span class="k">RUN</span><span class="w"> </span>mkdir <span class="nv">$APP_HOME</span>/staticfiles
<span class="k">WORKDIR</span><span class="w"> </span><span class="s">$APP_HOME</span>

...
</code></pre></div>

<p>Why is this necessary?</p>
<p>Docker Compose normally mounts named volumes as root. And since we're using a non-root user, we'll get a permission denied error when the <code>collectstatic</code> command is run if the directory does not already exist</p>
<p>To get around this, you can either:</p>
<ol>
<li>Create the folder in the Dockerfile (<a href="https://github.com/docker/compose/issues/3270#issuecomment-206214034">source</a>)</li>
<li>Change the permissions of the directory after it's mounted (<a href="https://stackoverflow.com/a/40510068/1799408">source</a>)</li>
</ol>
<p>We used the former.</p>
<p>Next, update the Nginx configuration to route static file requests to the "staticfiles" folder:</p>
<div class="codehilite"><pre><span></span><code>upstream hello_django <span class="o">{</span>
    server web:8000<span class="p">;</span>
<span class="o">}</span>

server <span class="o">{</span>

listen <span class="m">80</span><span class="p">;</span>

location / <span class="o">{</span>
        proxy_pass http://hello_django<span class="p">;</span>
        proxy_set_header X-Forwarded-For <span class="nv">$proxy_add_x_forwarded_for</span><span class="p">;</span>
        proxy_set_header Host <span class="nv">$host</span><span class="p">;</span>
        proxy_redirect off<span class="p">;</span>
    <span class="o">}</span>

location /static/ <span class="o">{</span>
        <span class="nb">alias</span> /home/app/web/staticfiles/<span class="p">;</span>
    <span class="o">}</span>

<span class="o">}</span>
</code></pre></div>

<p>Spin down the development containers:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose down -v
</code></pre></div>

<p>Test:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml <span class="nb">exec</span> web python manage.py migrate --noinput
$ docker-compose -f docker-compose.prod.yml <span class="nb">exec</span> web python manage.py collectstatic --no-input --clear
</code></pre></div>

<p>Again, requests to <code>http://localhost:1337/static/*</code> will be served from the "staticfiles" directory.</p>
<p>Navigate to <a href="http://localhost:1337/admin">http://localhost:1337/admin</a> and ensure the static assets load correctly.</p>
<p>You can also verify in the logs -- via <code>docker-compose -f docker-compose.prod.yml logs -f</code> -- that requests to the static files are served up successfully via Nginx:</p>
<div class="codehilite"><pre><span></span><code>nginx_1  <span class="p">|</span> <span class="m">192</span>.168.144.1 - - <span class="o">[</span><span class="m">23</span>/Aug/2021:20:11:00 +0000<span class="o">]</span> <span class="s2">&quot;GET /admin/ HTTP/1.1&quot;</span> <span class="m">302</span> <span class="m">0</span> <span class="s2">&quot;-&quot;</span> <span class="s2">&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36&quot;</span> <span class="s2">&quot;-&quot;</span>
nginx_1  <span class="p">|</span> <span class="m">192</span>.168.144.1 - - <span class="o">[</span><span class="m">23</span>/Aug/2021:20:11:00 +0000<span class="o">]</span> <span class="s2">&quot;GET /admin/login/?next=/admin/ HTTP/1.1&quot;</span> <span class="m">200</span> <span class="m">2214</span> <span class="s2">&quot;-&quot;</span> <span class="s2">&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36&quot;</span> <span class="s2">&quot;-&quot;</span>
nginx_1  <span class="p">|</span> <span class="m">192</span>.168.144.1 - - <span class="o">[</span><span class="m">23</span>/Aug/2021:20:11:00 +0000<span class="o">]</span> <span class="s2">&quot;GET /static/admin/css/base.css HTTP/1.1&quot;</span> <span class="m">304</span> <span class="m">0</span> <span class="s2">&quot;http://localhost:1337/admin/login/?next=/admin/&quot;</span> <span class="s2">&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36&quot;</span> <span class="s2">&quot;-&quot;</span>
nginx_1  <span class="p">|</span> <span class="m">192</span>.168.144.1 - - <span class="o">[</span><span class="m">23</span>/Aug/2021:20:11:00 +0000<span class="o">]</span> <span class="s2">&quot;GET /static/admin/css/nav_sidebar.css HTTP/1.1&quot;</span> <span class="m">304</span> <span class="m">0</span> <span class="s2">&quot;http://localhost:1337/admin/login/?next=/admin/&quot;</span> <span class="s2">&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36&quot;</span> <span class="s2">&quot;-&quot;</span>
nginx_1  <span class="p">|</span> <span class="m">192</span>.168.144.1 - - <span class="o">[</span><span class="m">23</span>/Aug/2021:20:11:00 +0000<span class="o">]</span> <span class="s2">&quot;GET /static/admin/css/responsive.css HTTP/1.1&quot;</span> <span class="m">304</span> <span class="m">0</span> <span class="s2">&quot;http://localhost:1337/admin/login/?next=/admin/&quot;</span> <span class="s2">&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36&quot;</span> <span class="s2">&quot;-&quot;</span>
nginx_1  <span class="p">|</span> <span class="m">192</span>.168.144.1 - - <span class="o">[</span><span class="m">23</span>/Aug/2021:20:11:00 +0000<span class="o">]</span> <span class="s2">&quot;GET /static/admin/css/login.css HTTP/1.1&quot;</span> <span class="m">304</span> <span class="m">0</span> <span class="s2">&quot;http://localhost:1337/admin/login/?next=/admin/&quot;</span> <span class="s2">&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36&quot;</span> <span class="s2">&quot;-&quot;</span>
nginx_1  <span class="p">|</span> <span class="m">192</span>.168.144.1 - - <span class="o">[</span><span class="m">23</span>/Aug/2021:20:11:00 +0000<span class="o">]</span> <span class="s2">&quot;GET /static/admin/js/nav_sidebar.js HTTP/1.1&quot;</span> <span class="m">304</span> <span class="m">0</span> <span class="s2">&quot;http://localhost:1337/admin/login/?next=/admin/&quot;</span> <span class="s2">&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36&quot;</span> <span class="s2">&quot;-&quot;</span>
nginx_1  <span class="p">|</span> <span class="m">192</span>.168.144.1 - - <span class="o">[</span><span class="m">23</span>/Aug/2021:20:11:00 +0000<span class="o">]</span> <span class="s2">&quot;GET /static/admin/css/fonts.css HTTP/1.1&quot;</span> <span class="m">304</span> <span class="m">0</span> <span class="s2">&quot;http://localhost:1337/static/admin/css/base.css&quot;</span> <span class="s2">&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36&quot;</span> <span class="s2">&quot;-&quot;</span>
nginx_1  <span class="p">|</span> <span class="m">192</span>.168.144.1 - - <span class="o">[</span><span class="m">23</span>/Aug/2021:20:11:00 +0000<span class="o">]</span> <span class="s2">&quot;GET /static/admin/fonts/Roboto-Regular-webfont.woff HTTP/1.1&quot;</span> <span class="m">304</span> <span class="m">0</span> <span class="s2">&quot;http://localhost:1337/static/admin/css/fonts.css&quot;</span> <span class="s2">&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36&quot;</span> <span class="s2">&quot;-&quot;</span>
nginx_1  <span class="p">|</span> <span class="m">192</span>.168.144.1 - - <span class="o">[</span><span class="m">23</span>/Aug/2021:20:11:00 +0000<span class="o">]</span> <span class="s2">&quot;GET /static/admin/fonts/Roboto-Light-webfont.woff HTTP/1.1&quot;</span> <span class="m">304</span> <span class="m">0</span> <span class="s2">&quot;http://localhost:1337/static/admin/css/fonts.css&quot;</span> <span class="s2">&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36&quot;</span> <span class="s2">&quot;-&quot;</span>
</code></pre></div>

<p>Bring the containers once done:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose -f docker-compose.prod.yml down -v
</code></pre></div>

<h2 id="media-files">Media Files</h2>
<p>To test out the handling of media files, start by creating a new Django app:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose up -d --build
$ docker-compose <span class="nb">exec</span> web python manage.py startapp upload
</code></pre></div>

<p>Add the new app to the <code>INSTALLED_APPS</code> list in <em>settings.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
    <span class="s2">&quot;django.contrib.admin&quot;</span><span class="p">,</span>
    <span class="s2">&quot;django.contrib.auth&quot;</span><span class="p">,</span>
    <span class="s2">&quot;django.contrib.contenttypes&quot;</span><span class="p">,</span>
    <span class="s2">&quot;django.contrib.sessions&quot;</span><span class="p">,</span>
    <span class="s2">&quot;django.contrib.messages&quot;</span><span class="p">,</span>
    <span class="s2">&quot;django.contrib.staticfiles&quot;</span><span class="p">,</span>

<span class="s2">&quot;upload&quot;</span><span class="p">,</span>
<span class="p">]</span>
</code></pre></div>

<p><em>app/upload/views.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="kn">from</span> <span class="nn">django.shortcuts</span> <span class="kn">import</span> <span class="n">render</span>
<span class="kn">from</span> <span class="nn">django.core.files.storage</span> <span class="kn">import</span> <span class="n">FileSystemStorage</span>


<span class="k">def</span> <span class="nf">image_upload</span><span class="p">(</span><span class="n">request</span><span class="p">):</span>
    <span class="k">if</span> <span class="n">request</span><span class="o">.</span><span class="n">method</span> <span class="o">==</span> <span class="s2">&quot;POST&quot;</span> <span class="ow">and</span> <span class="n">request</span><span class="o">.</span><span class="n">FILES</span><span class="p">[</span><span class="s2">&quot;image_file&quot;</span><span class="p">]:</span>
        <span class="n">image_file</span> <span class="o">=</span> <span class="n">request</span><span class="o">.</span><span class="n">FILES</span><span class="p">[</span><span class="s2">&quot;image_file&quot;</span><span class="p">]</span>
        <span class="n">fs</span> <span class="o">=</span> <span class="n">FileSystemStorage</span><span class="p">()</span>
        <span class="n">filename</span> <span class="o">=</span> <span class="n">fs</span><span class="o">.</span><span class="n">save</span><span class="p">(</span><span class="n">image_file</span><span class="o">.</span><span class="n">name</span><span class="p">,</span> <span class="n">image_file</span><span class="p">)</span>
        <span class="n">image_url</span> <span class="o">=</span> <span class="n">fs</span><span class="o">.</span><span class="n">url</span><span class="p">(</span><span class="n">filename</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="n">image_url</span><span class="p">)</span>
        <span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="s2">&quot;upload.html&quot;</span><span class="p">,</span> <span class="p">{</span>
            <span class="s2">&quot;image_url&quot;</span><span class="p">:</span> <span class="n">image_url</span>
        <span class="p">})</span>
    <span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="s2">&quot;upload.html&quot;</span><span class="p">)</span>
</code></pre></div>

<p>Add a "templates", directory to the "app/upload" directory, and then add a new template called <em>upload.html</em>:</p>
<div class="codehilite"><pre><span></span><code>{% block content %}

  <span class="p">&lt;</span><span class="nt">form</span> <span class="na">action</span><span class="o">=</span><span class="s">&quot;{% url &quot;</span><span class="na">upload</span><span class="err">&quot;</span> <span class="err">%}&quot;</span> <span class="na">method</span><span class="o">=</span><span class="s">&quot;post&quot;</span> <span class="na">enctype</span><span class="o">=</span><span class="s">&quot;multipart/form-data&quot;</span><span class="p">&gt;</span>
    {% csrf_token %}
    <span class="p">&lt;</span><span class="nt">input</span> <span class="na">type</span><span class="o">=</span><span class="s">&quot;file&quot;</span> <span class="na">name</span><span class="o">=</span><span class="s">&quot;image_file&quot;</span><span class="p">&gt;</span>
    <span class="p">&lt;</span><span class="nt">input</span> <span class="na">type</span><span class="o">=</span><span class="s">&quot;submit&quot;</span> <span class="na">value</span><span class="o">=</span><span class="s">&quot;submit&quot;</span> <span class="p">/&gt;</span>
  <span class="p">&lt;/</span><span class="nt">form</span><span class="p">&gt;</span>

  {% if image_url %}
    <span class="p">&lt;</span><span class="nt">p</span><span class="p">&gt;</span>File uploaded at: <span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">&quot;{{ image_url }}&quot;</span><span class="p">&gt;</span>{{ image_url }}<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;&lt;/</span><span class="nt">p</span><span class="p">&gt;</span>
  {% endif %}

{% endblock %}
</code></pre></div>

<p><em>app/hello_django/urls.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>
<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span>
<span class="kn">from</span> <span class="nn">django.conf</span> <span class="kn">import</span> <span class="n">settings</span>
<span class="kn">from</span> <span class="nn">django.conf.urls.static</span> <span class="kn">import</span> <span class="n">static</span>

<span class="kn">from</span> <span class="nn">upload.views</span> <span class="kn">import</span> <span class="n">image_upload</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
    <span class="n">path</span><span class="p">(</span><span class="s2">&quot;&quot;</span><span class="p">,</span> <span class="n">image_upload</span><span class="p">,</span> <span class="n">name</span><span class="o">=</span><span class="s2">&quot;upload&quot;</span><span class="p">),</span>
    <span class="n">path</span><span class="p">(</span><span class="s2">&quot;admin/&quot;</span><span class="p">,</span> <span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">urls</span><span class="p">),</span>
<span class="p">]</span>

<span class="k">if</span> <span class="nb">bool</span><span class="p">(</span><span class="n">settings</span><span class="o">.</span><span class="n">DEBUG</span><span class="p">):</span>
    <span class="n">urlpatterns</span> <span class="o">+=</span> <span class="n">static</span><span class="p">(</span><span class="n">settings</span><span class="o">.</span><span class="n">MEDIA_URL</span><span class="p">,</span> <span class="n">document_root</span><span class="o">=</span><span class="n">settings</span><span class="o">.</span><span class="n">MEDIA_ROOT</span><span class="p">)</span>
</code></pre></div>

<p><em>app/hello_django/settings.py</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="n">MEDIA_URL</span> <span class="o">=</span> <span class="s2">&quot;/media/&quot;</span>
<span class="n">MEDIA_ROOT</span> <span class="o">=</span> <span class="n">BASE_DIR</span> <span class="o">/</span> <span class="s2">&quot;mediafiles&quot;</span>
</code></pre></div>

<h3 id="development_1">Development</h3>
<p>Test:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose up -d --build
</code></pre></div>

<p>You should be able to upload an image at <a href="http://localhost:8000/">http://localhost:8000/</a>, and then view the image at <a href="http://localhost:8000/media/IMAGE_FILE_NAME">http://localhost:8000/media/IMAGE_FILE_NAME</a>.</p>
<h3 id="production_1">Production</h3>
<p>For production, add another volume to the <code>web</code> and <code>nginx</code> services:</p>
<div class="codehilite"><pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">&#39;3.8&#39;</span><span class="w"></span>

<span class="nt">services</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">web</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./app</span><span class="w"></span>
<span class="w">      </span><span class="nt">dockerfile</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Dockerfile.prod</span><span class="w"></span>
<span class="w">    </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000</span><span class="w"></span>
<span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">static_volume:/home/app/web/staticfiles</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">media_volume:/home/app/web/mediafiles</span><span class="w"></span>
<span class="w">    </span><span class="nt">expose</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">8000</span><span class="w"></span>
<span class="w">    </span><span class="nt">env_file</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./.env.prod</span><span class="w"></span>
<span class="w">    </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">db</span><span class="w"></span>
<span class="w">  </span><span class="nt">db</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">postgres:13.0-alpine</span><span class="w"></span>
<span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">postgres_data:/var/lib/postgresql/data/</span><span class="w"></span>
<span class="w">    </span><span class="nt">env_file</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./.env.prod.db</span><span class="w"></span>
<span class="w">  </span><span class="nt">nginx</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./nginx</span><span class="w"></span>
<span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">static_volume:/home/app/web/staticfiles</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">media_volume:/home/app/web/mediafiles</span><span class="w"></span>
<span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1337:80</span><span class="w"></span>
<span class="w">    </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">web</span><span class="w"></span>

<span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">postgres_data</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">static_volume</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">media_volume</span><span class="p">:</span><span class="w"></span>
</code></pre></div>

<p>Create the "/home/app/web/mediafiles" folder in <em>Dockerfile.prod</em>:</p>
<div class="codehilite"><pre><span></span><code>...

<span class="c"># create the appropriate directories</span>
<span class="k">ENV</span><span class="w"> </span><span class="nv">HOME</span><span class="o">=</span>/home/app
<span class="k">ENV</span><span class="w"> </span><span class="nv">APP_HOME</span><span class="o">=</span>/home/app/web
<span class="k">RUN</span><span class="w"> </span>mkdir <span class="nv">$APP_HOME</span>
<span class="k">RUN</span><span class="w"> </span>mkdir <span class="nv">$APP_HOME</span>/staticfiles
<span class="k">RUN</span><span class="w"> </span>mkdir <span class="nv">$APP_HOME</span>/mediafiles
<span class="k">WORKDIR</span><span class="w"> </span><span class="s">$APP_HOME</span>

...
</code></pre></div>

<p>Update the Nginx config again:</p>
<div class="codehilite"><pre><span></span><code>upstream hello_django <span class="o">{</span>
    server web:8000<span class="p">;</span>
<span class="o">}</span>

server <span class="o">{</span>

listen <span class="m">80</span><span class="p">;</span>

location / <span class="o">{</span>
        proxy_pass http://hello_django<span class="p">;</span>
        proxy_set_header X-Forwarded-For <span class="nv">$proxy_add_x_forwarded_for</span><span class="p">;</span>
        proxy_set_header Host <span class="nv">$host</span><span class="p">;</span>
        proxy_redirect off<span class="p">;</span>
    <span class="o">}</span>

location /static/ <span class="o">{</span>
        <span class="nb">alias</span> /home/app/web/staticfiles/<span class="p">;</span>
<span class="o">}</span>

location /media/ <span class="o">{</span>
        <span class="nb">alias</span> /home/app/web/mediafiles/<span class="p">;</span>
<span class="o">}</span>

<span class="o">}</span>
</code></pre></div>

<p>Re-build:</p>
<div class="codehilite"><pre><span></span><code>$ docker-compose down -v

$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml <span class="nb">exec</span> web python manage.py migrate --noinput
$ docker-compose -f docker-compose.prod.yml <span class="nb">exec</span> web python manage.py collectstatic --no-input --clear
</code></pre></div>

<p>Test it out one final time:</p>
<ol>
<li>Upload an image at <a href="http://localhost:1337/">http://localhost:1337/</a>.</li>
<li>Then, view the image at <a href="http://localhost:1337/media/IMAGE_FILE_NAME">http://localhost:1337/media/IMAGE_FILE_NAME</a>.</li>
</ol>


<h2 id="conclusion">Conclusion</h2>
<p>In this tutorial, we walked through how to containerize a Django web application with Postgres for development. We also created a production-ready Docker Compose file that adds Gunicorn and Nginx into the mix to handle static and media files. You can now test out a production setup locally.</p>
<p>In terms of actual deployment to a production environment, you'll probably want to use a:</p>
<ol>
<li>Fully managed database service -- like <a href="https://aws.amazon.com/rds/">RDS</a> or <a href="https://cloud.google.com/sql/">Cloud SQL</a> -- rather than managing your own Postgres instance within a container.</li>
<li>Non-root user for the <code>db</code> and <code>nginx</code> services</li>
</ol>


