---
layout: post
title: Concurrent Web Scraping with Selenium Grid and Docker Swarm
date: 2019-03-15 16:20:23 +0900
category: Docker
tag: Docker
---

<h1>Concurrent Web Scraping with Selenium Grid and Docker Swarm</h1>
<p><em>Dependencies</em>:</p>
<ol>
<li>Docker v20.10.13</li>
<li>Python v3.10.4</li>
<li>Selenium v4.1.3</li>
</ol>
<li>Docker v20.10.13</li>
<li>Python v3.10.4</li>
<li>Selenium v4.1.3</li>

<h2 id="getting-started">First Thing First</h2>
<p>Start by cloning down the base project with the web scraping script, create and activate a virtual environment, and install the dependencies:</p>
<pre><span></span><code>$ git clone https://github.com/ShihabYasin/selenium-with-docker-swarm.git --branch base --single-branch
$ <span class="nb">cd</span> selenium-grid-docker-swarm
$ python3.10 -m venv env
$ <span class="nb">source</span> env/bin/activate
<span class="o">(</span>env<span class="o">)</span>$ pip install -r requirements.txt
</code></pre>
<p>The above commands may differ depending on your environment.</p>
<p>Test out the scraper:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python project/script.py
</code></pre>
<p>You should see something similar to:</p>
<pre><span></span><code>Scraping random Wikipedia page...
<span class="o">[</span>
<span class="o">{</span>
<span class="s1">'url'</span>: <span class="s1">'https://en.wikipedia.org/wiki/Andreas_Reinke'</span>,
<span class="s1">'title'</span>: <span class="s1">'Andreas Reinke'</span>,
<span class="s1">'last_modified'</span>: <span class="s1">' This page was last edited on 10 January 2022, at 23:11\xa0(UTC).'</span>
<span class="o">}</span>
<span class="o">]</span>
Finished!
</code></pre>
<p>Essentially, the script makes a request to <a href="https://en.wikipedia.org/wiki/Wikipedia:Random">Wikipedia:Random</a> -- <code>https://en.wikipedia.org/wiki/Special:Random</code> -- for information about the random article using <a href="http://www.seleniumhq.org/projects/webdriver/">Selenium</a> to automate interaction with the site and <a href="https://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a> to parse the HTML.</p>
<p>It's a modified version of the scraper built in the <a href="/blog/building-a-concurrent-web-scraper-with-python-and-selenium">Building A Concurrent Web Scraper With Python and Selenium</a> tutorial. Please review the tutorial along with the code from the script for more info.</p>
<h2 id="configuring-selenium-grid">Configuring Selenium Grid</h2>
<p>Next, let's spin up <a href="https://www.selenium.dev/documentation/en/grid/">Selenium Grid</a> to simplify the running of the script in parallel on multiple machines. We'll also use Docker and Docker Compose to manage those machines with minimal installation and configuration.</p>
<p>Add a <em>docker-compose.yml</em> file to the root directory:</p>
<pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">'3.8'</span><span class="w"></span>

<span class="nt">services</span><span class="p">:</span><span class="w"></span>

<span class="w">  </span><span class="nt">hub</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">selenium/hub:4.1.3</span><span class="w"></span>
<span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">4442:4442</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">4443:4443</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">4444:4444</span><span class="w"></span>

<span class="w">  </span><span class="nt">chrome</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">selenium/node-chrome:4.1.3</span><span class="w"></span>
<span class="w">    </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">hub</span><span class="w"></span>
<span class="w">    </span><span class="nt">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SE_EVENT_BUS_HOST=hub</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SE_EVENT_BUS_PUBLISH_PORT=4442</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SE_EVENT_BUS_SUBSCRIBE_PORT=4443</span><span class="w"></span>
</code></pre>
<p>Here, we used the official <a href="https://hub.docker.com/r/selenium/">Selenium Docker</a> images to set up a basic Selenium Grid that consists of a hub and a single Chrome node. We used the <code>4.1.3</code> tag, which is associated with the following versions of Selenium, WebDriver, Chrome, and Firefox:</p>
<li>Selenium: 4.1.3</li>
<li>Google Chrome: 99.0.4844.84</li>
<li>ChromeDriver: 99.0.4844.51</li>
<li>Mozilla Firefox: 98.0.2</li>
<li>Geckodriver: 0.30.0</li>
<p>Want to use different versions? Find the appropriate tag from the <a href="https://github.com/SeleniumHQ/docker-selenium/releases">releases</a> page.</p>
<p>Pull and run the images:</p>
<pre><span></span><code>$ docker-compose up -d
</code></pre>
<p>Navigate to <a href="http://localhost:4444">http://localhost:4444</a> in your browser to ensure that the hub is up and running with one Chrome node:</p>

<p>Since Selenium Hub is running on a different machine (within the Docker container), we need to configure the remote driver in <em>project/scrapers/scraper.py</em>:</p>
<pre><span></span><code><span class="k">def</span> <span class="nf">get_driver</span><span class="p">():</span>
<span class="n">options</span> <span class="o">=</span> <span class="n">webdriver</span><span class="o">.</span><span class="n">ChromeOptions</span><span class="p">()</span>
<span class="n">options</span><span class="o">.</span><span class="n">add_argument</span><span class="p">(</span><span class="s2">"--headless"</span><span class="p">)</span>

<span class="c1"># initialize driver</span>
<span class="n">driver</span> <span class="o">=</span> <span class="n">webdriver</span><span class="o">.</span><span class="n">Remote</span><span class="p">(</span>
<span class="n">command_executor</span><span class="o">=</span><span class="s1">'http://localhost:4444/wd/hub'</span><span class="p">,</span>
<span class="n">desired_capabilities</span><span class="o">=</span><span class="n">DesiredCapabilities</span><span class="o">.</span><span class="n">CHROME</span><span class="p">)</span>
<span class="k">return</span> <span class="n">driver</span>
</code></pre>
<p>Add the import:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">selenium.webdriver.common.desired_capabilities</span> <span class="kn">import</span> <span class="n">DesiredCapabilities</span>
</code></pre>
<p>Run the scraper again:</p>
<pre><span></span><code><span class="o">(</span>env<span class="o">)</span>$ python project/script.py
</code></pre>
<p>While the scraper is running, you should see "Sessions" change to one, indicating that it's in use:
</p>

