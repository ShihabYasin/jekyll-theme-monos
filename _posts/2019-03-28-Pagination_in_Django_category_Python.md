---
layout: post
title: Pagination in Django
date: 2019-03-28 16:20:23 +0900
category: Python
tag: Python
---

<h1>Pagination in Django</h1>
<p>Find code <a href="https://github.com/ShihabYasin/simple-django-pagination">here.</a> </p>
<h2 id="django-constructs">Django Constructs</h2>
<p>When implementing pagination in Django, rather than re-inventing the logic required for pagination, you'll work with the following constructs:</p>
<ol>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/paginator/#paginator-class">Paginator</a> - splits a Django QuerySet or list into chunks of <code>Page</code> objects.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/paginator/#page-class">Page</a> - holds the actual paginated data along with pagination metadata.</li>
</ol>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/paginator/#paginator-class">Paginator</a> - splits a Django QuerySet or list into chunks of <code>Page</code> objects.</li>
<li><a href="https://docs.djangoproject.com/en/4.0/ref/paginator/#page-class">Page</a> - holds the actual paginated data along with pagination metadata.</li>
<p>Let's look at some quick examples.</p>
<h3 id="paginator">Paginator</h3>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>


<span class="k">for</span> <span class="n">num</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">43</span><span class="p">):</span>
<span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">create</span><span class="p">(</span><span class="n">username</span><span class="o">=</span><span class="sa">f</span><span class="s2">"</span><span class="si">{</span><span class="n">num</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</code></pre>
<p>Here, we created 43 User objects.</p>
<p>Next, we'll import the <code>Paginator</code> class and create a new instance:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django.core.paginator</span> <span class="kn">import</span> <span class="n">Paginator</span>

<span class="n">users</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>

<span class="n">paginator</span> <span class="o">=</span> <span class="n">Paginator</span><span class="p">(</span><span class="n">users</span><span class="p">,</span> <span class="mi">10</span><span class="p">)</span>

<span class="nb">print</span><span class="p">(</span><span class="n">paginator</span><span class="o">.</span><span class="n">num_pages</span><span class="p">)</span>  <span class="c1"># =&gt; 5</span>
</code></pre>
<p>The <code>Paginator</code> class takes four parameters:</p>
<ol>
<li><code>object_list</code> - any object with a <code>count()</code> or <code>__len__()</code> method, like a list, tuple, or QuerySet</li>
<li><code>per_page</code> - maximum number of items to include on a page</li>
<li><code>orphans</code> (optional) - used to prevent the last page from having very few items, defaults to <code>0</code></li>
<li><code>allow_empty_first_page</code> (optional) - as implied by the name, you can raise an <code>EmtpyPage</code> error if you disallow the first page from being empty by setting the argument to <code>False</code>, defaults to <code>True</code></li>
</ol>
<li><code>object_list</code> - any object with a <code>count()</code> or <code>__len__()</code> method, like a list, tuple, or QuerySet</li>
<li><code>per_page</code> - maximum number of items to include on a page</li>
<li><code>orphans</code> (optional) - used to prevent the last page from having very few items, defaults to <code>0</code></li>
<li><code>allow_empty_first_page</code> (optional) - as implied by the name, you can raise an <code>EmtpyPage</code> error if you disallow the first page from being empty by setting the argument to <code>False</code>, defaults to <code>True</code></li>
<p>So, in the above example, we sliced the users into pages (or chunks) of ten. The first four pages will have ten users while the last page will have three.</p>
<p>The <code>Paginator</code> class has the following <a href="https://docs.djangoproject.com/en/4.0/ref/paginator/#attributes">attributes</a>:</p>
<ol>
<li><code>count</code> - total number of objects</li>
<li><code>num_pages</code> - total number of pages</li>
<li><code>page_range</code> - range iterator of page numbers</li>
</ol>
<li><code>count</code> - total number of objects</li>
<li><code>num_pages</code> - total number of pages</li>
<li><code>page_range</code> - range iterator of page numbers</li>
<p>For consistent paginated results, the QuerySet or the model should be ordered.</p>
<p>If you'd prefer to not have just three users on the final page, you can use the <a href="https://docs.djangoproject.com/en/4.0/ref/paginator/#django.core.paginator.Paginator.orphans">orphans</a> argument like so to add the final three users to the previous page:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django.core.paginator</span> <span class="kn">import</span> <span class="n">Paginator</span>

<span class="n">users</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>

<span class="n">paginator</span> <span class="o">=</span> <span class="n">Paginator</span><span class="p">(</span><span class="n">users</span><span class="p">,</span> <span class="mi">10</span><span class="p">,</span> <span class="n">orphans</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>

<span class="nb">print</span><span class="p">(</span><span class="n">paginator</span><span class="o">.</span><span class="n">num_pages</span><span class="p">)</span>  <span class="c1"># =&gt; 4</span>
</code></pre>
<p>So, when the number of remaining objects for the last page is less than or equal to the value of <code>orphans</code>, those objects will be added to the previous page.</p>
<h3 id="page">Page</h3>
<p>After the Django QuerySet has been broken up into <code>Page</code> objects. We can then use the <code>page()</code> method to access the data for each page by passing the page number to it:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django.core.paginator</span> <span class="kn">import</span> <span class="n">Paginator</span>

<span class="n">users</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>

<span class="n">paginator</span> <span class="o">=</span> <span class="n">Paginator</span><span class="p">(</span><span class="n">users</span><span class="p">,</span> <span class="mi">10</span><span class="p">)</span>

<span class="n">page_obj</span> <span class="o">=</span> <span class="n">paginator</span><span class="o">.</span><span class="n">page</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>

<span class="nb">print</span><span class="p">(</span><span class="n">page_obj</span><span class="p">)</span>  <span class="c1"># =&gt; &lt;Page 1 of 5&gt;</span>
</code></pre>
<p>Here, <code>page_obj</code> gives us a page object that represents the first page of results. This can then be used in your templates.</p>
<p>Note that we didn't literally create a <code>Page</code> instance. Instead, we obtained the instance from the Paginator class.</p>
<p>What happens if the page doesn't exist?</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django.core.paginator</span> <span class="kn">import</span> <span class="n">Paginator</span>

<span class="n">users</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>

<span class="n">paginator</span> <span class="o">=</span> <span class="n">Paginator</span><span class="p">(</span><span class="n">users</span><span class="p">,</span> <span class="mi">10</span><span class="p">)</span>

<span class="n">page_obj</span> <span class="o">=</span> <span class="n">paginator</span><span class="o">.</span><span class="n">page</span><span class="p">(</span><span class="mi">99</span><span class="p">)</span>
</code></pre>
<p>You should see:</p>
<pre><span></span><code>    raise EmptyPage<span class="o">(</span>_<span class="o">(</span><span class="s1">'That page contains no results'</span><span class="o">))</span>
django.core.paginator.EmptyPage: That page contains no results
</code></pre>
<p>Thus, it's a good idea to catch an <code>EmptyPage</code> exception like so:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django.core.paginator</span> <span class="kn">import</span> <span class="n">EmptyPage</span><span class="p">,</span> <span class="n">Paginator</span>

<span class="n">users</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>

<span class="n">paginator</span> <span class="o">=</span> <span class="n">Paginator</span><span class="p">(</span><span class="n">users</span><span class="p">,</span> <span class="mi">10</span><span class="p">)</span>

<span class="k">try</span><span class="p">:</span>
<span class="n">page_obj</span> <span class="o">=</span> <span class="n">paginator</span><span class="o">.</span><span class="n">page</span><span class="p">(</span><span class="mi">99</span><span class="p">)</span>
<span class="k">except</span> <span class="n">EmptyPage</span><span class="p">:</span>
<span class="c1"># Do something</span>
<span class="k">pass</span>
</code></pre>
<p>You may want to catch a <code>PageNotAnInteger</code> exception as well.</p>
<p>For more on this, review the <a href="https://docs.djangoproject.com/en/4.0/ref/paginator/#exceptions">Exceptions</a> section from the Paginator documentation.</p>
<p>That said, if you'd prefer not to deal with the <code>EmptyPage</code> or <code>PageNotAnInteger</code> exceptions explicitly, you could use <a href="https://docs.djangoproject.com/en/4.0/ref/paginator/#django.core.paginator.Paginator.get_page">get_page()</a> method instead of <code>page()</code>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django.core.paginator</span> <span class="kn">import</span> <span class="n">Paginator</span>

<span class="n">users</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>

<span class="n">paginator</span> <span class="o">=</span> <span class="n">Paginator</span><span class="p">(</span><span class="n">users</span><span class="p">,</span> <span class="mi">10</span><span class="p">)</span>

<span class="n">page_obj</span> <span class="o">=</span> <span class="n">paginator</span><span class="o">.</span><span class="n">get_page</span><span class="p">(</span><span class="mi">99</span><span class="p">)</span>

<span class="nb">print</span><span class="p">(</span><span class="n">page_obj</span><span class="p">)</span>  <span class="c1"># =&gt; &lt;Page 5 of 5&gt;</span>
</code></pre>
<p>So, even though the number <code>99</code> is beyond the range, the last page will be returned.</p>
<p>Also, if the page isn't a valid number <code>get_page()</code> will return, by default, the first page:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django.core.paginator</span> <span class="kn">import</span> <span class="n">Paginator</span>

<span class="n">users</span> <span class="o">=</span> <span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>

<span class="n">paginator</span> <span class="o">=</span> <span class="n">Paginator</span><span class="p">(</span><span class="n">users</span><span class="p">,</span> <span class="mi">10</span><span class="p">)</span>

<span class="n">page_obj</span> <span class="o">=</span> <span class="n">paginator</span><span class="o">.</span><span class="n">get_page</span><span class="p">(</span><span class="s1">'foo'</span><span class="p">)</span>

<span class="nb">print</span><span class="p">(</span><span class="n">page_obj</span><span class="p">)</span>  <span class="c1"># =&gt; &lt;Page 1 of 5&gt;</span>
</code></pre>
<p>Therefore, both methods -- <code>page()</code> or <code>get_page()</code> -- can be used depending on your preferences. The examples shown in this article will use <code>page()</code>.</p>
<p>The <code>Page</code> object has several <a href="https://docs.djangoproject.com/en/4.0/ref/paginator/#id2">attributes</a> and <a href="https://docs.djangoproject.com/en/4.0/ref/paginator/#id1">methods</a> that can be used while constructing your template:</p>
<ol>
<li><code>number</code> - shows the page number for a given page</li>
<li><code>paginator</code> - displays the associated <code>Paginator</code> object</li>
<li><code>has_next()</code> - returns <code>True</code> if there's a next page</li>
<li><code>has_previous()</code> - - returns <code>True</code> if there's a previous page</li>
<li><code>next_page_number()</code> - returns the number of the next page</li>
<li><code>previous_page_number()</code> - returns the number of the previous page</li>
</ol>
<li><code>number</code> - shows the page number for a given page</li>
<li><code>paginator</code> - displays the associated <code>Paginator</code> object</li>
<li><code>has_next()</code> - returns <code>True</code> if there's a next page</li>
<li><code>has_previous()</code> - - returns <code>True</code> if there's a previous page</li>
<li><code>next_page_number()</code> - returns the number of the next page</li>
<li><code>previous_page_number()</code> - returns the number of the previous page</li>
<h2 id="function-based-views">Function-based Views</h2>
<p>Next, let's look at how to work with pagination in function-based views:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.core.paginator</span> <span class="kn">import</span> <span class="n">Paginator</span><span class="p">,</span> <span class="n">EmptyPage</span><span class="p">,</span> <span class="n">PageNotAnInteger</span>
<span class="kn">from</span> <span class="nn">django.shortcuts</span> <span class="kn">import</span> <span class="n">render</span>

<span class="kn">from</span> <span class="nn">.</span> <span class="n">models</span> <span class="kn">import</span> <span class="nn">Employee</span>


<span class="k">def</span> <span class="nf">index</span><span class="p">(</span><span class="n">request</span><span class="p">):</span>
<span class="n">object_list</span> <span class="o">=</span> <span class="n">Employee</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">all</span><span class="p">()</span>
<span class="n">page_num</span> <span class="o">=</span> <span class="n">request</span><span class="o">.</span><span class="n">GET</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">'page'</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>

<span class="n">paginator</span> <span class="o">=</span> <span class="n">Paginator</span><span class="p">(</span><span class="n">object_list</span><span class="p">,</span> <span class="mi">6</span><span class="p">)</span> <span class="c1"># 6 employees per page</span>


<span class="k">try</span><span class="p">:</span>
<span class="n">page_obj</span> <span class="o">=</span> <span class="n">paginator</span><span class="o">.</span><span class="n">page</span><span class="p">(</span><span class="n">page_num</span><span class="p">)</span>
<span class="k">except</span> <span class="n">PageNotAnInteger</span><span class="p">:</span>
<span class="c1"># if page is not an integer, deliver the first page</span>
<span class="n">page_obj</span> <span class="o">=</span> <span class="n">paginator</span><span class="o">.</span><span class="n">page</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
<span class="k">except</span> <span class="n">EmptyPage</span><span class="p">:</span>
<span class="c1"># if the page is out of range, deliver the last page</span>
<span class="n">page_obj</span> <span class="o">=</span> <span class="n">paginator</span><span class="o">.</span><span class="n">page</span><span class="p">(</span><span class="n">paginator</span><span class="o">.</span><span class="n">num_pages</span><span class="p">)</span>

<span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="s1">'index.html'</span><span class="p">,</span> <span class="p">{</span><span class="s1">'page_obj'</span><span class="p">:</span> <span class="n">page_obj</span><span class="p">})</span>
</code></pre>
<p>Here, we:</p>
<ol>
<li>Defined a <code>page_num</code> variable from the URL.</li>
<li>Instantiated the <code>Paginator</code> class passing it the required parameters, the <code>employees</code> QuerySet and the number of employees to be included on each page.</li>
<li>Generated a page object called <code>page_obj</code>, which contains the paginated employee data along with metadata for navigating to the previous and next pages.</li>
</ol>
<li>Defined a <code>page_num</code> variable from the URL.</li>
<li>Instantiated the <code>Paginator</code> class passing it the required parameters, the <code>employees</code> QuerySet and the number of employees to be included on each page.</li>
<li>Generated a page object called <code>page_obj</code>, which contains the paginated employee data along with metadata for navigating to the previous and next pages.</li>

<h2 id="class-based-views">Class-based Views</h2>
<p>Example of implementing pagination in a class-based view:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.views.generic</span> <span class="kn">import</span> <span class="n">ListView</span>

<span class="kn">from</span> <span class="nn">.</span> <span class="n">models</span> <span class="kn">import</span> <span class="nn">Employee</span>


<span class="k">class</span> <span class="nc">Index</span><span class="p">(</span><span class="n">ListView</span><span class="p">):</span>
<span class="n">model</span> <span class="o">=</span> <span class="n">Employee</span>
<span class="n">context_object_name</span> <span class="o">=</span> <span class="s1">'employees'</span>
<span class="n">paginate_by</span> <span class="o">=</span> <span class="mi">6</span>
<span class="n">template_name</span> <span class="o">=</span> <span class="s1">'index.html'</span>
</code></pre>

<h2 id="templates">Templates</h2>
<p>Working with pagination in the template is where things start to get interesting, as there are several different implementations. In this article, we'll look at three different implementations, each showing a different way in which to navigate to the previous and next pages.</p>


<p>So, in this example, we have "Previous" and "Next" links that the end-user can click to move from page to page.</p>
<p><em>index.html</em>:</p>
<pre><span></span><code><span class="cp">&lt;!doctype html&gt;</span>
<span class="p">&lt;</span><span class="nt">html</span> <span class="na">lang</span><span class="o">=</span><span class="s">"en"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">head</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">meta</span> <span class="na">charset</span><span class="o">=</span><span class="s">"utf-8"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">meta</span> <span class="na">name</span><span class="o">=</span><span class="s">"viewport"</span> <span class="na">content</span><span class="o">=</span><span class="s">"width=device-width, initial-scale=1"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">link</span> <span class="na">href</span><span class="o">=</span><span class="s">"https://cdn.jsdelivr.net/npm/<a class="__cf_email__" data-cfemail="02606d6d76717670637242372c322c30" href="/cdn-cgi/l/email-protection">[email protected]</a>/dist/css/bootstrap.min.css"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">title</span><span class="p">&gt;</span>Pagination in Django<span class="p">&lt;/</span><span class="nt">title</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">head</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">body</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">div</span> <span class="na">class</span><span class="o">=</span><span class="s">"container"</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">h1</span> <span class="na">class</span><span class="o">=</span><span class="s">"text-center"</span><span class="p">&gt;</span>List of Employees<span class="p">&lt;/</span><span class="nt">h1</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">hr</span><span class="p">&gt;</span>

<span class="p">&lt;</span><span class="nt">ul</span> <span class="na">class</span><span class="o">=</span><span class="s">"list-group list-group-flush"</span><span class="p">&gt;</span>
{% for employee in page_obj %}
<span class="p">&lt;</span><span class="nt">li</span> <span class="na">class</span><span class="o">=</span><span class="s">"list-group-item"</span><span class="p">&gt;</span>{{ employee }}<span class="p">&lt;/</span><span class="nt">li</span><span class="p">&gt;</span>
{% endfor %}
<span class="p">&lt;/</span><span class="nt">ul</span><span class="p">&gt;</span>

<span class="p">&lt;</span><span class="nt">br</span><span class="p">&gt;&lt;</span><span class="nt">hr</span><span class="p">&gt;</span>

{% include "pagination.html" %}
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">body</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">html</span><span class="p">&gt;</span>
</code></pre>
<p><em>pagination.html</em>:</p>
<pre><span></span><code><span class="p">&lt;</span><span class="nt">div</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">span</span><span class="p">&gt;</span>
{% if page_obj.has_previous %}
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"?page={{ page_obj.previous_page_number }}"</span><span class="p">&gt;</span>Previous<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% endif %}
<span class="p">&lt;</span><span class="nt">span</span><span class="p">&gt;</span>
Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
<span class="p">&lt;/</span><span class="nt">span</span><span class="p">&gt;</span>
{% if page_obj.has_next %}
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"?page={{ page_obj.next_page_number }}"</span><span class="p">&gt;</span>Next<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% endif %}
<span class="p">&lt;/</span><span class="nt">span</span><span class="p">&gt;</span>
<span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
</code></pre>
<p>Keep in mind that the <em>pagination.html</em> template can be reused across many templates.</p>
<h3 id="flavor-2">Flavor 2</h3>

<p><em>pagination.html</em>:</p>
<pre><span></span><code>{% if page_obj.has_previous %}
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"?page={{ page_obj.previous_page_number }}"</span><span class="p">&gt;</span>Previous<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% else %}
<span class="p">&lt;</span><span class="nt">a</span><span class="p">&gt;</span>Previous<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% endif %}

{% for i in page_obj.paginator.page_range %}
{% if page_obj.number == i %}
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"#"</span><span class="p">&gt;</span>{{ i }} <span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% else %}
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"?page={{ i }}"</span><span class="p">&gt;</span>{{ i }}<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% endif %}
{% endfor %}

{% if page_obj.has_next %}
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"?page={{ page_obj.next_page_number }}"</span><span class="p">&gt;</span>Next<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% else %}
<span class="p">&lt;</span><span class="nt">a</span><span class="p">&gt;</span>Next<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% endif %}
</code></pre>
<p>This flavor presents all the page numbers in the UI, making it easier to navigate to different pages.</p>
<h3 id="flavor-3">Flavor 3</h3>

<p><em>pagination.html</em>:</p>
<pre><span></span><code>{% if page_obj.has_previous %}
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"?page={{ page_obj.previous_page_number }}"</span><span class="p">&gt;</span>« Previous page<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>

{% if page_obj.number &gt; 3 %}
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"?page=1"</span><span class="p">&gt;</span>1<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% if page_obj.number &gt; 4 %}
<span class="p">&lt;</span><span class="nt">span</span><span class="p">&gt;</span>...<span class="p">&lt;/</span><span class="nt">span</span><span class="p">&gt;</span>
{% endif %}
{% endif %}
{% endif %}

{% for num in page_obj.paginator.page_range %}
{% if page_obj.number == num %}
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"?page={{ num }}"</span><span class="p">&gt;</span>{{ num }}<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% elif num &gt; page_obj.number|add:'-3' and num <span class="p">&lt;</span> <span class="nt">page_obj.number</span><span class="err">|</span><span class="na">add:</span><span class="err">'</span><span class="na">3</span><span class="err">'</span> <span class="err">%}</span>
<span class="err">&lt;</span><span class="na">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"?page={{ num }}"</span><span class="p">&gt;</span>{{ num }}<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% endif %}
{% endfor %}

{% if page_obj.has_next %}
{% if page_obj.number <span class="p">&lt;</span> <span class="nt">page_obj.paginator.num_pages</span><span class="err">|</span><span class="na">add:</span><span class="err">'</span><span class="na">-3</span><span class="err">'</span> <span class="err">%}</span>
<span class="err">&lt;</span><span class="na">span</span><span class="p">&gt;</span>...<span class="p">&lt;/</span><span class="nt">span</span><span class="p">&gt;</span>
<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"?page={{ page_obj.paginator.num_pages }}"</span><span class="p">&gt;</span>{{ page_obj.paginator.num_pages }}<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% elif page_obj.number <span class="p">&lt;</span> <span class="nt">page_obj.paginator.num_pages</span><span class="err">|</span><span class="na">add:</span><span class="err">'</span><span class="na">-2</span><span class="err">'</span> <span class="err">%}</span>
<span class="err">&lt;</span><span class="na">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"?page={{ page_obj.paginator.num_pages }}"</span><span class="p">&gt;</span>{{ page_obj.paginator.num_pages }}<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% endif %}

<span class="p">&lt;</span><span class="nt">a</span> <span class="na">href</span><span class="o">=</span><span class="s">"?page={{ page_obj.next_page_number }}"</span><span class="p">&gt;</span>Next Page »<span class="p">&lt;/</span><span class="nt">a</span><span class="p">&gt;</span>
{% endif %}
</code></pre>
<p>If you have a large number of pages, you may want to look at this third and final flavor.</p>
