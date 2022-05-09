---
layout: post
title: Dockerizing-Django-with-Postgres-Gunicorn-and-Nginx
date: 2019-02-27 16:20:23 +0900
category: Python
tag: Python
---

<h2 id="project-setup">Project Setup</h2>
<p>Create a new project directory along with a new Django project:</p>
<pre><span></span><code>$ mkdir django-on-docker <span class="o">&amp;&amp;</span> <span class="nb">cd</span> django-on-docker
$ mkdir app <span class="o">&amp;&amp;</span> <span class="nb">cd</span> app
$ python3.9 -m venv env
$ <span class="nb">source</span> env/bin/activate
<span class="o">(</span>env<span class="o">)</span>$

<span class="o">(</span>env<span class="o">)</span>$ pip install <span class="nv">django</span><span class="o">==</span><span class="m">3</span>.2.6
<span class="o">(</span>env<span class="o">)</span>$ django-admin.py startproject hello_django .
<span class="o">(</span>env<span class="o">)</span>$ python manage.py migrate
<span class="o">(</span>env<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>Feel free to swap out virtualenv and Pip for <a href="https://python-poetry.org/">Poetry</a> or <a href="https://github.com/pypa/pipenv">Pipenv</a>. For more, review <a href="https://testdriven.io/blog/python-environments/">Modern Python Environments</a>.</p>
<p>Navigate to <a href="http://localhost:8000/">http://localhost:8000/</a> to view the Django welcome screen. Kill the server once done. Then, exit from and remove the virtual environment. We now have a simple Django project to work with.</p>
<p>Create a <em>requirements.txt</em> file in the "app" directory and add Django as a dependency:</p>
<pre><span></span><code>Django==3.2.6
</code></pre>
<p>Since we'll be moving to Postgres, go ahead and remove the <em>db.sqlite3</em> file from the "app" directory.</p>
<p>Your project directory should look like:</p>
<pre><span></span><code>└── app
├── hello_django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
</code></pre>
<h2 id="docker">Docker</h2>
<p>Install <a href="https://docs.docker.com/install/">Docker</a>, if you don't already have it, then add a <em>Dockerfile</em> to the "app" directory:</p>
<pre><span></span><code><span class="c"># pull official base image</span>
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
</code></pre>
<p>So, we started with an <a href="https://github.com/gliderlabs/docker-alpine">Alpine</a>-based <a href="https://hub.docker.com/_/python/">Docker image</a> for Python 3.9.6. We then set a <a href="https://docs.docker.com/engine/reference/builder/#workdir">working directory</a> along with two environment variables:</p>
<ol>
<li><code>PYTHONDONTWRITEBYTECODE</code>: Prevents Python from writing pyc files to disc (equivalent to <code>python -B</code> <a href="https://docs.python.org/3/using/cmdline.html#id1">option</a>)</li>
<li><code>PYTHONUNBUFFERED</code>: Prevents Python from buffering stdout and stderr (equivalent to <code>python -u</code> <a href="https://docs.python.org/3/using/cmdline.html#cmdoption-u">option</a>)</li>
</ol>
<li><code>PYTHONDONTWRITEBYTECODE</code>: Prevents Python from writing pyc files to disc (equivalent to <code>python -B</code> <a href="https://docs.python.org/3/using/cmdline.html#id1">option</a>)</li>
<li><code>PYTHONUNBUFFERED</code>: Prevents Python from buffering stdout and stderr (equivalent to <code>python -u</code> <a href="https://docs.python.org/3/using/cmdline.html#cmdoption-u">option</a>)</li>
<p>Finally, we updated Pip, copied over the <em>requirements.txt</em> file, installed the dependencies, and copied over the Django project itself.</p>
<p>Review <a href="https://mherman.org/presentations/dockercon-2018">Docker for Python Developers</a> for more on structuring Dockerfiles as well as some best practices for configuring Docker for Python-based development.</p>
<p>Next, add a <em>docker-compose.yml</em> file to the project root:</p>
<pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">'3.8'</span><span class="w"></span>

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
</code></pre>
<p>Review the <a href="https://docs.docker.com/compose/compose-file/">Compose file reference</a> for info on how this file works.</p>
<p>Update the <code>SECRET_KEY</code>, <code>DEBUG</code>, and <code>ALLOWED_HOSTS</code> variables in <em>settings.py</em>:</p>
<pre><span></span><code><span class="n">SECRET_KEY</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"SECRET_KEY"</span><span class="p">)</span>

<span class="n">DEBUG</span> <span class="o">=</span> <span class="nb">int</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"DEBUG"</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="mi">0</span><span class="p">))</span>

<span class="c1"># 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.</span>
<span class="c1"># For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'</span>
<span class="n">ALLOWED_HOSTS</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"DJANGO_ALLOWED_HOSTS"</span><span class="p">)</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s2">" "</span><span class="p">)</span>
</code></pre>
<p>Make sure to add the import to the top:</p>
<pre><span></span><code><span class="kn">import</span> <span class="nn">os</span>
</code></pre>
<p>Then, create a <em>.env.dev</em> file in the project root to store environment variables for development:</p>
<pre><span></span><code>DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
</code></pre>
<p>Build the image:</p>
<pre><span></span><code>$ docker-compose build
</code></pre>
<p>Once the image is built, run the container:</p>
<pre><span></span><code>$ docker-compose up -d
</code></pre>
<p>Navigate to <a href="http://localhost:8000/">http://localhost:8000/</a> to again view the welcome screen.</p>
<p>Check for errors in the logs if this doesn't work via <code>docker-compose logs -f</code>.</p>
<h2 id="postgres">Postgres</h2>
<p>To configure Postgres, we'll need to add a new service to the <em>docker-compose.yml</em> file, update the Django settings, and install <a href="http://initd.org/psycopg/">Psycopg2</a>.</p>
<p>First, add a new service called <code>db</code> to <em>docker-compose.yml</em>:</p>
<pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">'3.8'</span><span class="w"></span>

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
</code></pre>
<p>To persist the data beyond the life of the container we configured a volume. This config will bind <code>postgres_data</code> to the "/var/lib/postgresql/data/" directory in the container.</p>
<p>We also added an environment key to define a name for the default database and set a username and password.</p>
<p>Review the "Environment Variables" section of the <a href="https://hub.docker.com/_/postgres">Postgres Docker Hub page</a> for more info.</p>
<p>We'll need some new environment variables for the <code>web</code> service as well, so update <em>.env.dev</em> like so:</p>
<pre><span></span><code>DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
</code></pre>
<p>Update the <code>DATABASES</code> dict in <em>settings.py</em>:</p>
<pre><span></span><code><span class="n">DATABASES</span> <span class="o">=</span> <span class="p">{</span>
<span class="s2">"default"</span><span class="p">:</span> <span class="p">{</span>
<span class="s2">"ENGINE"</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"SQL_ENGINE"</span><span class="p">,</span> <span class="s2">"django.db.backends.sqlite3"</span><span class="p">),</span>
<span class="s2">"NAME"</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"SQL_DATABASE"</span><span class="p">,</span> <span class="n">BASE_DIR</span> <span class="o">/</span> <span class="s2">"db.sqlite3"</span><span class="p">),</span>
<span class="s2">"USER"</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"SQL_USER"</span><span class="p">,</span> <span class="s2">"user"</span><span class="p">),</span>
<span class="s2">"PASSWORD"</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"SQL_PASSWORD"</span><span class="p">,</span> <span class="s2">"password"</span><span class="p">),</span>
<span class="s2">"HOST"</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"SQL_HOST"</span><span class="p">,</span> <span class="s2">"localhost"</span><span class="p">),</span>
<span class="s2">"PORT"</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s2">"SQL_PORT"</span><span class="p">,</span> <span class="s2">"5432"</span><span class="p">),</span>
<span class="p">}</span>
<span class="p">}</span>
</code></pre>
<p>Here, the database is configured based on the environment variables that we just defined. Take note of the default values.</p>
<p>Update the Dockerfile to install the appropriate packages required for Psycopg2:</p>
<pre><span></span><code><span class="c"># pull official base image</span>
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
</code></pre>
<p>Add Psycopg2 to <em>requirements.txt</em>:</p>
<pre><span></span><code>Django==3.2.6
psycopg2-binary==2.9.1
</code></pre>
<p>Review <a href="https://github.com/psycopg/psycopg2/issues/684">this GitHub Issue</a> for more info on installing Psycopg2 in an Alpine-based Docker Image.</p>
<p>Build the new image and spin up the two containers:</p>
<pre><span></span><code>$ docker-compose up -d --build
</code></pre>
<p>Run the migrations:</p>
<pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py migrate --noinput
</code></pre>
<p>Get the following error?</p>
<pre><span></span>django.db.utils.OperationalError: FATAL:  database <span class="s2">"hello_django_dev"</span> does not exist
</pre>
<p>Run <code>docker-compose down -v</code> to remove the volumes along with the containers. Then, re-build the images, run the containers, and apply the migrations.</p>
<p>Ensure the default Django tables were created:</p>
<pre><span></span><code>$ docker-compose <span class="nb">exec</span> db psql --username<span class="o">=</span>hello_django --dbname<span class="o">=</span>hello_django_dev

psql <span class="o">(</span><span class="m">13</span>.0<span class="o">)</span>
Type <span class="s2">"help"</span> <span class="k">for</span> help.

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
You are now connected to database <span class="s2">"hello_django_dev"</span> as user <span class="s2">"hello_django"</span>.

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
</code></pre>
<p>You can check that the volume was created as well by running:</p>
<pre><span></span><code>$ docker volume inspect django-on-docker_postgres_data
</code></pre>
<p>You should see something similar to:</p>
<pre><span></span><code><span class="o">[</span>
<span class="o">{</span>
<span class="s2">"CreatedAt"</span>: <span class="s2">"2021-08-23T15:49:08Z"</span>,
<span class="s2">"Driver"</span>: <span class="s2">"local"</span>,
<span class="s2">"Labels"</span>: <span class="o">{</span>
<span class="s2">"com.docker.compose.project"</span>: <span class="s2">"django-on-docker"</span>,
<span class="s2">"com.docker.compose.version"</span>: <span class="s2">"1.29.2"</span>,
<span class="s2">"com.docker.compose.volume"</span>: <span class="s2">"postgres_data"</span>
<span class="o">}</span>,
<span class="s2">"Mountpoint"</span>: <span class="s2">"/var/lib/docker/volumes/django-on-docker_postgres_data/_data"</span>,
<span class="s2">"Name"</span>: <span class="s2">"django-on-docker_postgres_data"</span>,
<span class="s2">"Options"</span>: null,
<span class="s2">"Scope"</span>: <span class="s2">"local"</span>
<span class="o">}</span>
<span class="o">]</span>
</code></pre>
<p>Next, add an <em>entrypoint.sh</em> file to the "app" directory to verify that Postgres is healthy <em>before</em> applying the migrations and running the Django development server:</p>
<pre><span></span><code><span class="ch">#!/bin/sh</span>

<span class="k">if</span> <span class="o">[</span> <span class="s2">"</span><span class="nv">$DATABASE</span><span class="s2">"</span> <span class="o">=</span> <span class="s2">"postgres"</span> <span class="o">]</span>
<span class="k">then</span>
<span class="nb">echo</span> <span class="s2">"Waiting for postgres..."</span>

<span class="k">while</span> ! nc -z <span class="nv">$SQL_HOST</span> <span class="nv">$SQL_PORT</span><span class="p">;</span> <span class="k">do</span>
sleep <span class="m">0</span>.1
<span class="k">done</span>

<span class="nb">echo</span> <span class="s2">"PostgreSQL started"</span>
<span class="k">fi</span>

python manage.py flush --no-input
python manage.py migrate

<span class="nb">exec</span> <span class="s2">"</span><span class="nv">$@</span><span class="s2">"</span>
</code></pre>
<p>Update the file permissions locally:</p>
<pre><span></span><code>$ chmod +x app/entrypoint.sh
</code></pre>
<p>Then, update the Dockerfile to copy over the <em>entrypoint.sh</em> file and run it as the Docker <a href="https://docs.docker.com/engine/reference/builder/#entrypoint">entrypoint</a> command:</p>
<pre><span></span><code><span class="c"># pull official base image</span>
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
<span class="k">RUN</span><span class="w"> </span>sed -i <span class="s1">'s/\r$//g'</span> /usr/src/app/entrypoint.sh
<span class="k">RUN</span><span class="w"> </span>chmod +x /usr/src/app/entrypoint.sh

<span class="c"># copy project</span>
<span class="k">COPY</span><span class="w"> </span>. .

<span class="c"># run entrypoint.sh</span>
<span class="k">ENTRYPOINT</span><span class="w"> </span><span class="p">[</span><span class="s2">"/usr/src/app/entrypoint.sh"</span><span class="p">]</span>
</code></pre>
<p>Add the <code>DATABASE</code> environment variable to <em>.env.dev</em>:</p>
<pre><span></span><code>DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
</code></pre>
<p>Test it out again:</p>
<ol>
<li>Re-build the images</li>
<li>Run the containers</li>
<li>Try <a href="http://localhost:8000/">http://localhost:8000/</a></li>
</ol>
<li>Re-build the images</li>
<li>Run the containers</li>
<li>Try <a href="http://localhost:8000/">http://localhost:8000/</a></li>
<h3 id="notes">Notes</h3>
<p>First, despite adding Postgres, we can still create an independent Docker image for Django as long as the <code>DATABASE</code> environment variable is not set to <code>postgres</code>. To test, build a new image and then run a new container:</p>
<pre><span></span><code>$ docker build -f ./app/Dockerfile -t hello_django:latest ./app
$ docker run -d <span class="se">\</span>
-p <span class="m">8006</span>:8000 <span class="se">\</span>
-e <span class="s2">"SECRET_KEY=please_change_me"</span> -e <span class="s2">"DEBUG=1"</span> -e <span class="s2">"DJANGO_ALLOWED_HOSTS=*"</span> <span class="se">\</span>
hello_django python /usr/src/app/manage.py runserver <span class="m">0</span>.0.0.0:8000
</code></pre>
<p>You should be able to view the welcome page at <a href="http://localhost:8006/">http://localhost:8006</a></p>
<p>Second, you may want to comment out the database flush and migrate commands in the <em>entrypoint.sh</em> script so they don't run on every container start or re-start:</p>
<pre><span></span><code><span class="ch">#!/bin/sh</span>

<span class="k">if</span> <span class="o">[</span> <span class="s2">"</span><span class="nv">$DATABASE</span><span class="s2">"</span> <span class="o">=</span> <span class="s2">"postgres"</span> <span class="o">]</span>
<span class="k">then</span>
<span class="nb">echo</span> <span class="s2">"Waiting for postgres..."</span>

<span class="k">while</span> ! nc -z <span class="nv">$SQL_HOST</span> <span class="nv">$SQL_PORT</span><span class="p">;</span> <span class="k">do</span>
sleep <span class="m">0</span>.1
<span class="k">done</span>

<span class="nb">echo</span> <span class="s2">"PostgreSQL started"</span>
<span class="k">fi</span>

<span class="c1"># python manage.py flush --no-input</span>
<span class="c1"># python manage.py migrate</span>

<span class="nb">exec</span> <span class="s2">"</span><span class="nv">$@</span><span class="s2">"</span>
</code></pre>
<p>Instead, you can run them manually, after the containers spin up, like so:</p>
<pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py flush --no-input
$ docker-compose <span class="nb">exec</span> web python manage.py migrate
</code></pre>
<h2 id="gunicorn">Gunicorn</h2>
<p>Moving along, for production environments, let's add <a href="https://gunicorn.org/">Gunicorn</a>, a production-grade WSGI server, to the requirements file:</p>
<pre><span></span><code>Django==3.2.6
gunicorn==20.1.0
psycopg2-binary==2.9.1
</code></pre>
<p>Curious about WSGI and Gunicorn? Review the <a href="https://testdriven.io/courses/python-web-framework/wsgi/">WSGI</a> chapter from the <a href="https://testdriven.io/courses/python-web-framework/">Building Your Own Python Web Framework</a> course.</p>
<p>Since we still want to use Django's built-in server in development, create a new compose file called <em>docker-compose.prod.yml</em> for production:</p>
<pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">'3.8'</span><span class="w"></span>

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
</code></pre>
<p>If you have multiple environments, you may want to look at using a <a href="https://docs.docker.com/compose/extends/">docker-compose.override.yml</a> configuration file. With this approach, you'd add your base config to a <em>docker-compose.yml</em> file and then use a <em>docker-compose.override.yml</em> file to override those config settings based on the environment.</p>
<p>Take note of the default <code>command</code>. We're running Gunicorn rather than the Django development server. We also removed the volume from the <code>web</code> service since we don't need it in production. Finally, we're using <a href="https://docs.docker.com/compose/env-file/">separate environment variable files</a> to define environment variables for both services that will be passed to the container at runtime.</p>
<p><em>.env.prod</em>:</p>
<pre><span></span><code>DEBUG=0
SECRET_KEY=change_me
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_prod
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
</code></pre>
<p><em>.env.prod.db</em>:</p>
<pre><span></span><code>POSTGRES_USER=hello_django
POSTGRES_PASSWORD=hello_django
POSTGRES_DB=hello_django_prod
</code></pre>
<p>Add the two files to the project root. You'll probably want to keep them out of version control, so add them to a <em>.gitignore</em> file.</p>
<p>Bring <a href="https://docs.docker.com/compose/reference/down/">down</a> the development containers (and the associated volumes with the <code>-v</code> flag):</p>
<pre><span></span><code>$ docker-compose down -v
</code></pre>
<p>Then, build the production images and spin up the containers:</p>
<pre><span></span><code>$ docker-compose -f docker-compose.prod.yml up -d --build
</code></pre>
<p>Verify that the <code>hello_django_prod</code> database was created along with the default Django tables. Test out the admin page at <a href="http://localhost:8000/admin">http://localhost:8000/admin</a>. The static files are not being loaded anymore. This is expected since Debug mode is off. We'll fix this shortly.</p>
<p>Again, if the container fails to start, check for errors in the logs via <code>docker-compose -f docker-compose.prod.yml logs -f</code>.</p>
<h2 id="production-dockerfile">Production Dockerfile</h2>
<p>Did you notice that we're still running the database <a href="https://docs.djangoproject.com/en/2.2/ref/django-admin/#flush">flush</a> (which clears out the database) and migrate commands every time the container is run? This is fine in development, but let's create a new entrypoint file for production.</p>
<p><em>entrypoint.prod.sh</em>:</p>
<pre><span></span><code><span class="ch">#!/bin/sh</span>

<span class="k">if</span> <span class="o">[</span> <span class="s2">"</span><span class="nv">$DATABASE</span><span class="s2">"</span> <span class="o">=</span> <span class="s2">"postgres"</span> <span class="o">]</span>
<span class="k">then</span>
<span class="nb">echo</span> <span class="s2">"Waiting for postgres..."</span>

<span class="k">while</span> ! nc -z <span class="nv">$SQL_HOST</span> <span class="nv">$SQL_PORT</span><span class="p">;</span> <span class="k">do</span>
sleep <span class="m">0</span>.1
<span class="k">done</span>

<span class="nb">echo</span> <span class="s2">"PostgreSQL started"</span>
<span class="k">fi</span>

<span class="nb">exec</span> <span class="s2">"</span><span class="nv">$@</span><span class="s2">"</span>
</code></pre>
<p>Update the file permissions locally:</p>
<pre><span></span><code>$ chmod +x app/entrypoint.prod.sh
</code></pre>
<p>To use this file, create a new Dockerfile called <em>Dockerfile.prod</em> for use with production builds:</p>
<pre><span></span><code><span class="c">###########</span>
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
<span class="k">RUN</span><span class="w"> </span>sed -i <span class="s1">'s/\r$//g'</span>  <span class="nv">$APP_HOME</span>/entrypoint.prod.sh
<span class="k">RUN</span><span class="w"> </span>chmod +x  <span class="nv">$APP_HOME</span>/entrypoint.prod.sh

<span class="c"># copy project</span>
<span class="k">COPY</span><span class="w"> </span>. <span class="nv">$APP_HOME</span>

<span class="c"># chown all the files to the app user</span>
<span class="k">RUN</span><span class="w"> </span>chown -R app:app <span class="nv">$APP_HOME</span>

<span class="c"># change to the app user</span>
<span class="k">USER</span><span class="w"> </span><span class="s">app</span>

<span class="c"># run entrypoint.prod.sh</span>
<span class="k">ENTRYPOINT</span><span class="w"> </span><span class="p">[</span><span class="s2">"/home/app/web/entrypoint.prod.sh"</span><span class="p">]</span>
</code></pre>
<p>Here, we used a Docker <a href="https://docs.docker.com/develop/develop-images/multistage-build/">multi-stage build</a> to reduce the final image size. Essentially, <code>builder</code> is a temporary image that's used for building the Python wheels. The wheels are then copied over to the final production image and the <code>builder</code> image is discarded.</p>
<p>You could take the <a href="https://stackoverflow.com/a/53101932/1799408">multi-stage build approach</a> a step further and use a single <em>Dockerfile</em> instead of creating two Dockerfiles. Think of the pros and cons of using this approach over two different files.</p>
<p>Did you notice that we created a non-root user? By default, Docker runs container processes as root inside of a container. This is a bad practice since attackers can gain root access to the Docker host if they manage to break out of the container. If you're root in the container, you'll be root on the host.</p>
<p>Update the <code>web</code> service within the <em>docker-compose.prod.yml</em> file to build with <em>Dockerfile.prod</em>:</p>
<pre><span></span><code><span class="nt">web</span><span class="p">:</span><span class="w"></span>
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
</code></pre>
<p>Try it out:</p>
<pre><span></span><code>$ docker-compose -f docker-compose.prod.yml down -v
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml <span class="nb">exec</span> web python manage.py migrate --noinput
</code></pre>
<h2 id="nginx">Nginx</h2>
<p>Next, let's add Nginx into the mix to act as a <a href="https://www.nginx.com/resources/glossary/reverse-proxy-server/">reverse proxy</a> for Gunicorn to handle client requests as well as serve up static files.</p>
<p>Add the service to <em>docker-compose.prod.yml</em>:</p>
<pre><span></span><code><span class="nt">nginx</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./nginx</span><span class="w"></span>
<span class="w">  </span><span class="nt">ports</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1337:80</span><span class="w"></span>
<span class="w">  </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">web</span><span class="w"></span>
</code></pre>
<p>Then, in the local project root, create the following files and folders:</p>
<pre><span></span><code>└── nginx
├── Dockerfile
└── nginx.conf
</code></pre>
<p><em>Dockerfile</em>:</p>
<pre><span></span><code><span class="k">FROM</span><span class="w"> </span><span class="s">nginx:1.21-alpine</span>

<span class="k">RUN</span><span class="w"> </span>rm /etc/nginx/conf.d/default.conf
<span class="k">COPY</span><span class="w"> </span>nginx.conf /etc/nginx/conf.d
</code></pre>
<p><em>nginx.conf</em>:</p>
<pre><span></span><code>upstream hello_django <span class="o">{</span>
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
</code></pre>
<p>Review <a href="https://docs.nginx.com/nginx/admin-guide/web-server/app-gateway-uwsgi-django/">Using NGINX and NGINX Plus as an Application Gateway with uWSGI and Django</a> for more info on configuring Nginx to work with Django.</p>
<p>Then, update the <code>web</code> service, in <em>docker-compose.prod.yml</em>, replacing <code>ports</code> with <code>expose</code>:</p>
<pre><span></span><code><span class="nt">web</span><span class="p">:</span><span class="w"></span>
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
</code></pre>
<p>Now, port 8000 is only exposed internally, to other Docker services. The port will no longer be published to the host machine.</p>
<p>For more on ports vs expose, review <a href="https://stackoverflow.com/questions/40801772/what-is-the-difference-between-docker-compose-ports-vs-expose">this</a> Stack Overflow question.</p>
<p>Test it out again.</p>
<pre><span></span><code>$ docker-compose -f docker-compose.prod.yml down -v
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml <span class="nb">exec</span> web python manage.py migrate --noinput
</code></pre>
<p>Ensure the app is up and running at <a href="http://localhost:1337/">http://localhost:1337</a>.</p>
<p>Your project structure should now look like:</p>
<pre><span></span><code>├── .env.dev
├── .env.prod
├── .env.prod.db
├── .gitignore
├── app
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── entrypoint.prod.sh
│   ├── entrypoint.sh
│   ├── hello_django
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── requirements.txt
├── docker-compose.prod.yml
├── docker-compose.yml
└── nginx
├── Dockerfile
└── nginx.conf
</code></pre>
<p>Bring the containers down once done:</p>
<pre><span></span><code>$ docker-compose -f docker-compose.prod.yml down -v
</code></pre>
<p>Since Gunicorn is an application server, it will not serve up static files. So, how should both static and media files be handled in this particular configuration?</p>
<h2 id="static-files">Static Files</h2>
<p>Update <em>settings.py</em>:</p>
<pre><span></span><code><span class="nv">STATIC_URL</span> <span class="o">=</span> <span class="s2">"/static/"</span>
<span class="nv">STATIC_ROOT</span> <span class="o">=</span> BASE_DIR / <span class="s2">"staticfiles"</span>
</code></pre>
<h3 id="development">Development</h3>
<p>Now, any request to <code>http://localhost:8000/static/*</code> will be served from the "staticfiles" directory.</p>
<p>To test, first re-build the images and spin up the new containers per usual. Ensure static files are still being served correctly at <a href="http://localhost:8000/admin">http://localhost:8000/admin</a>.</p>
<h3 id="production">Production</h3>
<p>For production, add a volume to the <code>web</code> and <code>nginx</code> services in <em>docker-compose.prod.yml</em> so that each container will share a directory named "staticfiles":</p>
<pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">'3.8'</span><span class="w"></span>

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
</code></pre>
<p>We need to also create the "/home/app/web/staticfiles" folder in <em>Dockerfile.prod</em>:</p>
<pre><span></span><code>...

<span class="c"># create the appropriate directories</span>
<span class="k">ENV</span><span class="w"> </span><span class="nv">HOME</span><span class="o">=</span>/home/app
<span class="k">ENV</span><span class="w"> </span><span class="nv">APP_HOME</span><span class="o">=</span>/home/app/web
<span class="k">RUN</span><span class="w"> </span>mkdir <span class="nv">$APP_HOME</span>
<span class="k">RUN</span><span class="w"> </span>mkdir <span class="nv">$APP_HOME</span>/staticfiles
<span class="k">WORKDIR</span><span class="w"> </span><span class="s">$APP_HOME</span>

...
</code></pre>
<p>Why is this necessary?</p>
<p>Docker Compose normally mounts named volumes as root. And since we're using a non-root user, we'll get a permission denied error when the <code>collectstatic</code> command is run if the directory does not already exist</p>
<p>To get around this, you can either:</p>
<ol>
<li>Create the folder in the Dockerfile (<a href="https://github.com/docker/compose/issues/3270#issuecomment-206214034">source</a>)</li>
<li>Change the permissions of the directory after it's mounted (<a href="https://stackoverflow.com/a/40510068/1799408">source</a>)</li>
</ol>
<li>Create the folder in the Dockerfile (<a href="https://github.com/docker/compose/issues/3270#issuecomment-206214034">source</a>)</li>
<li>Change the permissions of the directory after it's mounted (<a href="https://stackoverflow.com/a/40510068/1799408">source</a>)</li>
<p>We used the former.</p>
<p>Next, update the Nginx configuration to route static file requests to the "staticfiles" folder:</p>
<pre><span></span><code>upstream hello_django <span class="o">{</span>
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
</code></pre>
<p>Spin down the development containers:</p>
<pre><span></span><code>$ docker-compose down -v
</code></pre>
<p>Test:</p>
<pre><span></span><code>$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml <span class="nb">exec</span> web python manage.py migrate --noinput
$ docker-compose -f docker-compose.prod.yml <span class="nb">exec</span> web python manage.py collectstatic --no-input --clear


</code>
</pre>
<p>Again, requests to <code>http://localhost:1337/static/*</code> will be served from the "staticfiles" directory.</p>
<p>Navigate to <a href="http://localhost:1337/admin">http://localhost:1337/admin</a> and ensure the static assets load correctly.</p>
<p>You can also verify in the logs -- via <code>docker-compose -f docker-compose.prod.yml logs -f</code> -- that requests to the static files are served up successfully via Nginx:</p>

<textarea rows="10" cols="150" readonly>
nginx_1  | 192.168.144.1 - - [23/Aug/2021:20:11:00 +0000] "GET /admin/ HTTP/1.1" 302 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36" "-"
nginx_1  | 192.168.144.1 - - [23/Aug/2021:20:11:00 +0000] "GET /admin/login/?next=/admin/ HTTP/1.1" 200 2214 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36" "-"
nginx_1  | 192.168.144.1 - - [23/Aug/2021:20:11:00 +0000] "GET /static/admin/css/base.css HTTP/1.1" 304 0 "http://localhost:1337/admin/login/?next=/admin/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36" "-"
nginx_1  | 192.168.144.1 - - [23/Aug/2021:20:11:00 +0000] "GET /static/admin/css/nav_sidebar.css HTTP/1.1" 304 0 "http://localhost:1337/admin/login/?next=/admin/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36" "-"
nginx_1  | 192.168.144.1 - - [23/Aug/2021:20:11:00 +0000] "GET /static/admin/css/responsive.css HTTP/1.1" 304 0 "http://localhost:1337/admin/login/?next=/admin/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36" "-"
nginx_1  | 192.168.144.1 - - [23/Aug/2021:20:11:00 +0000] "GET /static/admin/css/login.css HTTP/1.1" 304 0 "http://localhost:1337/admin/login/?next=/admin/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36" "-"
nginx_1  | 192.168.144.1 - - [23/Aug/2021:20:11:00 +0000] "GET /static/admin/js/nav_sidebar.js HTTP/1.1" 304 0 "http://localhost:1337/admin/login/?next=/admin/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36" "-"
nginx_1  | 192.168.144.1 - - [23/Aug/2021:20:11:00 +0000] "GET /static/admin/css/fonts.css HTTP/1.1" 304 0 "http://localhost:1337/static/admin/css/base.css" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36" "-"
nginx_1  | 192.168.144.1 - - [23/Aug/2021:20:11:00 +0000] "GET /static/admin/fonts/Roboto-Regular-webfont.woff HTTP/1.1" 304 0 "http://localhost:1337/static/admin/css/fonts.css" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36" "-"
nginx_1  | 192.168.144.1 - - [23/Aug/2021:20:11:00 +0000] "GET /static/admin/fonts/Roboto-Light-webfont.woff HTTP/1.1" 304 0 "http://localhost:1337/static/admin/css/fonts.css" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36" "-"
</textarea>




<p>Bring the containers once done:</p>
<pre><span></span><code>$ docker-compose -f docker-compose.prod.yml down -v
</code></pre>
<h2 id="media-files">Media Files</h2>
<p>To test out the handling of media files, start by creating a new Django app:</p>
<pre><span></span><code>$ docker-compose up -d --build
$ docker-compose <span class="nb">exec</span> web python manage.py startapp upload
</code></pre>
<p>Add the new app to the <code>INSTALLED_APPS</code> list in <em>settings.py</em>:</p>
<pre><span></span><code><span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
<span class="s2">"django.contrib.admin"</span><span class="p">,</span>
<span class="s2">"django.contrib.auth"</span><span class="p">,</span>
<span class="s2">"django.contrib.contenttypes"</span><span class="p">,</span>
<span class="s2">"django.contrib.sessions"</span><span class="p">,</span>
<span class="s2">"django.contrib.messages"</span><span class="p">,</span>
<span class="s2">"django.contrib.staticfiles"</span><span class="p">,</span>

<span class="s2">"upload"</span><span class="p">,</span>
<span class="p">]</span>
</code></pre>
<p><em>app/upload/views.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.shortcuts</span> <span class="kn">import</span> <span class="n">render</span>
<span class="kn">from</span> <span class="nn">django.core.files.storage</span> <span class="kn">import</span> <span class="n">FileSystemStorage</span>


<span class="k">def</span> <span class="nf">image_upload</span><span class="p">(</span><span class="n">request</span><span class="p">):</span>
<span class="k">if</span> <span class="n">request</span><span class="o">.</span><span class="n">method</span> <span class="o">==</span> <span class="s2">"POST"</span> <span class="ow">and</span> <span class="n">request</span><span class="o">.</span><span class="n">FILES</span><span class="p">[</span><span class="s2">"image_file"</span><span class="p">]:</span>
<span class="n">image_file</span> <span class="o">=</span> <span class="n">request</span><span class="o">.</span><span class="n">FILES</span><span class="p">[</span><span class="s2">"image_file"</span><span class="p">]</span>
<span class="n">fs</span> <span class="o">=</span> <span class="n">FileSystemStorage</span><span class="p">()</span>
<span class="n">filename</span> <span class="o">=</span> <span class="n">fs</span><span class="o">.</span><span class="n">save</span><span class="p">(</span><span class="n">image_file</span><span class="o">.</span><span class="n">name</span><span class="p">,</span> <span class="n">image_file</span><span class="p">)</span>
<span class="n">image_url</span> <span class="o">=</span> <span class="n">fs</span><span class="o">.</span><span class="n">url</span><span class="p">(</span><span class="n">filename</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">image_url</span><span class="p">)</span>
<span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="s2">"upload.html"</span><span class="p">,</span> <span class="p">{</span>
<span class="s2">"image_url"</span><span class="p">:</span> <span class="n">image_url</span>
<span class="p">})</span>
<span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="s2">"upload.html"</span><span class="p">)</span>
</code></pre>
<p>Add a "templates", directory to the "app/upload" directory, and then add a new template called <em>upload.html</em>:</p>
<pre><span></span><code>

<span class="p">&lt;</span><span class="nt">form</span> <span class="na">action</span><span class="o">=</span><span class="s">upload<span class="na">method</span><span class="o">=</span><span class="s">"post"</span> <span class="na">enctype</span><span class="o">=</span><span class="s">"multipart/form-data"</span><span class="p">&gt;</span>

<span class="p">&lt;</span><span class="nt">input</span> <span class="na">type</span><span class="o">=</span><span class="s">"file"</span> <span class="na">name</span><span class="o">=</span><span class="s">"image_file"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">input</span> <span class="na">type</span><span class="o">=</span><span class="s">"submit"</span> <span class="na">value</span><span class="o">=</span><span class="s">"submit"</span> <span class="p">/&gt;</span>
<span class="p">&lt;/</span><span class="nt">form</span><span class="p">&gt;</span>

{% if image_url %}
<span class="p">&lt;</span><span class="nt">p</span><span class="p">&gt;</span>File uploaded at: <span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"{{ image_url }}"</span><span class="p">&gt;</span>{{ image_url }}<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;&lt;/</span><span class="nt">p</span><span class="p">&gt;</span>
{% endif %}


</code></pre>
<p><em>app/hello_django/urls.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>
<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span>
<span class="kn">from</span> <span class="nn">django.conf</span> <span class="kn">import</span> <span class="n">settings</span>
<span class="kn">from</span> <span class="nn">django.conf.urls.static</span> <span class="kn">import</span> <span class="n">static</span>

<span class="kn">from</span> <span class="nn">upload.views</span> <span class="kn">import</span> <span class="n">image_upload</span>

<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">path</span><span class="p">(</span><span class="s2">""</span><span class="p">,</span> <span class="n">image_upload</span><span class="p">,</span> <span class="n">name</span><span class="o">=</span><span class="s2">"upload"</span><span class="p">),</span>
<span class="n">path</span><span class="p">(</span><span class="s2">"admin/"</span><span class="p">,</span> <span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">urls</span><span class="p">),</span>
<span class="p">]</span>

<span class="k">if</span> <span class="nb">bool</span><span class="p">(</span><span class="n">settings</span><span class="o">.</span><span class="n">DEBUG</span><span class="p">):</span>
<span class="n">urlpatterns</span> <span class="o">+=</span> <span class="n">static</span><span class="p">(</span><span class="n">settings</span><span class="o">.</span><span class="n">MEDIA_URL</span><span class="p">,</span> <span class="n">document_root</span><span class="o">=</span><span class="n">settings</span><span class="o">.</span><span class="n">MEDIA_ROOT</span><span class="p">)</span>
</code></pre>
<p><em>app/hello_django/settings.py</em>:</p>
<pre><span></span><code><span class="n">MEDIA_URL</span> <span class="o">=</span> <span class="s2">"/media/"</span>
<span class="n">MEDIA_ROOT</span> <span class="o">=</span> <span class="n">BASE_DIR</span> <span class="o">/</span> <span class="s2">"mediafiles"</span>
</code></pre>
<h3 id="development_1">Development</h3>
<p>Test:</p>
<pre><span></span><code>$ docker-compose up -d --build
</code></pre>
<p>You should be able to upload an image at <a href="http://localhost:8000/">http://localhost:8000/</a>, and then view the image at <a href="http://localhost:8000/media/IMAGE_FILE_NAME">http://localhost:8000/media/IMAGE_FILE_NAME</a>.</p>
<h3 id="production_1">Production</h3>
<p>For production, add another volume to the <code>web</code> and <code>nginx</code> services:</p>
<pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">'3.8'</span><span class="w"></span>

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
</code></pre>
<p>Create the "/home/app/web/mediafiles" folder in <em>Dockerfile.prod</em>:</p>
<pre><span></span><code>...

<span class="c"># create the appropriate directories</span>
<span class="k">ENV</span><span class="w"> </span><span class="nv">HOME</span><span class="o">=</span>/home/app
<span class="k">ENV</span><span class="w"> </span><span class="nv">APP_HOME</span><span class="o">=</span>/home/app/web
<span class="k">RUN</span><span class="w"> </span>mkdir <span class="nv">$APP_HOME</span>
<span class="k">RUN</span><span class="w"> </span>mkdir <span class="nv">$APP_HOME</span>/staticfiles
<span class="k">RUN</span><span class="w"> </span>mkdir <span class="nv">$APP_HOME</span>/mediafiles
<span class="k">WORKDIR</span><span class="w"> </span><span class="s">$APP_HOME</span>

...
</code></pre>
<p>Update the Nginx config again:</p>
<pre><span></span><code>upstream hello_django <span class="o">{</span>
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
</code></pre>
<p>Re-build:</p>
<pre><span></span><code>$ docker-compose down -v

$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml <span class="nb">exec</span> web python manage.py migrate --noinput
$ docker-compose -f docker-compose.prod.yml <span class="nb">exec</span> web python manage.py collectstatic --no-input --clear
</code></pre>
<p>Test it out one final time:</p>
<ol>
<li>Upload an image at <a href="http://localhost:1337/">http://localhost:1337/</a>.</li>
<li>Then, view the image at <a href="http://localhost:1337/media/IMAGE_FILE_NAME">http://localhost:1337/media/IMAGE_FILE_NAME</a>.</li>
</ol>
<li>Upload an image at <a href="http://localhost:1337/">http://localhost:1337/</a>.</li>
<li>Then, view the image at <a href="http://localhost:1337/media/IMAGE_FILE_NAME">http://localhost:1337/media/IMAGE_FILE_NAME</a>.</li>
<p>If you see an <code>413 Request Entity Too Large</code> error, you'll need to <a href="https://stackoverflow.com/a/28476755/1799408">increase the maximum allowed size of the client request body</a> in either the server or location context within the Nginx config.</p>
<p>Example:</p>
<pre><span></span>location / <span class="o">{</span>
proxy_pass http://hello_django<span class="p">;</span>
proxy_set_header X-Forwarded-For <span class="nv">$proxy_add_x_forwarded_for</span><span class="p">;</span>
proxy_set_header Host <span class="nv">$host</span><span class="p">;</span>
proxy_redirect off<span class="p">;</span>
client_max_body_size 100M<span class="p">;</span>
<span class="o">}</span>
</pre>

