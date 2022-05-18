---
layout: post
title: Creating a Custom User Model in Django.
date: 2019-03-20 16:20:23 +0900
category: Django
tag: Django
---


<h1>Creating a Custom User Model in Django</h1>

<h2 id="abstractuser-vs-abstractbaseuser">AbstractUser vs AbstractBaseUser</h2>
<p>The default User model in Django uses a username to uniquely identify a user during authentication. If you'd rather use an email address, you'll need to create a custom User model by either subclassing <code>AbstractUser</code> or <code>AbstractBaseUser</code>.</p>
<p>Options:</p>
<ol>
<li><code>AbstractUser</code>: Use this option if you are happy with the existing fields on the User model and just want to remove the username field.</li>
<li><code>AbstractBaseUser</code>: Use this option if you want to start from scratch by creating your own, completely new User model.</li>
</ol>
<li><code>AbstractUser</code>: Use this option if you are happy with the existing fields on the User model and just want to remove the username field.</li>
<li><code>AbstractBaseUser</code>: Use this option if you want to start from scratch by creating your own, completely new User model.</li>
<p>We'll look at both options, <code>AbstractUser</code> and <code>AbstractBaseUser</code>, in this post.</p>
<p>The steps are the same for each:</p>
<ol>
<li>Create a custom User model and Manager</li>
<li>Update <em>settings.py</em></li>
<li>Customize the <code>UserCreationForm</code> and <code>UserChangeForm</code> forms</li>
<li>Update the admin</li>
</ol>
<li>Create a custom User model and Manager</li>
<li>Update <em>settings.py</em></li>
<li>Customize the <code>UserCreationForm</code> and <code>UserChangeForm</code> forms</li>
<li>Update the admin</li>
<p>It's <a href="https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project">highly recommended</a> to set up a custom User model when starting a new Django project. Without it, you will need to create another model (like <code>UserProfile</code>) and link it to the Django User model with a <code>OneToOneField</code> if you want to add new fields to the User model.</p>
<h2 id="project-setup">Project Setup</h2>
<p>Start by creating a new Django project along with a users app:</p>
<pre><span></span><code>$ mkdir django-custom-user-model <span class="o">&amp;&amp;</span> <span class="nb">cd</span> django-custom-user-model
$ python3 -m venv env
$ <span class="nb">source</span> env/bin/activate

<span class="o">(</span>env<span class="o">)</span>$ pip install <span class="nv">Django</span><span class="o">==</span><span class="m">3</span>.2.2
<span class="o">(</span>env<span class="o">)</span>$ django-admin startproject hello_django .
<span class="o">(</span>env<span class="o">)</span>$ python manage.py startapp users
</code></pre>
<p>Feel free to swap out virtualenv and Pip for <a href="https://python-poetry.org">Poetry</a> or <a href="https://github.com/pypa/pipenv">Pipenv</a>. For more, review <a href="/blog/python-environments/">Modern Python Environments</a>.</p>
<p>DO NOT apply the migrations. Remember: You must create the custom User model <em>before</em> you apply your first migration.</p>
<p>Add the new app to the <code>INSTALLED_APPS</code> list in <em>settings.py</em>:</p>
<pre><span></span><code><span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
<span class="s1">'django.contrib.admin'</span><span class="p">,</span>
<span class="s1">'django.contrib.auth'</span><span class="p">,</span>
<span class="s1">'django.contrib.contenttypes'</span><span class="p">,</span>
<span class="s1">'django.contrib.sessions'</span><span class="p">,</span>
<span class="s1">'django.contrib.messages'</span><span class="p">,</span>
<span class="s1">'django.contrib.staticfiles'</span><span class="p">,</span>

<span class="s1">'users'</span><span class="p">,</span>
<span class="p">]</span>
</code></pre>
<h2 id="tests">Tests</h2>
<p>Let's take a test-first approach:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth</span> <span class="kn">import</span> <span class="n">get_user_model</span>
<span class="kn">from</span> <span class="nn">django.test</span> <span class="kn">import</span> <span class="n">TestCase</span>


<span class="k">class</span> <span class="nc">UsersManagersTests</span><span class="p">(</span><span class="n">TestCase</span><span class="p">):</span>

<span class="k">def</span> <span class="nf">test_create_user</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="n">User</span> <span class="o">=</span> <span class="n">get_user_model</span><span class="p">()</span>
<span class="n">user</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">create_user</span><span class="p">(</span><span class="n">email</span><span class="o">=</span><span class="s1">'<a class="__cf_email__" data-cfemail="c0aeafb2ada1ac80b5b3a5b2eea3afad" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span><span class="p">,</span> <span class="n">password</span><span class="o">=</span><span class="s1">'foo'</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertEqual</span><span class="p">(</span><span class="n">user</span><span class="o">.</span><span class="n">email</span><span class="p">,</span> <span class="s1">'<a class="__cf_email__" data-cfemail="3e50514c535f527e4b4d5b4c105d5153" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertTrue</span><span class="p">(</span><span class="n">user</span><span class="o">.</span><span class="n">is_active</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertFalse</span><span class="p">(</span><span class="n">user</span><span class="o">.</span><span class="n">is_staff</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertFalse</span><span class="p">(</span><span class="n">user</span><span class="o">.</span><span class="n">is_superuser</span><span class="p">)</span>
<span class="k">try</span><span class="p">:</span>
<span class="c1"># username is None for the AbstractUser option</span>
<span class="c1"># username does not exist for the AbstractBaseUser option</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertIsNone</span><span class="p">(</span><span class="n">user</span><span class="o">.</span><span class="n">username</span><span class="p">)</span>
<span class="k">except</span> <span class="ne">AttributeError</span><span class="p">:</span>
<span class="k">pass</span>
<span class="k">with</span> <span class="bp">self</span><span class="o">.</span><span class="n">assertRaises</span><span class="p">(</span><span class="ne">TypeError</span><span class="p">):</span>
<span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">create_user</span><span class="p">()</span>
<span class="k">with</span> <span class="bp">self</span><span class="o">.</span><span class="n">assertRaises</span><span class="p">(</span><span class="ne">TypeError</span><span class="p">):</span>
<span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">create_user</span><span class="p">(</span><span class="n">email</span><span class="o">=</span><span class="s1">''</span><span class="p">)</span>
<span class="k">with</span> <span class="bp">self</span><span class="o">.</span><span class="n">assertRaises</span><span class="p">(</span><span class="ne">ValueError</span><span class="p">):</span>
<span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">create_user</span><span class="p">(</span><span class="n">email</span><span class="o">=</span><span class="s1">''</span><span class="p">,</span> <span class="n">password</span><span class="o">=</span><span class="s2">"foo"</span><span class="p">)</span>

<span class="k">def</span> <span class="nf">test_create_superuser</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="n">User</span> <span class="o">=</span> <span class="n">get_user_model</span><span class="p">()</span>
<span class="n">admin_user</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">create_superuser</span><span class="p">(</span><span class="n">email</span><span class="o">=</span><span class="s1">'<a class="__cf_email__" data-cfemail="1a696f6a7f685a6f697f6834797577" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span><span class="p">,</span> <span class="n">password</span><span class="o">=</span><span class="s1">'foo'</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertEqual</span><span class="p">(</span><span class="n">admin_user</span><span class="o">.</span><span class="n">email</span><span class="p">,</span> <span class="s1">'<a class="__cf_email__" data-cfemail="4d3e383d283f0d383e283f632e2220" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertTrue</span><span class="p">(</span><span class="n">admin_user</span><span class="o">.</span><span class="n">is_active</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertTrue</span><span class="p">(</span><span class="n">admin_user</span><span class="o">.</span><span class="n">is_staff</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertTrue</span><span class="p">(</span><span class="n">admin_user</span><span class="o">.</span><span class="n">is_superuser</span><span class="p">)</span>
<span class="k">try</span><span class="p">:</span>
<span class="c1"># username is None for the AbstractUser option</span>
<span class="c1"># username does not exist for the AbstractBaseUser option</span>
<span class="bp">self</span><span class="o">.</span><span class="n">assertIsNone</span><span class="p">(</span><span class="n">admin_user</span><span class="o">.</span><span class="n">username</span><span class="p">)</span>
<span class="k">except</span> <span class="ne">AttributeError</span><span class="p">:</span>
<span class="k">pass</span>
<span class="k">with</span> <span class="bp">self</span><span class="o">.</span><span class="n">assertRaises</span><span class="p">(</span><span class="ne">ValueError</span><span class="p">):</span>
<span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">create_superuser</span><span class="p">(</span>
<span class="n">email</span><span class="o">=</span><span class="s1">'<a class="__cf_email__" data-cfemail="f88b8d889d8ab88d8b9d8ad69b9795" href="/cdn-cgi/l/email-protection">[email protected]</a>'</span><span class="p">,</span> <span class="n">password</span><span class="o">=</span><span class="s1">'foo'</span><span class="p">,</span> <span class="n">is_superuser</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</code></pre>
<p>Add the specs to <em>users/tests.py</em>, and then make sure the tests fail.</p>
<h2 id="model-manager">Model Manager</h2>
<p>First, we need to add a custom <a href="https://docs.djangoproject.com/en/3.2/topics/db/managers/">Manager</a>, by subclassing <code>BaseUserManager</code>, that uses an email as the unique identifier instead of a username.</p>
<p>Create a <em>managers.py</em> file in the "users" directory:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth.base_user</span> <span class="kn">import</span> <span class="n">BaseUserManager</span>
<span class="kn">from</span> <span class="nn">django.utils.translation</span> <span class="kn">import</span> <span class="n">ugettext_lazy</span> <span class="k">as</span> <span class="n">_</span>


<span class="k">class</span> <span class="nc">CustomUserManager</span><span class="p">(</span><span class="n">BaseUserManager</span><span class="p">):</span>
<span class="sd">"""</span>
<span class="sd">    Custom user model manager where email is the unique identifiers</span>
<span class="sd">    for authentication instead of usernames.</span>
<span class="sd">    """</span>
<span class="k">def</span> <span class="nf">create_user</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">email</span><span class="p">,</span> <span class="n">password</span><span class="p">,</span> <span class="o">**</span><span class="n">extra_fields</span><span class="p">):</span>
<span class="sd">"""</span>
<span class="sd">        Create and save a User with the given email and password.</span>
<span class="sd">        """</span>
<span class="k">if</span> <span class="ow">not</span> <span class="n">email</span><span class="p">:</span>
<span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="n">_</span><span class="p">(</span><span class="s1">'The Email must be set'</span><span class="p">))</span>
<span class="n">email</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">normalize_email</span><span class="p">(</span><span class="n">email</span><span class="p">)</span>
<span class="n">user</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">model</span><span class="p">(</span><span class="n">email</span><span class="o">=</span><span class="n">email</span><span class="p">,</span> <span class="o">**</span><span class="n">extra_fields</span><span class="p">)</span>
<span class="n">user</span><span class="o">.</span><span class="n">set_password</span><span class="p">(</span><span class="n">password</span><span class="p">)</span>
<span class="n">user</span><span class="o">.</span><span class="n">save</span><span class="p">()</span>
<span class="k">return</span> <span class="n">user</span>

<span class="k">def</span> <span class="nf">create_superuser</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">email</span><span class="p">,</span> <span class="n">password</span><span class="p">,</span> <span class="o">**</span><span class="n">extra_fields</span><span class="p">):</span>
<span class="sd">"""</span>
<span class="sd">        Create and save a SuperUser with the given email and password.</span>
<span class="sd">        """</span>
<span class="n">extra_fields</span><span class="o">.</span><span class="n">setdefault</span><span class="p">(</span><span class="s1">'is_staff'</span><span class="p">,</span> <span class="kc">True</span><span class="p">)</span>
<span class="n">extra_fields</span><span class="o">.</span><span class="n">setdefault</span><span class="p">(</span><span class="s1">'is_superuser'</span><span class="p">,</span> <span class="kc">True</span><span class="p">)</span>
<span class="n">extra_fields</span><span class="o">.</span><span class="n">setdefault</span><span class="p">(</span><span class="s1">'is_active'</span><span class="p">,</span> <span class="kc">True</span><span class="p">)</span>

<span class="k">if</span> <span class="n">extra_fields</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">'is_staff'</span><span class="p">)</span> <span class="ow">is</span> <span class="ow">not</span> <span class="kc">True</span><span class="p">:</span>
<span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="n">_</span><span class="p">(</span><span class="s1">'Superuser must have is_staff=True.'</span><span class="p">))</span>
<span class="k">if</span> <span class="n">extra_fields</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">'is_superuser'</span><span class="p">)</span> <span class="ow">is</span> <span class="ow">not</span> <span class="kc">True</span><span class="p">:</span>
<span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="n">_</span><span class="p">(</span><span class="s1">'Superuser must have is_superuser=True.'</span><span class="p">))</span>
<span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">create_user</span><span class="p">(</span><span class="n">email</span><span class="p">,</span> <span class="n">password</span><span class="p">,</span> <span class="o">**</span><span class="n">extra_fields</span><span class="p">)</span>
</code></pre>
<h2 id="user-model">User Model</h2>
<p>Decide which option you'd like to use: subclassing <code>AbstractUser</code> or <code>AbstractBaseUser</code>.</p>
<h3 id="abstractuser">AbstractUser</h3>
<p>Update <em>users/models.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">AbstractUser</span>
<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>
<span class="kn">from</span> <span class="nn">django.utils.translation</span> <span class="kn">import</span> <span class="n">ugettext_lazy</span> <span class="k">as</span> <span class="n">_</span>

<span class="kn">from</span> <span class="nn">.managers</span> <span class="kn">import</span> <span class="n">CustomUserManager</span>


<span class="k">class</span> <span class="nc">CustomUser</span><span class="p">(</span><span class="n">AbstractUser</span><span class="p">):</span>
<span class="n">username</span> <span class="o">=</span> <span class="kc">None</span>
<span class="n">email</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">EmailField</span><span class="p">(</span><span class="n">_</span><span class="p">(</span><span class="s1">'email address'</span><span class="p">),</span> <span class="n">unique</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<span class="n">USERNAME_FIELD</span> <span class="o">=</span> <span class="s1">'email'</span>
<span class="n">REQUIRED_FIELDS</span> <span class="o">=</span> <span class="p">[]</span>

<span class="n">objects</span> <span class="o">=</span> <span class="n">CustomUserManager</span><span class="p">()</span>

<span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">email</span>
</code></pre>
<p>Here, we:</p>
<ol>
<li>Created a new class called <code>CustomUser</code> that subclasses <code>AbstractUser</code></li>
<li>Removed the <code>username</code> field</li>
<li>Made the <code>email</code> field required and unique</li>
<li>Set the <code>USERNAME_FIELD</code> -- which defines the unique identifier for the <code>User</code> model -- to <code>email</code></li>
<li>Specified that all objects for the class come from the <code>CustomUserManager</code></li>
</ol>
<li>Created a new class called <code>CustomUser</code> that subclasses <code>AbstractUser</code></li>
<li>Removed the <code>username</code> field</li>
<li>Made the <code>email</code> field required and unique</li>
<li>Set the <code>USERNAME_FIELD</code> -- which defines the unique identifier for the <code>User</code> model -- to <code>email</code></li>
<li>Specified that all objects for the class come from the <code>CustomUserManager</code></li>
<h3 id="abstractbaseuser">AbstractBaseUser</h3>
<p>Update <em>users/models.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">AbstractBaseUser</span><span class="p">,</span> <span class="n">PermissionsMixin</span>
<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>
<span class="kn">from</span> <span class="nn">django.utils</span> <span class="kn">import</span> <span class="n">timezone</span>
<span class="kn">from</span> <span class="nn">django.utils.translation</span> <span class="kn">import</span> <span class="n">gettext_lazy</span> <span class="k">as</span> <span class="n">_</span>

<span class="kn">from</span> <span class="nn">.managers</span> <span class="kn">import</span> <span class="n">CustomUserManager</span>


<span class="k">class</span> <span class="nc">CustomUser</span><span class="p">(</span><span class="n">AbstractBaseUser</span><span class="p">,</span> <span class="n">PermissionsMixin</span><span class="p">):</span>
<span class="n">email</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">EmailField</span><span class="p">(</span><span class="n">_</span><span class="p">(</span><span class="s1">'email address'</span><span class="p">),</span> <span class="n">unique</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="n">is_staff</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">BooleanField</span><span class="p">(</span><span class="n">default</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
<span class="n">is_active</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">BooleanField</span><span class="p">(</span><span class="n">default</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="n">date_joined</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">default</span><span class="o">=</span><span class="n">timezone</span><span class="o">.</span><span class="n">now</span><span class="p">)</span>

<span class="n">USERNAME_FIELD</span> <span class="o">=</span> <span class="s1">'email'</span>
<span class="n">REQUIRED_FIELDS</span> <span class="o">=</span> <span class="p">[]</span>

<span class="n">objects</span> <span class="o">=</span> <span class="n">CustomUserManager</span><span class="p">()</span>

<span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">email</span>
</code></pre>
<p>Here, we:</p>
<ol>
<li>Created a new class called <code>CustomUser</code> that subclasses <code>AbstractBaseUser</code></li>
<li>Added fields for <code>email</code>, <code>is_staff</code>, <code>is_active</code>, and <code>date_joined</code></li>
<li>Set the <code>USERNAME_FIELD</code> -- which defines the unique identifier for the <code>User</code> model -- to <code>email</code></li>
<li>Specified that all objects for the class come from the <code>CustomUserManager</code></li>
</ol>
<li>Created a new class called <code>CustomUser</code> that subclasses <code>AbstractBaseUser</code></li>
<li>Added fields for <code>email</code>, <code>is_staff</code>, <code>is_active</code>, and <code>date_joined</code></li>
<li>Set the <code>USERNAME_FIELD</code> -- which defines the unique identifier for the <code>User</code> model -- to <code>email</code></li>
<li>Specified that all objects for the class come from the <code>CustomUserManager</code></li>
<h2 id="settings">Settings</h2>
<p>Add the following line to the <em>settings.py</em> file so that Django knows to use the new User class:</p>
<pre><span></span><code><span class="n">AUTH_USER_MODEL</span> <span class="o">=</span> <span class="s1">'users.CustomUser'</span>
</code></pre>
<p>Now, you can create and apply the migrations, which will create a new database that uses the custom User model. Before we do that, let's look at what the migration will actually look like <em>without</em> creating the migration file, with the <a href="https://docs.djangoproject.com/en/3.2/ref/django-admin/#cmdoption-makemigrations-dry-run">--dry-run</a> flag:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py makemigrations --dry-run --verbosity <span class="m">3</span>
</code></pre>
<p>You should see something similar to:</p>
<pre><span></span><code><span class="c1"># Generated by Django 3.2.2 on 2021-05-12 20:43</span>

<span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">migrations</span><span class="p">,</span> <span class="n">models</span>
<span class="kn">import</span> <span class="nn">django.utils.timezone</span>


<span class="k">class</span> <span class="nc">Migration</span><span class="p">(</span><span class="n">migrations</span><span class="o">.</span><span class="n">Migration</span><span class="p">):</span>

<span class="n">initial</span> <span class="o">=</span> <span class="kc">True</span>

<span class="n">dependencies</span> <span class="o">=</span> <span class="p">[</span>
<span class="p">(</span><span class="s1">'auth'</span><span class="p">,</span> <span class="s1">'0012_alter_user_first_name_max_length'</span><span class="p">),</span>
<span class="p">]</span>

<span class="n">operations</span> <span class="o">=</span> <span class="p">[</span>
<span class="n">migrations</span><span class="o">.</span><span class="n">CreateModel</span><span class="p">(</span>
<span class="n">name</span><span class="o">=</span><span class="s1">'CustomUser'</span><span class="p">,</span>
<span class="n">fields</span><span class="o">=</span><span class="p">[</span>
<span class="p">(</span><span class="s1">'id'</span><span class="p">,</span> <span class="n">models</span><span class="o">.</span><span class="n">BigAutoField</span><span class="p">(</span><span class="n">auto_created</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">primary_key</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">serialize</span><span class="o">=</span><span class="kc">False</span><span class="p">,</span> <span class="n">verbose_name</span><span class="o">=</span><span class="s1">'ID'</span><span class="p">)),</span>
<span class="p">(</span><span class="s1">'password'</span><span class="p">,</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">128</span><span class="p">,</span> <span class="n">verbose_name</span><span class="o">=</span><span class="s1">'password'</span><span class="p">)),</span>
<span class="p">(</span><span class="s1">'last_login'</span><span class="p">,</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">blank</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">null</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">verbose_name</span><span class="o">=</span><span class="s1">'last login'</span><span class="p">)),</span>
<span class="p">(</span><span class="s1">'is_superuser'</span><span class="p">,</span> <span class="n">models</span><span class="o">.</span><span class="n">BooleanField</span><span class="p">(</span><span class="n">default</span><span class="o">=</span><span class="kc">False</span><span class="p">,</span> <span class="n">help_text</span><span class="o">=</span><span class="s1">'Designates that this user has all permissions without explicitly assigning them.'</span><span class="p">,</span> <span class="n">verbose_name</span><span class="o">=</span><span class="s1">'superuser status'</span><span class="p">)),</span>
<span class="p">(</span><span class="s1">'first_name'</span><span class="p">,</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">blank</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">max_length</span><span class="o">=</span><span class="mi">150</span><span class="p">,</span> <span class="n">verbose_name</span><span class="o">=</span><span class="s1">'first name'</span><span class="p">)),</span>
<span class="p">(</span><span class="s1">'last_name'</span><span class="p">,</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">blank</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">max_length</span><span class="o">=</span><span class="mi">150</span><span class="p">,</span> <span class="n">verbose_name</span><span class="o">=</span><span class="s1">'last name'</span><span class="p">)),</span>
<span class="p">(</span><span class="s1">'is_staff'</span><span class="p">,</span> <span class="n">models</span><span class="o">.</span><span class="n">BooleanField</span><span class="p">(</span><span class="n">default</span><span class="o">=</span><span class="kc">False</span><span class="p">,</span> <span class="n">help_text</span><span class="o">=</span><span class="s1">'Designates whether the user can log into this admin site.'</span><span class="p">,</span> <span class="n">verbose_name</span><span class="o">=</span><span class="s1">'staff status'</span><span class="p">)),</span>
<span class="p">(</span><span class="s1">'is_active'</span><span class="p">,</span> <span class="n">models</span><span class="o">.</span><span class="n">BooleanField</span><span class="p">(</span><span class="n">default</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">help_text</span><span class="o">=</span><span class="s1">'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'</span><span class="p">,</span> <span class="n">verbose_name</span><span class="o">=</span><span class="s1">'active'</span><span class="p">)),</span>
<span class="p">(</span><span class="s1">'date_joined'</span><span class="p">,</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">default</span><span class="o">=</span><span class="n">django</span><span class="o">.</span><span class="n">utils</span><span class="o">.</span><span class="n">timezone</span><span class="o">.</span><span class="n">now</span><span class="p">,</span> <span class="n">verbose_name</span><span class="o">=</span><span class="s1">'date joined'</span><span class="p">)),</span>
<span class="p">(</span><span class="s1">'email'</span><span class="p">,</span> <span class="n">models</span><span class="o">.</span><span class="n">EmailField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">254</span><span class="p">,</span> <span class="n">unique</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">verbose_name</span><span class="o">=</span><span class="s1">'email address'</span><span class="p">)),</span>
<span class="p">(</span><span class="s1">'groups'</span><span class="p">,</span> <span class="n">models</span><span class="o">.</span><span class="n">ManyToManyField</span><span class="p">(</span><span class="n">blank</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">help_text</span><span class="o">=</span><span class="s1">'The groups this user belongs to. A user will get all permissions granted to each of their groups.'</span><span class="p">,</span> <span class="n">related_name</span><span class="o">=</span><span class="s1">'user_set'</span><span class="p">,</span> <span class="n">related_query_name</span><span class="o">=</span><span class="s1">'user'</span><span class="p">,</span> <span class="n">to</span><span class="o">=</span><span class="s1">'auth.Group'</span><span class="p">,</span> <span class="n">verbose_name</span><span class="o">=</span><span class="s1">'groups'</span><span class="p">)),</span>
<span class="p">(</span><span class="s1">'user_permissions'</span><span class="p">,</span> <span class="n">models</span><span class="o">.</span><span class="n">ManyToManyField</span><span class="p">(</span><span class="n">blank</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">help_text</span><span class="o">=</span><span class="s1">'Specific permissions for this user.'</span><span class="p">,</span> <span class="n">related_name</span><span class="o">=</span><span class="s1">'user_set'</span><span class="p">,</span> <span class="n">related_query_name</span><span class="o">=</span><span class="s1">'user'</span><span class="p">,</span> <span class="n">to</span><span class="o">=</span><span class="s1">'auth.Permission'</span><span class="p">,</span> <span class="n">verbose_name</span><span class="o">=</span><span class="s1">'user permissions'</span><span class="p">)),</span>
<span class="p">],</span>
<span class="n">options</span><span class="o">=</span><span class="p">{</span>
<span class="s1">'verbose_name'</span><span class="p">:</span> <span class="s1">'user'</span><span class="p">,</span>
<span class="s1">'verbose_name_plural'</span><span class="p">:</span> <span class="s1">'users'</span><span class="p">,</span>
<span class="s1">'abstract'</span><span class="p">:</span> <span class="kc">False</span><span class="p">,</span>
<span class="p">},</span>
<span class="p">),</span>
<span class="p">]</span>
</code></pre>
<p>If you went the <code>AbstractBaseUser</code> route, you won't have fields for <code>first_name</code> or <code>last_name</code>. Why?</p>
<p>Make sure the migration does not include a <code>username</code> field. Then, create and apply the migration:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py makemigrations
<span class="o">(</span>env<span class="o">)</span>$ python manage.py migrate
</code></pre>
<p>View the schema:</p>
<pre><span></span><code>$ sqlite3 db.sqlite3

SQLite version <span class="m">3</span>.28.0 <span class="m">2019</span>-04-15 <span class="m">14</span>:49:49
Enter <span class="s2">".help"</span> <span class="k">for</span> usage hints.

sqlite&gt; .tables

auth_group                         django_migrations
auth_group_permissions             django_session
auth_permission                    users_customuser
django_admin_log                   users_customuser_groups
django_content_type                users_customuser_user_permissions

sqlite&gt; .schema users_customuser

CREATE TABLE IF NOT EXISTS <span class="s2">"users_customuser"</span> <span class="o">(</span>
<span class="s2">"id"</span> integer NOT NULL PRIMARY KEY AUTOINCREMENT,
<span class="s2">"password"</span> varchar<span class="o">(</span><span class="m">128</span><span class="o">)</span> NOT NULL,
<span class="s2">"last_login"</span> datetime NULL,
<span class="s2">"is_superuser"</span> bool NOT NULL,
<span class="s2">"first_name"</span> varchar<span class="o">(</span><span class="m">150</span><span class="o">)</span> NOT NULL,
<span class="s2">"last_name"</span> varchar<span class="o">(</span><span class="m">150</span><span class="o">)</span> NOT NULL,
<span class="s2">"is_staff"</span> bool NOT NULL,
<span class="s2">"is_active"</span> bool NOT NULL,
<span class="s2">"date_joined"</span> datetime NOT NULL,
<span class="s2">"email"</span> varchar<span class="o">(</span><span class="m">254</span><span class="o">)</span> NOT NULL UNIQUE
<span class="o">)</span><span class="p">;</span>
</code></pre>
<p>If you went the <code>AbstractBaseUser</code> route, why is <code>last_login</code> part of the model?</p>
<p>You can now reference the User model with either <code>get_user_model()</code> or <code>settings.AUTH_USER_MODEL</code>. Refer to <a href="https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#referencing-the-user-model">Referencing the User model</a> from the official docs for more info.</p>
<p>Also, when you create a superuser, you should be prompted to enter an email rather than a username:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py createsuperuser

Email address: <a class="__cf_email__" data-cfemail="7e0a1b0d0a3e0a1b0d0a501d1113" href="/cdn-cgi/l/email-protection">[email protected]</a>
Password:
Password <span class="o">(</span>again<span class="o">)</span>:
Superuser created successfully.
</code></pre>
<p>Make sure the tests pass:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python manage.py <span class="nb">test</span>

Creating <span class="nb">test</span> database <span class="k">for</span> <span class="nb">alias</span> <span class="s1">'default'</span>...
System check identified no issues <span class="o">(</span><span class="m">0</span> silenced<span class="o">)</span>.
..
----------------------------------------------------------------------
Ran <span class="m">2</span> tests <span class="k">in</span> <span class="m">0</span>.282s

OK
Destroying <span class="nb">test</span> database <span class="k">for</span> <span class="nb">alias</span> <span class="s1">'default'</span>...
</code></pre>
<h2 id="forms">Forms</h2>
<p>Next, let's subclass the <code>UserCreationForm</code> and <code>UserChangeForm</code> forms so that they use the new <code>CustomUser</code> model.</p>
<p>Create a new file in "users" called <em>forms.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth.forms</span> <span class="kn">import</span> <span class="n">UserCreationForm</span><span class="p">,</span> <span class="n">UserChangeForm</span>

<span class="kn">from</span> <span class="nn">.models</span> <span class="kn">import</span> <span class="n">CustomUser</span>


<span class="k">class</span> <span class="nc">CustomUserCreationForm</span><span class="p">(</span><span class="n">UserCreationForm</span><span class="p">):</span>

<span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">CustomUser</span>
<span class="n">fields</span> <span class="o">=</span> <span class="p">(</span><span class="s1">'email'</span><span class="p">,)</span>


<span class="k">class</span> <span class="nc">CustomUserChangeForm</span><span class="p">(</span><span class="n">UserChangeForm</span><span class="p">):</span>

<span class="k">class</span> <span class="nc">Meta</span><span class="p">:</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">CustomUser</span>
<span class="n">fields</span> <span class="o">=</span> <span class="p">(</span><span class="s1">'email'</span><span class="p">,)</span>
</code></pre>
<h2 id="admin">Admin</h2>
<p>Tell the admin to use these forms by subclassing <code>UserAdmin</code> in <em>users/admin.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib</span> <span class="kn">import</span> <span class="n">admin</span>
<span class="kn">from</span> <span class="nn">django.contrib.auth.admin</span> <span class="kn">import</span> <span class="n">UserAdmin</span>

<span class="kn">from</span> <span class="nn">.forms</span> <span class="kn">import</span> <span class="n">CustomUserCreationForm</span><span class="p">,</span> <span class="n">CustomUserChangeForm</span>
<span class="kn">from</span> <span class="nn">.models</span> <span class="kn">import</span> <span class="n">CustomUser</span>


<span class="k">class</span> <span class="nc">CustomUserAdmin</span><span class="p">(</span><span class="n">UserAdmin</span><span class="p">):</span>
<span class="n">add_form</span> <span class="o">=</span> <span class="n">CustomUserCreationForm</span>
<span class="n">form</span> <span class="o">=</span> <span class="n">CustomUserChangeForm</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">CustomUser</span>
<span class="n">list_display</span> <span class="o">=</span> <span class="p">(</span><span class="s1">'email'</span><span class="p">,</span> <span class="s1">'is_staff'</span><span class="p">,</span> <span class="s1">'is_active'</span><span class="p">,)</span>
<span class="n">list_filter</span> <span class="o">=</span> <span class="p">(</span><span class="s1">'email'</span><span class="p">,</span> <span class="s1">'is_staff'</span><span class="p">,</span> <span class="s1">'is_active'</span><span class="p">,)</span>
<span class="n">fieldsets</span> <span class="o">=</span> <span class="p">(</span>
<span class="p">(</span><span class="kc">None</span><span class="p">,</span> <span class="p">{</span><span class="s1">'fields'</span><span class="p">:</span> <span class="p">(</span><span class="s1">'email'</span><span class="p">,</span> <span class="s1">'password'</span><span class="p">)}),</span>
<span class="p">(</span><span class="s1">'Permissions'</span><span class="p">,</span> <span class="p">{</span><span class="s1">'fields'</span><span class="p">:</span> <span class="p">(</span><span class="s1">'is_staff'</span><span class="p">,</span> <span class="s1">'is_active'</span><span class="p">)}),</span>
<span class="p">)</span>
<span class="n">add_fieldsets</span> <span class="o">=</span> <span class="p">(</span>
<span class="p">(</span><span class="kc">None</span><span class="p">,</span> <span class="p">{</span>
<span class="s1">'classes'</span><span class="p">:</span> <span class="p">(</span><span class="s1">'wide'</span><span class="p">,),</span>
<span class="s1">'fields'</span><span class="p">:</span> <span class="p">(</span><span class="s1">'email'</span><span class="p">,</span> <span class="s1">'password1'</span><span class="p">,</span> <span class="s1">'password2'</span><span class="p">,</span> <span class="s1">'is_staff'</span><span class="p">,</span> <span class="s1">'is_active'</span><span class="p">)}</span>
<span class="p">),</span>
<span class="p">)</span>
<span class="n">search_fields</span> <span class="o">=</span> <span class="p">(</span><span class="s1">'email'</span><span class="p">,)</span>
<span class="n">ordering</span> <span class="o">=</span> <span class="p">(</span><span class="s1">'email'</span><span class="p">,)</span>


<span class="n">admin</span><span class="o">.</span><span class="n">site</span><span class="o">.</span><span class="n">register</span><span class="p">(</span><span class="n">CustomUser</span><span class="p">,</span> <span class="n">CustomUserAdmin</span><span class="p">)</span>
</code></pre>
