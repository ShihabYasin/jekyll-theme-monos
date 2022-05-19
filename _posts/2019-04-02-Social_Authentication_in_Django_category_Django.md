---
layout: post
title: Social Authentication in Django
date: 2019-04-02 16:20:23 +0900
category: Django
tag: Django
---


<h1>Social Authentication in Django</h1>

<h2 id="oauth">OAuth</h2>
<p>Social auth is most often implemented with <a href="https://oauth.net/">OAuth</a> -- an open standard protocol for authorization -- where a third-party auth provider verifies a user's identity.</p>
<p>Typical flow:</p>
<ol>
<li>A user attempts to log in to your app using their account from a third-party auth provider</li>
<li>They are redirected to the auth provider for verification</li>
<li>After verification, they are then redirected back to your app</li>
<li>They are then logged in so they can access the protected resources</li>
</ol>
<li>A user attempts to log in to your app using their account from a third-party auth provider</li>
<li>They are redirected to the auth provider for verification</li>
<li>After verification, they are then redirected back to your app</li>
<li>They are then logged in so they can access the protected resources</li>
<p>For more on OAuth, review <a href="https://www.digitalocean.com/community/tutorials/an-introduction-to-oauth-2">An Introduction to OAuth 2</a>.</p>
<p>Why would you want to leverage OAuth over rolling your own auth?</p>
<p><strong>Pros</strong>:</p>
<ol>
<li>Improved security.</li>
<li>Easier and faster log-in flows since there's no need to create and remember a username or password.</li>
<li>In case of a security breach, no third-party damage will occur, as the authentication is passwordless.</li>
</ol>
<li>Improved security.</li>
<li>Easier and faster log-in flows since there's no need to create and remember a username or password.</li>
<li>In case of a security breach, no third-party damage will occur, as the authentication is passwordless.</li>
<p><strong>Cons</strong>:</p>
<ol>
<li>Your application now depends on another app outside of your control. If the provider is down, users won't be able to log in.</li>
<li>People often tend to ignore the permissions requested by OAuth providers.</li>
<li>Users that don't have accounts on one of the providers that you have configured won't be able to access your application. The best approach is to implement both -- e.g., username and password and social auth -- and let the user choose.</li>
</ol>
<li>Your application now depends on another app outside of your control. If the provider is down, users won't be able to log in.</li>
<li>People often tend to ignore the permissions requested by OAuth providers.</li>
<li>Users that don't have accounts on one of the providers that you have configured won't be able to access your application. The best approach is to implement both -- e.g., username and password and social auth -- and let the user choose.</li>
<h2 id="django-allauth-vs-python-social-auth">Django Allauth vs. Python Social Auth</h2>
<p><a href="https://github.com/pennersr/django-allauth">Django Allauth</a> and <a href="https://python-social-auth.readthedocs.io/en/latest/">Python Social Auth</a> are the two most popular packages for implementing social authentication in Django. Which one should you use?</p>
<h3 id="django-allauth">Django Allauth</h3>
<p><strong>Pros</strong>:</p>
<ol>
<li>Django Allauth is one of the most popular Django packages.</li>
<li>It supports over 50 authentication providers (i.e., GitHub, Twitter, Google).</li>
<li>Along with social auth, it also provides regular auth with username and password.</li>
<li>Django Allauth makes it easy to customize the forms used during the auth flow.</li>
</ol>
<li>Django Allauth is one of the most popular Django packages.</li>
<li>It supports over 50 authentication providers (i.e., GitHub, Twitter, Google).</li>
<li>Along with social auth, it also provides regular auth with username and password.</li>
<li>Django Allauth makes it easy to customize the forms used during the auth flow.</li>
<p><strong>Cons</strong>:</p>
<ol>
<li>Despite the package's popularity, the documentation is poorly structured and not meant for beginners.</li>
<li>There's quite a bit of initial setup required to register an OAuth provider, which can be difficult for beginners.</li>
<li>There's 250+ issues on GitHub (as of writing).</li>
</ol>
<li>Despite the package's popularity, the documentation is poorly structured and not meant for beginners.</li>
<li>There's quite a bit of initial setup required to register an OAuth provider, which can be difficult for beginners.</li>
<li>There's 250+ issues on GitHub (as of writing).</li>
<h3 id="python-social-auth">Python Social Auth</h3>
<p><strong>Pros</strong>:</p>
<ol>
<li>Python Social Auth provides support for several Python web frameworks like Django, Flask, Webpy, Pyramid, and Tornado.</li>
<li>It supports almost 50 OAuth providers.</li>
<li>It supports the Django ORM and <a href="http://mongoengine.org/">MongoEngine</a> ODM</li>
<li>
<p>It provides a storage interface to allow users to add more ORMs.</p>

</li>
</ol>
<li>Python Social Auth provides support for several Python web frameworks like Django, Flask, Webpy, Pyramid, and Tornado.</li>
<li>It supports almost 50 OAuth providers.</li>
<li>It supports the Django ORM and <a href="http://mongoengine.org/">MongoEngine</a> ODM</li>
<li>
<p>It provides a storage interface to allow users to add more ORMs.</p>

</li>
<p>It provides a storage interface to allow users to add more ORMs.</p>

<p><strong>Cons</strong>:</p>
<ol>
<li>The documentation is a bit simpler, but it could still use some work with regard to the organization.</li>
<li>Again, there's quite a bit of initial setup required to register an OAuth provider, which can be difficult for beginners.</li>
<li>There's close to 100 open issues on GitHub (as of writing).</li>
</ol>
<li>The documentation is a bit simpler, but it could still use some work with regard to the organization.</li>
<li>Again, there's quite a bit of initial setup required to register an OAuth provider, which can be difficult for beginners.</li>
<li>There's close to 100 open issues on GitHub (as of writing).</li>
<p><br/></p>
<p>Both packages have their ups and downs. However, this tutorial focuses on Django Allauth as it's much more popular and supports social auth and regular auth via username and password.</p>
<h2 id="django-setup">Django Setup</h2>
<p>Let's create a new Django project and configure Django Allauth.</p>
<h3 id="create-a-new-django-project">Create a new Django project</h3>
<p>Start by creating a virtual environment and installing Django:</p>
<pre><span></span><code>$ mkdir django-social-auth <span class="o">&amp;&amp;</span> <span class="nb">cd</span> django-social-auth
$ python3.9 -m venv .venv
$ <span class="nb">source</span> .venv/bin/activate
<span class="o">(</span>.venv<span class="o">)</span>$ pip install <span class="nv">Django</span><span class="o">==</span><span class="m">3</span>.1.5
</code></pre>
<p>Feel free to swap out venv and Pip for <a href="https://python-poetry.org">Poetry</a> or <a href="https://github.com/pypa/pipenv">Pipenv</a>. For more, review <a href="/blog/python-environments/">Modern Python Environments</a>.</p>
<p>Now create a new project, apply the migrations, and run the server:</p>
<pre><span></span><code><span class="o">(</span>.venv<span class="o">)</span>$ django-admin startproject social_app .
<span class="o">(</span>.venv<span class="o">)</span>$ python manage.py migrate
<span class="o">(</span>.venv<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>Navigate to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a>. 

<h3 id="configure-django-allauth">Configure Django Allauth</h3>
<p>Next, let's set up Django Allauth for our Django app.</p>
<pre><span></span><code><span class="o">(</span>.venv<span class="o">)</span>$ pip install django-allauth<span class="o">==</span><span class="m">0</span>.44.0
</code></pre>
<p>For Django Allauth to work with our Django app, update <code>INSTALLED_APPS</code> inside the <em>settings.py</em> file like so:</p>
<pre><span></span><code><span class="c1"># social_app/settings.py</span>

<span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
<span class="s2">"django.contrib.admin"</span><span class="p">,</span>
<span class="s2">"django.contrib.auth"</span><span class="p">,</span>
<span class="s2">"django.contrib.contenttypes"</span><span class="p">,</span>
<span class="s2">"django.contrib.sessions"</span><span class="p">,</span>
<span class="s2">"django.contrib.messages"</span><span class="p">,</span>
<span class="s2">"django.contrib.staticfiles"</span><span class="p">,</span>
<span class="s2">"django.contrib.sites"</span><span class="p">,</span>  <span class="c1"># new</span>
<span class="c1"># 3rd party</span>
<span class="s2">"allauth"</span><span class="p">,</span> <span class="c1"># new</span>
<span class="s2">"allauth.account"</span><span class="p">,</span> <span class="c1"># new</span>
<span class="s2">"allauth.socialaccount"</span><span class="p">,</span> <span class="c1"># new</span>
<span class="c1"># social providers</span>
<span class="s2">"allauth.socialaccount.providers.github"</span><span class="p">,</span> <span class="c1"># new</span>
<span class="s2">"allauth.socialaccount.providers.twitter"</span><span class="p">,</span> <span class="c1"># new</span>
<span class="p">]</span>
</code></pre>
<p>First, we added the <a href="https://docs.djangoproject.com/en/3.1/ref/contrib/sites/">Django "sites" framework</a>, which is required for Allauth to work properly. We then added the core Allauth apps: <code>allauth</code>, <code>allauth.account</code>, and <code>allauth.socialaccount</code>.</p>
<p>Now add the following to the bottom of <em>settings.py</em>:</p>
<pre><span></span><code><span class="c1"># social_app/settings.py</span>

<span class="n">AUTHENTICATION_BACKENDS</span> <span class="o">=</span> <span class="p">(</span>
<span class="s2">"allauth.account.auth_backends.AuthenticationBackend"</span><span class="p">,</span>
<span class="p">)</span>

<span class="n">SITE_ID</span> <span class="o">=</span> <span class="mi">1</span>
<span class="n">ACCOUNT_EMAIL_VERIFICATION</span> <span class="o">=</span> <span class="s2">"none"</span>
<span class="n">LOGIN_REDIRECT_URL</span> <span class="o">=</span> <span class="s2">"home"</span>
<span class="n">ACCOUNT_LOGOUT_ON_GET</span> <span class="o">=</span> <span class="kc">True</span>
</code></pre>
<p>Here, we defined the following:</p>
<li>We added <code>allauth</code> as the authentication backend. All logging in and out (via OAuth or regular username and password) will now be handled by Allauth.</li>
<li><code>SITE_ID</code>, which is required for Django Allauth to function.</li>
<li><code>ACCOUNT_EMAIL_VERIFICATION = "none"</code> turns off verification emails. Django automatically sets up an email verification workflow. We do not need this functionality right now.</li>
<li><code>LOGIN_REDIRECT_URL = "home"</code> redirects the user to the homepage after a successful login.</li>
<li><code>ACCOUNT_LOGOUT_ON_GET = True</code> directly logs the user out when the logout button is clicked via a GET request. This skips the <a href="https://django-allauth.readthedocs.io/en/latest/views.html#logout-account-logout">confirm logout page</a>.</li>
<p>Update the <em>urls.py</em> to include Django Allauth:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>
<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span><span class="p">,</span> <span class="n">include</span> <span class="c1"># new</span>


<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">path</span><span class="p">(</span><span class="s2">"admin/"</span><span class="p">,</span> <span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">urls</span><span class="p">),</span>
<span class="n">path</span><span class="p">(</span><span class="s2">"accounts/"</span><span class="p">,</span> <span class="n">include</span><span class="p">(</span><span class="s2">"allauth.urls"</span><span class="p">)),</span> <span class="c1"># new</span>
<span class="p">]</span>
</code></pre>
<p>Apply the migration files associated with Django Allauth:</p>
<pre><span></span><code><span class="o">(</span>.venv<span class="o">)</span>$ python manage.py migrate
</code></pre>
<p>Migrations are important here since a number of new tables are required by Allauth. Don't forget this step!</p>
<p>Create a superuser:</p>
<pre><span></span><code><span class="o">(</span>.venv<span class="o">)</span>$ python manage.py createsuperuser
</code></pre>
<h3 id="templates">Templates</h3>
<p>Create a new folder called "templates", and add two files to it called <em>_base.html</em> and <em>home.html</em>:</p>
<pre><span></span><code><span class="o">(</span>.venv<span class="o">)</span>$ mkdir templates <span class="o">&amp;&amp;</span> <span class="nb">cd</span> templates
<span class="o">(</span>.venv<span class="o">)</span>$ touch _base.html home.html
</code></pre>
<p>Update <code>TEMPLATES</code> in <em>settings.py</em> so that Django knows where to find the templates:</p>
<pre><span></span><code><span class="c1"># social_app/settings.py</span>

<span class="n">TEMPLATES</span> <span class="o">=</span> <span class="p">[</span>
<span class="p">{</span>
<span class="o">...</span>
<span class="s2">"DIRS"</span><span class="p">:</span> <span class="p">[</span><span class="nb">str</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="o">.</span><span class="n">joinpath</span><span class="p">(</span><span class="s2">"templates"</span><span class="p">))],</span>
<span class="o">...</span>
<span class="p">},</span>
<span class="p">]</span>
</code></pre>
<p><em>templates/_base.html</em>:</p>
<pre><span></span><code><span class="cp">&lt;!DOCTYPE html&gt;</span>
<span class="p">&lt;</span><span class="nt">html</span> <span class="na">lang</span><span class="o">=</span><span class="s">"en"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">head</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">meta</span> <span class="na">charset</span><span class="o">=</span><span class="s">"UTF-8"</span> <span class="p">/&gt;</span>
<span class="p">&lt;</span><span class="nt">link</span>
<span class="na">href</span><span class="o">=</span><span class="s">"https://cdn.jsdelivr.net/npm/<a class="__cf_email__" data-cfemail="93f1fcfce7e0e7e1f2e3d3a6bda3bda3bef1f6e7f2a2" href="/cdn-cgi/l/email-protection">[email protected]</a>/dist/css/bootstrap.min.css"</span>
<span class="na">rel</span><span class="o">=</span><span class="s">"stylesheet"</span>
<span class="p">/&gt;</span>
<span class="p">&lt;</span><span class="nt">link</span>
<span class="na">rel</span><span class="o">=</span><span class="s">"stylesheet"</span>
<span class="na">href</span><span class="o">=</span><span class="s">"https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"</span>
<span class="p">/&gt;</span>
<span class="p">&lt;</span><span class="nt">meta</span> <span class="na">name</span><span class="o">=</span><span class="s">"viewport"</span> <span class="na">content</span><span class="o">=</span><span class="s">"width=device-width, initial-scale=1.0"</span> <span class="p">/&gt;</span>
<span class="p">&lt;</span><span class="nt">title</span><span class="p">&gt;</span>Django Social Login<span class="p">&lt;/</span><span class="nt">title</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">head</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">body</span><span class="p">&gt;</span>
{% block content %} {% endblock content %}
<span class="p">&lt;/</span><span class="nt">body</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">html</span><span class="p">&gt;</span>
</code></pre>
<p><em>templates/home.html</em></p>
<pre><span></span><code>{% extends '_base.html' %} {% load socialaccount %}

{% block content %}

<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"container"</span> <span class="na">style</span><span class="o">=</span><span class="s">"text-align: center; padding-top: 10%;"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">h1</span><span class="p">&gt;</span>Django Social Login<span class="p">&lt;/</span><span class="nt">h1</span><span class="p">&gt;</span>

<span class="p">&lt;</span><span class="nt">br</span> <span class="p">/&gt;&lt;</span><span class="nt">br</span> <span class="p">/&gt;</span>

{% if user.is_authenticated %}
<span class="p">&lt;</span><span class="nt">h3</span><span class="p">&gt;</span>Welcome {{ user.username }} !!!<span class="p">&lt;/</span><span class="nt">h3</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">br</span> <span class="p">/&gt;&lt;</span><span class="nt">br</span> <span class="p">/&gt;</span>
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"{% url 'account_logout' %}"</span> <span class="na">class</span><span class="o">=</span><span class="s">"btn btn-danger"</span><span class="p">&gt;</span>Logout<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% endif %}
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>

{% endblock content %}
</code></pre>
<p>Create a view to serve up the <em>home.html</em> template:</p>
<pre><span></span><code><span class="c1"># social_app/views.py</span>

<span class="kn">from</span> <span class="nn">django.views.generic</span> <span class="kn">import</span> <span class="n">TemplateView</span>


<span class="k">class</span> <span class="nc">Home</span><span class="p">(</span><span class="n">TemplateView</span><span class="p">):</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s2">"home.html"</span>
</code></pre>
<p>Add the new URL:</p>
<pre><span></span><code><span class="c1"># social_app/urls.py</span>

<span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>
<span class="kn">from</span> <span class="nn">django.urls</span> <span class="kn">import</span> <span class="n">path</span><span class="p">,</span> <span class="n">include</span>

<span class="kn">from</span> <span class="nn">.views</span> <span class="kn">import</span> <span class="n">Home</span> <span class="c1"># new</span>


<span class="n">urlpatterns</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">path</span><span class="p">(</span><span class="s2">"admin/"</span><span class="p">,</span> <span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">urls</span><span class="p">),</span>
<span class="n">path</span><span class="p">(</span><span class="s2">"accounts/"</span><span class="p">,</span> <span class="n">include</span><span class="p">(</span><span class="s2">"allauth.urls"</span><span class="p">)),</span>
<span class="n">path</span><span class="p">(</span><span class="s2">""</span><span class="p">,</span> <span class="n">Home</span><span class="o">.</span><span class="n">as_view</span><span class="p">(),</span> <span class="n">name</span><span class="o">=</span><span class="s2">"home"</span><span class="p">),</span> <span class="c1"># new</span>
<span class="p">]</span>
</code></pre>
<p>That's it! Django Allauth is configured and ready to test. You should now be able to log in via username and password. Run the server. Navigate to <a href="http://127.0.0.1:8000/accounts/login/">http://127.0.0.1:8000/accounts/login/</a>. Make sure you can log in with your superuser credentials.</p>
<p>You'll probably want to override the default templates to apply CSS style and what not. Review the <a href="https://django-allauth.readthedocs.io/en/latest/templates.html">Templates</a> page from the official docs for more.</p>
<h2 id="github-provider">GitHub Provider</h2>
<p>Now that both Django and Django Allauth are ready let's wire up our first social auth provider -- GitHub.</p>
<h3 id="app">App</h3>
<p>First, we need to create an OAuth app and get the OAuth keys from GitHub. Log in to your GitHub account, and then navigate to <a href="https://github.com/settings/applications/new">https://github.com/settings/applications/new</a> to create a new <a href="https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps">OAuth application</a>:</p>
<pre><span></span><code>Application name: Testing Django Allauth
Homepage URL: http://127.0.0.1:8000
Callback URL: http://127.0.0.1:8000/accounts/github/login/callback
</code></pre>

<p>Click "Register application". You'll be redirected to your app. Take note of the Client ID and Client Secret:</p>

<p>If a Client Secret wasn't generated, click "Generate a new client secret".</p>
<p>Next, we need to add the GitHub provider in the Django admin panel.</p>
<p>Run the server:</p>
<pre><span></span><code><span class="o">(</span>.venv<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>Log in to the admin at <a href="http://127.0.0.1:8000/admin">http://127.0.0.1:8000/admin</a>. Then, under "Social applications", click "Add Social Application":</p>
<li>Choose GitHub as the Provider</li>
<li>Add a name</li>
<li>Add the Client ID and Client Secret (to Secret key) obtained earlier</li>
<li>Add example.com as one of the Chosen Sites</li>

<p>We've successfully integrated GitHub as a social auth provider. With that, let's update the <em>templates/home.html</em> template to test it out:</p>
<pre><span></span><code>{% extends '_base.html' %} {% load socialaccount %}

{% block content %}

<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"container"</span> <span class="na">style</span><span class="o">=</span><span class="s">"text-align: center; padding-top: 10%;"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">h1</span><span class="p">&gt;</span>Django Social Login<span class="p">&lt;/</span><span class="nt">h1</span><span class="p">&gt;</span>

<span class="p">&lt;</span><span class="nt">br</span> <span class="p">/&gt;&lt;</span><span class="nt">br</span> <span class="p">/&gt;</span>

{% if user.is_authenticated %}
<span class="p">&lt;</span><span class="nt">h3</span><span class="p">&gt;</span>Welcome {{ user.username }} !!!<span class="p">&lt;/</span><span class="nt">h3</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">br</span> <span class="p">/&gt;&lt;</span><span class="nt">br</span> <span class="p">/&gt;</span>
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"{% url 'account_logout' %}"</span> <span class="na">class</span><span class="o">=</span><span class="s">"btn btn-danger"</span><span class="p">&gt;</span>Logout<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% else %}
<span class="cm">&lt;!-- GitHub button starts here --&gt;</span>
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"{% provider_login_url 'github' %}"</span> <span class="na">class</span><span class="o">=</span><span class="s">"btn btn-secondary"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">i</span> <span class="na">class</span><span class="o">=</span><span class="s">"fa fa-github fa-fw"</span><span class="p">&gt;&lt;/</span><span class="nt">i</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">span</span><span class="p">&gt;</span>Login with GitHub<span class="p">&lt;/</span><span class="nt">span</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
<span class="cm">&lt;!-- GitHub button ends here --&gt;</span>
{% endif %}
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>

{% endblock content %}
</code></pre>
<p>Run the app. You should now be able to log in via GitHub.</p>

<p>After logging in, you should see the user at <a href="http://127.0.0.1:8000/admin/auth/user/">http://127.0.0.1:8000/admin/auth/user/</a> as well as the associated social account at <a href="http://127.0.0.1:8000/admin/socialaccount/socialaccount/">http://127.0.0.1:8000/admin/socialaccount/socialaccount/</a>. If you view the social account, you'll see all the public data associated with the GitHub account. This data (which is called <a href="https://oauth.net/2/scope/">scope</a>) can be used for your user profile on Django. It's recommended to use a custom <a href="https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#user-model">User Model</a> for this. 

Do you need to read or write access to user info beyond Allauth's default scope? Review <a href="https://django-allauth.readthedocs.io/en/latest/advanced.html#changing-provider-scopes">Changing provider scopes</a> from the official docs.</p>
<h2 id="twitter-provider">Twitter Provider</h2>
<p>Setting up the Twitter provider is similar to GitHub:</p>
<ol>
<li>Create an OAuth app on Twitter</li>
<li>Register the provider in the Django admin</li>
<li>Update the <em>home.html</em> template</li>
</ol>
<li>Create an OAuth app on Twitter</li>
<li>Register the provider in the Django admin</li>
<li>Update the <em>home.html</em> template</li>
<p>Start by <a href="https://developer.twitter.com/en/portal/dashboard">applying</a> for a Twitter developer account. Once created, navigate to <a href="https://developer.twitter.com/en/portal/projects-and-apps">Projects and Apps</a> and click "Create App".</p>
<p>Give the app a name, and take note of the API key and API secret key. Then, under "Authentication Settings", turn on "Enable 3-legged OAuth" and "Request email address from users". Add the Callback, Website, Terms of service, and Privacy policy URLs as well:</p>
<pre><span></span><code>Callback URL: http://127.0.0.1:8000/accounts/twitter/login/callback
Website URL: http://example.com
Terms of service: http://example.com
Privacy policy: http://example.com
</code></pre>

<p>Let's add the provider in the Django Admin.</p>
<p>Run the server:</p>
<pre><span></span><code><span class="o">(</span>.venv<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>Log in to the admin at <a href="http://127.0.0.1:8000/admin">http://127.0.0.1:8000/admin</a>. Then, under "Social applications", click "Add Social Application":</p>
<li>Choose Twitter as the Provider</li>
<li>Add a name</li>
<li>Add the API key (to Client id) and and API secret key (to Secret key) obtained earlier</li>
<li>Add example.com as one of the Chosen Sites</li>

<p>Remember to safeguard your API keys and tokens.</p>
<p>Finally, add a "Login with Twitter" button to <em>templates/home.html</em>:</p>
<pre><span></span><code>{% extends '_base.html' %} {% load socialaccount %}

{% block content %}

<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"container"</span> <span class="na">style</span><span class="o">=</span><span class="s">"text-align: center; padding-top: 10%;"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">h1</span><span class="p">&gt;</span>Django Social Login<span class="p">&lt;/</span><span class="nt">h1</span><span class="p">&gt;</span>

<span class="p">&lt;</span><span class="nt">br</span> <span class="p">/&gt;&lt;</span><span class="nt">br</span> <span class="p">/&gt;</span>

{% if user.is_authenticated %}
<span class="p">&lt;</span><span class="nt">h3</span><span class="p">&gt;</span>Welcome {{ user.username }} !!!<span class="p">&lt;/</span><span class="nt">h3</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">br</span> <span class="p">/&gt;&lt;</span><span class="nt">br</span> <span class="p">/&gt;</span>
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"{% url 'account_logout' %}"</span> <span class="na">class</span><span class="o">=</span><span class="s">"btn btn-danger"</span><span class="p">&gt;</span>Logout<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% else %}

...

<span class="cm">&lt;!-- Twitter button starts here --&gt;</span>
<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"{% provider_login_url 'twitter' %}"</span> <span class="na">class</span><span class="o">=</span><span class="s">"btn btn-primary"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">i</span> <span class="na">class</span><span class="o">=</span><span class="s">"fa fa-twitter fa-fw"</span><span class="p">&gt;&lt;/</span><span class="nt">i</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">span</span><span class="p">&gt;</span>Login with Twitter<span class="p">&lt;/</span><span class="nt">span</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
<span class="cm">&lt;!-- Twitter button ends here --&gt;</span>
{% endif %}
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>

{% endblock content %}
</code></pre>
<p>Navigate to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a> to test out the auth workflow.</p>
