---
layout: post
title: Handling Static and Media Files in Django
date: 2019-04-05 16:20:23 +0900
category: Python
tag: Python
---


<h1>Handling Static and Media Files in Django</h1>

<h2 id="types-of-files">Types of Files</h2>
<p>Django is an opinionated, full-stack web application framework. It comes with many <a href="https://docs.djangoproject.com/en/4.0/ref/contrib/">batteries</a> that you can use to build a fully functional web application, including static and media file management.</p>
<p>Before we look at the <em>how</em>, let's start with some definitions.</p>
<p><em>What are static and media files?</em></p>
<p>First off, you'll typically find these three types of files in a Django project:</p>
<ol>
<li><strong>Source code</strong>: These are your core Python modules and HTML files that make up every Django project, where you define your models, views, and templates.</li>
<li><strong>Static files</strong>: These are your CSS stylesheets, JavaScript files, fonts, and images. Since there's no processing involved, these files are very energy efficient since they can just be served up as is. They are also much easier to cache.</li>
<li><strong>Media file</strong>: These are files that a user uploads.</li>
</ol>
<li><strong>Source code</strong>: These are your core Python modules and HTML files that make up every Django project, where you define your models, views, and templates.</li>
<li><strong>Static files</strong>: These are your CSS stylesheets, JavaScript files, fonts, and images. Since there's no processing involved, these files are very energy efficient since they can just be served up as is. They are also much easier to cache.</li>
<li><strong>Media file</strong>: These are files that a user uploads.</li>
<p>This article focuses on static and media files. Even though the names are different, both represent regular files. The significant difference is that static files are kept in version control and shipped with your source code files during deployment. On the other hand, media files are files that your end-users (internally and externally) upload or are dynamically created by your application (often as a side effect of some user action).</p>
<p><em>Why should you treat static and media files differently?</em></p>
<ol>
<li>You can't trust files uploaded by end-users, so media files need to be treated differently.</li>
<li>You may need to perform processing on user uploaded, media files to be better served -- e.g., you could optimize uploaded images to support different devices.</li>
<li>You don't want a user uploaded file to replace a static file accidentally.</li>
</ol>
<li>You can't trust files uploaded by end-users, so media files need to be treated differently.</li>
<li>You may need to perform processing on user uploaded, media files to be better served -- e.g., you could optimize uploaded images to support different devices.</li>
<li>You don't want a user uploaded file to replace a static file accidentally.</li>
<p>Additional Notes:</p>
<ol>
<li>Static and media files are sometimes referred to as static and media assets.</li>
<li>The Django admin comes with some static files, which are stored in version control on <a href="https://github.com/django/django/tree/main/django/contrib/admin/static/admin">GitHub</a>.</li>
<li>Adding to the confusion between static and media files is that the Django documentation itself doesn't do a great job differentiating between the two.</li>
</ol>
<li>Static and media files are sometimes referred to as static and media assets.</li>
<li>The Django admin comes with some static files, which are stored in version control on <a href="https://github.com/django/django/tree/main/django/contrib/admin/static/admin">GitHub</a>.</li>
<li>Adding to the confusion between static and media files is that the Django documentation itself doesn't do a great job differentiating between the two.</li>
<h2 id="static-files">Static Files</h2>
<p>Django provides a powerful battery for working with static files, aptly named <a href="https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/">staticfiles</a>.</p>
<p>If you're new to the staticfiles app, take a quick look at the <a href="https://docs.djangoproject.com/en/4.0/howto/static-files/">How to manage static files (e.g., images, JavaScript, CSS)</a> guide from the Django documentation.</p>
<p>Django's staticfiles app provides the following core components:</p>
<ol>
<li>Settings</li>
<li>Management Commands</li>
<li>Storage Classes</li>
<li>Template Tags</li>
</ol>
<li>Settings</li>
<li>Management Commands</li>
<li>Storage Classes</li>
<li>Template Tags</li>
<h3 id="settings">Settings</h3>
<p>There are a number of <a href="https://docs.djangoproject.com/en/4.0/ref/settings/#settings-staticfiles">settings</a> that you <em>may</em> need to configure, depending on your environment:</p>
<ol>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#static-url">STATIC_URL</a>: URL where the user can access your static files from in the browser. The default is <code>/static/</code>, which means your files will be available at <code>http://127.0.0.1:8000/static/</code> in development mode -- e.g.,  <code>http://127.0.0.1:8000/static/css/main.css</code>.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#static-root">STATIC_ROOT</a>: The absolute path to the directory where your Django application will serve your static files from. When you run the <a href="https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/#django-admin-collectstatic">collectstatic</a> management command (more on this shortly), it will find all static files and copy them into this directory.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#staticfiles-dirs">STATICFILES_DIRS</a>: By default, static files are stored at the app-level at <code>&lt;APP_NAME&gt;/static/</code>. The collectstatic command will look for static files in those directories. You can also tell Django to look for static files in additional locations with <code>STATICFILES_DIRS</code>.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#staticfiles-storage">STATICFILES_STORAGE</a>: The file storage class you'd like to use, which controls how the static files are stored and accessed. The files are stored in the file system via <a href="https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/#staticfilesstorage">StaticFilesStorage</a>.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-STATICFILES_FINDERS">STATICFILES_FINDERS</a>: This setting defines the file finder backends to be used to automatically find static files. By default, the <code>FileSystemFinder</code> and <code>AppDirectoriesFinder</code> finders are used:<ul>
<li><code>FileSystemFinder</code> - uses the <code>STATICFILES_DIRS</code> setting to find files.</li>
<li><code>AppDirectoriesFinder</code> - looks for files in a "static" folder in each Django app within the project.</li>
</ul>
</li>
</ol>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#static-url">STATIC_URL</a>: URL where the user can access your static files from in the browser. The default is <code>/static/</code>, which means your files will be available at <code>http://127.0.0.1:8000/static/</code> in development mode -- e.g.,  <code>http://127.0.0.1:8000/static/css/main.css</code>.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#static-root">STATIC_ROOT</a>: The absolute path to the directory where your Django application will serve your static files from. When you run the <a href="https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/#django-admin-collectstatic">collectstatic</a> management command (more on this shortly), it will find all static files and copy them into this directory.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#staticfiles-dirs">STATICFILES_DIRS</a>: By default, static files are stored at the app-level at <code>&lt;APP_NAME&gt;/static/</code>. The collectstatic command will look for static files in those directories. You can also tell Django to look for static files in additional locations with <code>STATICFILES_DIRS</code>.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#staticfiles-storage">STATICFILES_STORAGE</a>: The file storage class you'd like to use, which controls how the static files are stored and accessed. The files are stored in the file system via <a href="https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/#staticfilesstorage">StaticFilesStorage</a>.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-STATICFILES_FINDERS">STATICFILES_FINDERS</a>: This setting defines the file finder backends to be used to automatically find static files. By default, the <code>FileSystemFinder</code> and <code>AppDirectoriesFinder</code> finders are used:<ul>
<li><code>FileSystemFinder</code> - uses the <code>STATICFILES_DIRS</code> setting to find files.</li>
<li><code>AppDirectoriesFinder</code> - looks for files in a "static" folder in each Django app within the project.</li>
</ul>
</li>
<li><code>FileSystemFinder</code> - uses the <code>STATICFILES_DIRS</code> setting to find files.</li>
<li><code>AppDirectoriesFinder</code> - looks for files in a "static" folder in each Django app within the project.</li>
<h3 id="management-commands">Management Commands</h3>
<p>The staticfiles apps provides the following <a href="https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/#management-commands">management commands</a>:</p>
<ol>
<li><code>collectstatic</code> is a management command that collects static files from the various locations -- i.e., <code>&lt;APP_NAME&gt;/static/</code> and the directories found in the <code>STATICFILES_DIRS</code> setting -- and copies them to the <code>STATIC_ROOT</code> directory.</li>
<li><code>findstatic</code> is a really helpful command to use when debugging so you can see exactly where a specific file comes from</li>
<li><code>runserver</code> starts a lightweight, development server to run your Django application in development.</li>
</ol>
<li><code>collectstatic</code> is a management command that collects static files from the various locations -- i.e., <code>&lt;APP_NAME&gt;/static/</code> and the directories found in the <code>STATICFILES_DIRS</code> setting -- and copies them to the <code>STATIC_ROOT</code> directory.</li>
<li><code>findstatic</code> is a really helpful command to use when debugging so you can see exactly where a specific file comes from</li>
<li><code>runserver</code> starts a lightweight, development server to run your Django application in development.</li>
<p>Notes:</p>
<ol>
<li>Don't put any static files in the <code>STATIC_ROOT</code> directory. That's where the static files get copied to automatically after you run <code>collectstatic</code>. Instead, always put them in the directories associated with the <code>STATICFILES_DIRS</code> setting or <code>&lt;APP_NAME&gt;/static/</code>.</li>
<li>Do not use the development server in production. Use a production-grade WSGI application server instead. More on this shortly.</li>
</ol>
<li>Don't put any static files in the <code>STATIC_ROOT</code> directory. That's where the static files get copied to automatically after you run <code>collectstatic</code>. Instead, always put them in the directories associated with the <code>STATICFILES_DIRS</code> setting or <code>&lt;APP_NAME&gt;/static/</code>.</li>
<li>Do not use the development server in production. Use a production-grade WSGI application server instead. More on this shortly.</li>
<p><strong>Quick example of the <code>findstatic</code> command:</strong></p>
<p>Say you have two Django apps, <code>app1</code> and <code>app2</code>. Each app has a folder named "static", and within each of those folders, a file called <em>app.css</em>. Relevant settings from <em>settings.py</em>:</p>
<pre><span></span><code><span class="n">STATIC_ROOT</span> <span class="o">=</span> <span class="s1">'staticfiles'</span>

<span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
<span class="o">...</span>
<span class="s1">'app1'</span><span class="p">,</span>
<span class="s1">'app2'</span><span class="p">,</span>
<span class="p">]</span>
</code></pre>
<p>When <code>python manage.py collectstatic</code> is run, the "staticfiles" directory will be created and the appropriate static files will be copied into it:</p>
<pre><span></span><code>$ ls staticfiles/

admin   app.css
</code></pre>
<p>There's only one <em>app.css</em> file because when multiple files with the same name are present, the staticfiles finder will use the first found file. To see which file is copied over, you can use the <code>findstatic</code> command:</p>
<pre><span></span><code>$ python manage.py findstatic app.css

Found <span class="s1">'app.css'</span> here:
/app1/static/app.css
/app2/static/app.css
</code></pre>
<p>Since only the first encountered file is collected, to check the source of the <em>app.css</em> that was copied over to the "staticfiles" directory, run:</p>
<pre><span></span><code>$ python manage.py findstatic app.css --first

Found <span class="s1">'app.css'</span> here:
/app1/static/app.css
</code></pre>
<h3 id="storage-classes">Storage Classes</h3>
<p>When the <code>collectstatic</code> command is run, Django uses storage classes to determine how the static files are stored and accessed. Again, this is configured via the <a href="https://docs.djangoproject.com/en/4.0/ref/settings/#staticfiles-storage">STATICFILES_STORAGE</a> setting.</p>
<p>The default storage class is <a href="https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/#staticfilesstorage">StaticFilesStorage</a>. Behind the scenes, <code>StaticFilesStorage</code> uses the <a href="https://docs.djangoproject.com/en/4.0/ref/files/storage/#the-filesystemstorage-class">FileSystemStorage</a> class to store files on the local filesystem.</p>
<p>You may want to deviate from the default in production. For example, <a href="https://django-storages.readthedocs.io/en/latest/">django-storages</a> provides a few custom storage classes for different cloud/CDN providers. You can also write your own storage class using the <a href="https://docs.djangoproject.com/en/4.0/ref/files/storage/">file storage API</a>. Review <a href="https://docs.djangoproject.com/en/4.0/howto/static-files/deployment/#serving-static-files-from-a-cloud-service-or-cdn">Serving static files from a cloud service or CDN</a> for more on this.</p>
<p>Storage classes can be used to perform post processing tasks like <a href="https://developer.mozilla.org/en-US/docs/Glossary/minification">minification</a>.</p>
<h3 id="template-tags">Template Tags</h3>
<p>To load static files in your template files, you need to:</p>
<ol>
<li>Add <code>{% load static %}</code> to the top of the template file</li>
<li>Then, for each file you'd like to link, add the <code>{% static %}</code> template tag</li>
</ol>
<li>Add <code>{% load static %}</code> to the top of the template file</li>
<li>Then, for each file you'd like to link, add the <code>{% static %}</code> template tag</li>
<p>For example:</p>
<pre><span></span><code>{% load static %}

<span class="p">&lt;</span><span class="nt">link</span> <span class="na">rel</span><span class="o">=</span><span class="s">"stylesheet"</span> <span class="na">href</span><span class="o">=</span><span class="s">"{% static 'base.css' %}"</span><span class="p">&gt;</span>
</code></pre>
<p>Together, these tags generate a complete URL -- e.g, <code>/static/base.css</code> -- based on the static files configuration in the <em>settings.py</em> file.</p>
<p>You should always load static files in this manner rather than hard coding the URL directly so that you can change your static file configuration and point to a different <code>STATIC_URL</code> without having to manually update each template.</p>
<p>For more on these template tags, review the <a href="https://docs.djangoproject.com/en/4.0/ref/templates/builtins/#static">static</a> section from <a href="https://docs.djangoproject.com/en/4.0/ref/templates/builtins/">Built-in template tags and filters</a>.</p>
<h2 id="static-files-in-development-mode">Static Files in Development Mode</h2>
<p>During development, as long as you have <code>DEBUG</code> set to <code>TRUE</code> and you're using the <a href="https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/">staticfiles</a> app, you can serve up static files using Django's development server. You don't even need to run the <code>collecstatic</code> command.</p>
<p>Typical development config:</p>
<pre><span></span><code><span class="c1"># settings.py</span>
<span class="n">STATIC_URL</span> <span class="o">=</span> <span class="s1">'/static/'</span>
<span class="n">STATIC_ROOT</span> <span class="o">=</span> <span class="n">BASE_DIR</span> <span class="o">/</span> <span class="s1">'staticfiles'</span>
<span class="n">STATICFILES_DIRS</span> <span class="o">=</span> <span class="p">[</span><span class="n">BASE_DIR</span> <span class="o">/</span> <span class="s1">'static'</span><span class="p">,]</span>
<span class="n">STATICFILES_STORAGE</span> <span class="o">=</span> <span class="s1">'django.contrib.staticfiles.storage.StaticFilesStorage'</span>
</code></pre>

<h2 id="static-files-in-production">Static Files in Production</h2>
<p>Handling static files in production isn't quite as easy as your development environment since you'll be using either a WSGI (like <a href="https://gunicorn.org/">Gunicorn</a>) or ASGI (like <a href="https://www.uvicorn.org/">Uvicorn</a>) compatible web application server, which are used to serve up the dynamic content -- i.e., your Django source code files.</p>
<p>There are a number of different ways to handle static files in production, but the two most popular options are:</p>
<ol>
<li>Use a web server like <a href="https://www.nginx.com">Nginx</a> to route traffic destined for your static files directly to the static root (configured via <code>STATIC_ROOT</code>)</li>
<li>Use <a href="https://whitenoise.evans.io/en/stable/">WhiteNoise</a> to serve up static files directly from the WSGI or ASGI web application server</li>
</ol>
<li>Use a web server like <a href="https://www.nginx.com">Nginx</a> to route traffic destined for your static files directly to the static root (configured via <code>STATIC_ROOT</code>)</li>
<li>Use <a href="https://whitenoise.evans.io/en/stable/">WhiteNoise</a> to serve up static files directly from the WSGI or ASGI web application server</li>
<p>Regardless of the option, you'll probably want to leverage a <a href="https://en.wikipedia.org/wiki/Content_delivery_network">CDN</a>.</p>
<p>For more on these options, review <a href="https://docs.djangoproject.com/en/4.0/howto/static-files/deployment/">How to deploy static files</a>.</p>
<h3 id="nginx">Nginx</h3>
<p>Sample Nginx config:</p>
<pre><span></span><code><span class="nt">upstream</span><span class="w"> </span><span class="nt">hello_django</span><span class="w"> </span><span class="p">{</span><span class="w"></span>
<span class="w">    </span><span class="err">server</span><span class="w"> </span><span class="n">web</span><span class="p">:</span><span class="mi">8000</span><span class="p">;</span><span class="w"></span>
<span class="p">}</span><span class="w"></span>

<span class="nt">server</span><span class="w"> </span><span class="p">{</span><span class="w"></span>

<span class="w">    </span><span class="err">listen</span><span class="w"> </span><span class="err">80</span><span class="p">;</span><span class="w"></span>

<span class="w">    </span><span class="err">location</span><span class="w"> </span><span class="err">/</span><span class="w"> </span><span class="err">{</span><span class="w"></span>
<span class="w">        </span><span class="err">proxy_pass</span><span class="w"> </span><span class="n">http</span><span class="p">:</span><span class="o">//</span><span class="n">hello_django</span><span class="p">;</span><span class="w"></span>
<span class="w">        </span><span class="err">proxy_set_header</span><span class="w"> </span><span class="err">X-Forwarded-For</span><span class="w"> </span><span class="err">$proxy_add_x_forwarded_for</span><span class="p">;</span><span class="w"></span>
<span class="w">        </span><span class="err">proxy_set_header</span><span class="w"> </span><span class="err">Host</span><span class="w"> </span><span class="err">$host</span><span class="p">;</span><span class="w"></span>
<span class="w">        </span><span class="err">proxy_redirect</span><span class="w"> </span><span class="err">off</span><span class="p">;</span><span class="w"></span>
<span class="w">    </span><span class="p">}</span><span class="w"></span>

<span class="w">    </span><span class="nt">location</span><span class="w"> </span><span class="o">/</span><span class="nt">static</span><span class="o">/</span><span class="w"> </span><span class="p">{</span><span class="w"></span>
<span class="w">        </span><span class="err">alias</span><span class="w"> </span><span class="err">/home/app/web/staticfiles/</span><span class="p">;</span><span class="w"></span>
<span class="w">    </span><span class="p">}</span><span class="w"></span>

<span class="err">}</span><span class="w"></span>
</code></pre>
<p>In short, when a request is sent to <code>/static/</code> -- e.g, <code>/static/base.css</code> -- Nginx will attempt to serve the file from the "/home/app/web/staticfiles/" folder.</p>
<p>Curious how the above Nginx config works? Check out the <a href="/dockerizing-django-with-postgres-gunicorn-and-nginx">Dockerizing Django with Postgres, Gunicorn, and Nginx</a> tutorial.</p>
<h3 id="whitenoise">WhiteNoise</h3>
<p>You can use <a href="http://whitenoise.evans.io/en/stable/">WhiteNoise</a> to serve static files from a WSGI or ASGI web application server.</p>
<p>The most basic set up is simple. After you install the package, add WhiteNoise to the <code>MIDDLEWARE</code> list above all other middleware apart from <code>django.middleware.security.SecurityMiddleware</code>:</p>
<pre><span></span><code><span class="n">MIDDLEWARE</span> <span class="o">=</span> <span class="p">[</span>
<span class="s1">'django.middleware.security.SecurityMiddleware'</span><span class="p">,</span>
<span class="s1">'whitenoise.middleware.WhiteNoiseMiddleware'</span><span class="p">,</span>  <span class="c1"># &lt;---- WhiteNoise!</span>
<span class="s1">'django.contrib.sessions.middleware.SessionMiddleware'</span><span class="p">,</span>
<span class="s1">'django.middleware.common.CommonMiddleware'</span><span class="p">,</span>
<span class="s1">'django.middleware.csrf.CsrfViewMiddleware'</span><span class="p">,</span>
<span class="s1">'django.contrib.auth.middleware.AuthenticationMiddleware'</span><span class="p">,</span>
<span class="s1">'django.contrib.messages.middleware.MessageMiddleware'</span><span class="p">,</span>
<span class="s1">'django.middleware.clickjacking.XFrameOptionsMiddleware'</span><span class="p">,</span>
<span class="p">]</span>
</code></pre>
<p>Then, for compression and caching support, update <code>STATICFILES_STORAGE</code> like so:</p>
<pre><span></span><code><span class="n">STATICFILES_STORAGE</span> <span class="o">=</span> <span class="s1">'whitenoise.storage.CompressedManifestStaticFilesStorage'</span>
</code></pre>
<p>That's it! Turn off debug mode, run the <code>collectstatic</code> command, and then run your WSGI or ASGI web application server.</p>
<p>Refer to the <a href="http://whitenoise.evans.io/en/stable/django.html">Using WhiteNoise with Django</a> guide for more on configuring WhiteNoise to work with Django.</p>
<h2 id="media-files">Media Files</h2>
<p>Again, <a href="https://docs.djangoproject.com/en/4.0/topics/files/">media files</a> are files that your end-users (internally and externally) upload or are dynamically created by your application (often as a side effect of some user action). They are not typically kept in version control.</p>
<p>Almost always, the files associated with the <a href="https://docs.djangoproject.com/en/4.0/ref/models/fields/#filefield">FileField</a> or <a href="https://docs.djangoproject.com/en/4.0/ref/models/fields/#imagefield">ImageField</a> model fields should be treated as media files.</p>
<p>Just like with static files, the handling of media files is configured in the <em>settings.py</em> file.</p>
<p>Essential configuration settings for handling media files:</p>
<ol>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#media-url">MEDIA_URL</a>: Similar to the <code>STATIC_URL</code>, this is the URL where users can access media files.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#media-root">MEDIA_ROOT</a>: The absolute path to the directory where your Django application will serve your media files from.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#default-file-storage">DEFAULT_FILE_STORAGE</a>: The file storage class you'd like to use, which controls how the media files are stored and accessed. The default is <a href="https://docs.djangoproject.com/en/4.0/ref/files/storage/#django.core.files.storage.FileSystemStorage">FileSystemStorage</a>.</li>
</ol>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#media-url">MEDIA_URL</a>: Similar to the <code>STATIC_URL</code>, this is the URL where users can access media files.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#media-root">MEDIA_ROOT</a>: The absolute path to the directory where your Django application will serve your media files from.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/settings/#default-file-storage">DEFAULT_FILE_STORAGE</a>: The file storage class you'd like to use, which controls how the media files are stored and accessed. The default is <a href="https://docs.djangoproject.com/en/4.0/ref/files/storage/#django.core.files.storage.FileSystemStorage">FileSystemStorage</a>.</li>
<p>Refer to the <a href="https://docs.djangoproject.com/en/4.0/ref/settings/#file-uploads">File uploads</a> section from <a href="https://docs.djangoproject.com/en/4.0/ref/settings/">Settings</a> for additional configuration settings.</p>
<h2 id="media-files-in-development-mode">Media Files in Development Mode</h2>
<p>Typical development config:</p>
<pre><span></span><code><span class="n">MEDIA_URL</span> <span class="o">=</span> <span class="s1">'/media/'</span>
<span class="n">MEDIA_ROOT</span> <span class="o">=</span> <span class="n">BASE_DIR</span> <span class="o">/</span> <span class="s1">'uploads'</span>
</code></pre>
<p>Unfortunately, the Django development server doesn't serve media files by <a href="https://docs.djangoproject.com/en/4.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development">default</a>. Fortunately, there's a very simple workaround: You can add the media root as a static path to the <code>ROOT_URLCONF</code> in your project-level URLs.</p>
<p>Example:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.conf</span> <span class="kn">import</span> <span class="n">settings</span>
<span class="kn">from</span> <span class="nn">django.conf.urls.static</span> <span class="kn">import</span> <span class="n">static</span>
<span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>
<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span><span class="p">,</span> <span class="n">include</span>


<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">path</span><span class="p">(</span><span class="s1">'admin/'</span><span class="p">,</span> <span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">urls</span><span class="p">),</span>
<span class="c1"># ... the rest of your URLconf goes here ...</span>
<span class="p">]</span>

<span class="k">if</span> <span class="n">settings</span><span class="o">.</span><span class="n">DEBUG</span><span class="p">:</span>
<span class="n">urlpatterns</span> <span class="o">+=</span> <span class="n">static</span><span class="p">(</span><span class="n">settings</span><span class="o">.</span><span class="n">MEDIA_URL</span><span class="p">,</span> <span class="n">document_root</span><span class="o">=</span><span class="n">settings</span><span class="o">.</span><span class="n">MEDIA_ROOT</span><span class="p">)</span>
</code></pre>
<h2 id="media-files-in-production">Media Files in Production</h2>
<p>When it comes to handling media files in production, you have less options than you do for static files since you <a href="https://whitenoise.evans.io/en/stable/django.html#serving-media-files">can't use WhiteNoise for serving media files</a>. Thus, you'll typically want to use Nginx along with <a href="https://django-storages.readthedocs.io/en/latest/">django-storages</a> to store media files outside the local file system where your application is running in production.</p>
<p>Sample Nginx config:</p>
<pre><span></span><code><span class="nt">upstream</span><span class="w"> </span><span class="nt">hello_django</span><span class="w"> </span><span class="p">{</span><span class="w"></span>
<span class="w">    </span><span class="err">server</span><span class="w"> </span><span class="n">web</span><span class="p">:</span><span class="mi">8000</span><span class="p">;</span><span class="w"></span>
<span class="p">}</span><span class="w"></span>

<span class="nt">server</span><span class="w"> </span><span class="p">{</span><span class="w"></span>

<span class="w">    </span><span class="err">listen</span><span class="w"> </span><span class="err">80</span><span class="p">;</span><span class="w"></span>

<span class="w">    </span><span class="err">location</span><span class="w"> </span><span class="err">/</span><span class="w"> </span><span class="err">{</span><span class="w"></span>
<span class="w">        </span><span class="err">proxy_pass</span><span class="w"> </span><span class="n">http</span><span class="p">:</span><span class="o">//</span><span class="n">hello_django</span><span class="p">;</span><span class="w"></span>
<span class="w">        </span><span class="err">proxy_set_header</span><span class="w"> </span><span class="err">X-Forwarded-For</span><span class="w"> </span><span class="err">$proxy_add_x_forwarded_for</span><span class="p">;</span><span class="w"></span>
<span class="w">        </span><span class="err">proxy_set_header</span><span class="w"> </span><span class="err">Host</span><span class="w"> </span><span class="err">$host</span><span class="p">;</span><span class="w"></span>
<span class="w">        </span><span class="err">proxy_redirect</span><span class="w"> </span><span class="err">off</span><span class="p">;</span><span class="w"></span>
<span class="w">    </span><span class="p">}</span><span class="w"></span>

<span class="w">    </span><span class="nt">location</span><span class="w"> </span><span class="o">/</span><span class="nt">media</span><span class="o">/</span><span class="w"> </span><span class="p">{</span><span class="w"></span>
<span class="w">        </span><span class="err">alias</span><span class="w"> </span><span class="err">/home/app/web/mediafiles/</span><span class="p">;</span><span class="w"></span>
<span class="w">    </span><span class="p">}</span><span class="w"></span>

<span class="err">}</span><span class="w"></span>
</code></pre>
<p>So, when a request is sent to <code>/media/</code> -- e.g, <code>/media/upload.png</code> -- Nginx will attempt to serve the file from the "/home/app/web/mediafiles/" folder.</p>

