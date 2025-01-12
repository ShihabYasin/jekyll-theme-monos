---
layout: post
title: Concurrent-Web-Scraping-with-Python-and-Selenium
date: 2019-03-02 16:20:23 +0900
category: Selenium
tag: Selenium
---

# Web Scraping with Python and Selenium ( Concurrent, Parallel, AsyncIO versions compare )

### * Checkout codebase [here](https://github.com/ShihabYasin/concurrent-webscrapping-python)


## How to run:
1. Prepare virtual environment.

<pre class="code" style="background-color: rgb(217,238,239,255);">
$ python -m venv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
</pre>

2. Install ChromeDriver globally( e.g. this [one](https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/) )

3. Run different scrapers:

<pre class="code" style="background-color: rgb(217,238,239,255);">
# sync styled, makes 20 requests to https://en.wikipedia.org/wiki/Special:Random
(env)$ python script.py headless

# parallel with multiprocessing
(env)$ python script_parallel_1.py headless

# parallel with concurrent.futures
(env)$ python script_parallel_2.py headless

# concurrent with concurrent.futures (according to theory should be the fastest)
(env)$ python script_concurrent.py headless

# parallel with concurrent.futures and concurrent with asyncio
(env)$ python script_asyncio.py headless
</pre>Will get output like below:
<pre class="code" style="background-color: rgb(217,238,239,255);">
(env)$ python script.py
Scraping Wikipedia #1 time(s)...
Scraping Wikipedia #2 time(s)...
...
Scraping Wikipedia #19 time(s)...
Scraping Wikipedia #20 time(s)...
Elapsed run time: 57.36561393737793 seconds
</pre>
<pre class="code" style="background-color: rgb(217,238,239,255);">
(env)$ python script_concurrent.py

Elapsed run time: 11.831077098846436 seconds
</pre>
<pre class="code" style="background-color: rgb(217,238,239,255);">
(env)$ python script_concurrent.py headless

Running in headless mode
Elapsed run time: 6.222846269607544 seconds
</pre>4. Run the tests:

<pre class="code" style="background-color: rgb(217,238,239,255);">
(env)$ python -m pytest test/test_scraper_mock.py
(env)$ python -m pytest test/test_scraper.py
</pre>Will get output like below:
<pre class="code" style="background-color: rgb(217,238,239,255);">
(env)$ python -m pytest test/test_scraper_mock.py

================================ test session starts =================================
platform darwin -- Python 3.10.0, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /Users/michael/repos/testdriven/async-web-scraping
collected 3 items

test/test_scraper.py ...                                                       [100%]

================================= 3 passed in 0.27s =================================
</pre>

<pre class="code" style="background-color: rgb(217,238,239,255);">
(env)$ python -m pytest test/test_scraper.py

================================ test session starts =================================
platform darwin -- Python 3.10.0, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /Users/michael/repos/testdriven/async-web-scraping
collected 3 items

test/test_scraper.py ...                                                       [100%]

================================= 3 passed in 0.19 ==================================
</pre>

<pre class="code" style="background-color: rgb(217,238,239,255);">

</pre>
