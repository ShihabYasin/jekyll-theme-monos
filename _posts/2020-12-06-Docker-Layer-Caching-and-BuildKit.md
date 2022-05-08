---
layout: post
title: Docker-Layer-Caching-and-BuildKit
date: 2020-12-06 16:20:23 +0900
category: ["DevOps", "Docker"]
tag: ["DevOps", "Docker"] 
---



## Docker Layer Caching and BuildKit 

<main>




<h2 id="docker-layer-caching">Docker Layer Caching</h2>
<p>Docker caches each layer as an image is built, and each layer will only be re-built if it or the layer above it has changed since the last build. So, you can significantly speed up builds with Docker cache. Let's take a look at a quick example.</p>
<p><em>Dockerfile</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="c"># pull base image</span>
<span class="k">FROM</span><span class="w"> </span><span class="s">python:3.9.7-slim</span>

<span class="c"># install netcat</span>
<span class="k">RUN</span><span class="w"> </span>apt-get update <span class="o">&amp;&amp;</span> <span class="se">\</span>
   apt-get -y install netcat <span class="o">&amp;&amp;</span> <span class="se">\</span>
   apt-get clean

<span class="c"># set working directory</span>
<span class="k">WORKDIR</span><span class="w"> </span><span class="s">/usr/src/app</span>

<span class="c"># install requirements</span>
<span class="k">COPY</span><span class="w"> </span>./requirements.txt .
<span class="k">RUN</span><span class="w"> </span>pip install -r requirements.txt

<span class="c"># add app</span>
<span class="k">COPY</span><span class="w"> </span>. .

<span class="c"># run server</span>
<span class="k">CMD</span><span class="w"> </span>gunicorn -b <span class="m">0</span>.0.0.0:5000 manage:app
</code></pre></div>

<p>The first Docker build can take several minutes to complete, depending on your connection speed. Subsequent builds should only take a few seconds since the layers get cached after that first build:</p>
<div class="codehilite"><pre><span></span><code><span class="o">[</span>+<span class="o">]</span> Building <span class="m">0</span>.4s <span class="o">(</span><span class="m">12</span>/12<span class="o">)</span> <span class="nv">FINISHED</span>
<span class="o">=</span>&gt; <span class="o">[</span>internal<span class="o">]</span> load build definition from Dockerfile                                                                     <span class="m">0</span>.0s
<span class="o">=</span>&gt; <span class="o">=</span>&gt; transferring dockerfile: 37B                                                                                      <span class="m">0</span>.0s
<span class="o">=</span>&gt; <span class="o">[</span>internal<span class="o">]</span> load .dockerignore                                                                                        <span class="m">0</span>.0s
<span class="o">=</span>&gt; <span class="o">=</span>&gt; transferring context: 35B                                                                                         <span class="m">0</span>.0s
<span class="o">=</span>&gt; <span class="o">[</span>internal<span class="o">]</span> load metadata <span class="k">for</span> docker.io/library/python:3.9.7-slim                                                     <span class="m">0</span>.3s
<span class="o">=</span>&gt; <span class="o">[</span>internal<span class="o">]</span> load build context                                                                                        <span class="m">0</span>.0s
<span class="o">=</span>&gt; <span class="o">=</span>&gt; transferring context: 555B                                                                                        <span class="m">0</span>.0s
<span class="o">=</span>&gt; <span class="o">[</span><span class="m">1</span>/7<span class="o">]</span> FROM docker.io/library/python:<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="bb889582958c96c8d7d2d6fbc8d3da898e8d">[email&#160;protected]</a>:bdefda2b80c5b4d993ef83d2445d81b2b894bf627b62bd7b0f01244de2b6a  <span class="m">0</span>.0s
<span class="o">=</span>&gt; CACHED <span class="o">[</span><span class="m">2</span>/7<span class="o">]</span> RUN apt-get update <span class="o">&amp;&amp;</span>     apt-get -y install netcat <span class="o">&amp;&amp;</span>     apt-get clean                                <span class="m">0</span>.0s
<span class="o">=</span>&gt; CACHED <span class="o">[</span><span class="m">3</span>/7<span class="o">]</span> WORKDIR /usr/src/app                                                                                    <span class="m">0</span>.0s
<span class="o">=</span>&gt; CACHED <span class="o">[</span><span class="m">4</span>/7<span class="o">]</span> COPY ./requirements.txt .                                                                               <span class="m">0</span>.0s
<span class="o">=</span>&gt; CACHED <span class="o">[</span><span class="m">5</span>/7<span class="o">]</span> RUN pip install -r requirements.txt                                                                     <span class="m">0</span>.0s
<span class="o">=</span>&gt; CACHED <span class="o">[</span><span class="m">6</span>/7<span class="o">]</span> COPY project .                                                                                          <span class="m">0</span>.0s
<span class="o">=</span>&gt; CACHED <span class="o">[</span><span class="m">7</span>/7<span class="o">]</span> COPY manage.py .                                                                                        <span class="m">0</span>.0s
<span class="o">=</span>&gt; exporting to image                                                                                                   <span class="m">0</span>.0s
<span class="o">=</span>&gt; <span class="o">=</span>&gt; exporting layers                                                                                                  <span class="m">0</span>.0s
<span class="o">=</span>&gt; <span class="o">=</span>&gt; writing image sha256:2b8b7c5a6d1b77d5bcd689ab265b0281ad531bd2e34729cff82285f5abdcb59f                             <span class="m">0</span>.0s
<span class="o">=</span>&gt; <span class="o">=</span>&gt; naming to docker.io/library/cache                                                                                 <span class="m">0</span>.0s
</code></pre></div>

<p>Even if you make a change to the source code it should still only take a few seconds to build as the dependencies will not need to be downloaded. Only the last two layers have to be re-built, in other words:</p>
<div class="codehilite"><pre><span></span><code> <span class="o">=</span>&gt; <span class="o">[</span><span class="m">6</span>/7<span class="o">]</span> COPY project .
<span class="o">=</span>&gt; <span class="o">[</span><span class="m">7</span>/7<span class="o">]</span> COPY manage.py .
</code></pre></div>

<p>To avoid invalidating the cache:</p>
<ol>
<li>Start your Dockerfile with commands that are less likely to change</li>
<li>Place commands that are more likely to change (like <code>COPY . .</code>) as late as possible</li>
<li>Add only the necessary files (use a <em>.dockerignore</em> file)</li>
</ol>

<h2 id="buildkit">BuildKit</h2>
<p>If you're using a Docker version &gt;= <a href="https://docs.docker.com/engine/release-notes/#19030">19.03</a> you can use BuildKit, a container image builder, in place of the traditional image builder back-end inside the Docker engine. Without BuildKit, if an image doesn't exist on your local image registry, you would need to pull the remote images before building in order to take advantage of Docker layer caching.</p>
<p>Example:</p>
<div class="codehilite"><pre><span></span><code>$ docker pull mjhea0/docker-ci-cache:latest

$ docker docker build --tag mjhea0/docker-ci-cache:latest .
</code></pre></div>

<p>With BuildKit, you don't need to pull the remote images before building since it caches each build layer in your image registry. Then, when you build the image, each layer is downloaded as needed during the build.</p>
<p>To enable BuildKit, set the <code>DOCKER_BUILDKIT</code> environment variable to <code>1</code>. Then, to turn on the inline layer caching, use the <code>BUILDKIT_INLINE_CACHE</code> build argument.</p>
<p>Example:</p>
<div class="codehilite"><pre><span></span><code><span class="nb">export</span> <span class="nv">DOCKER_BUILDKIT</span><span class="o">=</span><span class="m">1</span>

<span class="c1"># Build and cache image</span>
$ docker build --tag mjhea0/docker-ci-cache:latest --build-arg <span class="nv">BUILDKIT_INLINE_CACHE</span><span class="o">=</span><span class="m">1</span> .

<span class="c1"># Build image from remote cache</span>
$ docker build --cache-from mjhea0/docker-ci-cache:latest .
</code></pre></div>

<h2 id="ci-environments">CI Environments</h2>
<p>Since CI platforms provide a fresh environment for every build, you'll need to use a remote image registry as the source of the cache for BuildKit's layer caching.</p>
<p>Steps:</p>
<ol>
<li>
<p>Log in to the image registry (like <a href="https://hub.docker.com/">Docker Hub</a>, <a href="https://aws.amazon.com/ecr/">Elastic Container Registry</a> (ECR), and <a href="https://quay.io/">Quay</a>, to name a few).</p>

</li>
<li>
<p>Use Docker build's <code>--cache-from</code> <a href="https://docs.docker.com/engine/reference/commandline/build/#options">option</a> to use the existing image as the cache source.</p>
</li>
<li>Push the new image to the registry if the build is successful.</li>
</ol>
<p>Let's look at how to do this on CircleCI, GitLab CI, and GitHub Actions, using both single and multi-stage Docker builds with and without Docker Compose. Each of the examples use Docker Hub as the image registry with <code>REGISTRY_USER</code> and <code>REGISTRY_PASS</code> set as variables in the CI builds in order to push to and pull from the registry.</p>

<h2 id="single-stage-builds">Single-stage Builds</h2>
<p>CircleCI:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># _config-examples/single-stage/circle.yml</span><span class="w"></span>

<span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">2.1</span><span class="w"></span>

<span class="nt">jobs</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">machine</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">ubuntu-2004:202010-01</span><span class="w"></span>
<span class="w">    </span><span class="nt">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">CACHE_IMAGE</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache</span><span class="w"></span>
<span class="w">      </span><span class="nt">DOCKER_BUILDKIT</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>
<span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">checkout</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Log in to docker hub</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker login -u $REGISTRY_USER -p $REGISTRY_PASS</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build from dockerfile</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="p p-Indicator">|</span><span class="w"></span>
<span class="w">            </span><span class="no">docker build \</span><span class="w"></span>
<span class="w">              </span><span class="no">--cache-from $CACHE_IMAGE:latest \</span><span class="w"></span>
<span class="w">              </span><span class="no">--tag $CACHE_IMAGE:latest \</span><span class="w"></span>
<span class="w">              </span><span class="no">--build-arg BUILDKIT_INLINE_CACHE=1 \</span><span class="w"></span>
<span class="w">              </span><span class="no">&quot;.&quot;</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Push to docker hub</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:latest</span><span class="w"></span>
</code></pre></div>

<p>GitLab CI:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># _config-examples/single-stage/.gitlab-ci.yml</span><span class="w"></span>

<span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker:stable</span><span class="w"></span>
<span class="nt">services</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker:dind</span><span class="w"></span>

<span class="nt">variables</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">DOCKER_DRIVER</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">overlay2</span><span class="w"></span>
<span class="w">  </span><span class="nt">CACHE_IMAGE</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache</span><span class="w"></span>
<span class="w">  </span><span class="nt">DOCKER_BUILDKIT</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>

<span class="nt">stages</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">build</span><span class="w"></span>

<span class="nt">docker-build</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">stage</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">build</span><span class="w"></span>
<span class="w">  </span><span class="nt">before_script</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker login -u $REGISTRY_USER -p $REGISTRY_PASS</span><span class="w"></span>
<span class="w">  </span><span class="nt">script</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker build</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--cache-from $CACHE_IMAGE:latest</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--tag $CACHE_IMAGE:latest</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--file ./Dockerfile</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--build-arg BUILDKIT_INLINE_CACHE=1</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">&quot;.&quot;</span><span class="w"></span>
<span class="w">  </span><span class="nt">after_script</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:latest</span><span class="w"></span>
</code></pre></div>

<p>GitHub Actions:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># _config-examples/single-stage/github.yml</span><span class="w"></span>

<span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Docker Build</span><span class="w"></span>

<span class="nt">on</span><span class="p">:</span><span class="w"> </span><span class="p p-Indicator">[</span><span class="nv">push</span><span class="p p-Indicator">]</span><span class="w"></span>

<span class="nt">env</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">CACHE_IMAGE</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache</span><span class="w"></span>
<span class="w">  </span><span class="nt">DOCKER_BUILDKIT</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>

<span class="nt">jobs</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build Docker Image</span><span class="w"></span>
<span class="w">    </span><span class="nt">runs-on</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">ubuntu-latest</span><span class="w"></span>
<span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Checkout master</span><span class="w"></span>
<span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">actions/<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="0e6d666b6d65617b7a4e783f">[email&#160;protected]</a></span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Log in to docker hub</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker login -u ${{ secrets.REGISTRY_USER }} -p ${{ secrets.REGISTRY_PASS }}</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build from dockerfile</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="p p-Indicator">|</span><span class="w"></span>
<span class="w">          </span><span class="no">docker build \</span><span class="w"></span>
<span class="w">            </span><span class="no">--cache-from $CACHE_IMAGE:latest \</span><span class="w"></span>
<span class="w">            </span><span class="no">--tag $CACHE_IMAGE:latest \</span><span class="w"></span>
<span class="w">            </span><span class="no">--build-arg BUILDKIT_INLINE_CACHE=1 \</span><span class="w"></span>
<span class="w">            </span><span class="no">&quot;.&quot;</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Push to docker hub</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:latest</span><span class="w"></span>
</code></pre></div>

<h3 id="compose">Compose</h3>
<p>If you're using Docker Compose, you can add the <code>cache_from</code> <a href="https://docs.docker.com/compose/compose-file/compose-file-v3/#cache_from">option</a> to the compose file, which maps back to the <code>docker build --cache-from &lt;image&gt;</code> command when you run <code>docker-compose build</code>.</p>
<p>Example:</p>
<div class="codehilite"><pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">&#39;3.8&#39;</span><span class="w"></span>

<span class="nt">services</span><span class="p">:</span><span class="w"></span>

<span class="w">  </span><span class="nt">web</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">.</span><span class="w"></span>
<span class="w">      </span><span class="nt">cache_from</span><span class="p">:</span><span class="w"></span>
<span class="w">        </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache:latest</span><span class="w"></span>
<span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache:latest</span><span class="w"></span>
</code></pre></div>

<p>To take advantage of BuildKit, make sure you're using a version of Docker Compose &gt;= <a href="https://github.com/docker/compose/releases/tag/1.25.0">1.25.0</a>. To enable BuildKit, set the <code>DOCKER_BUILDKIT</code> and <code>COMPOSE_DOCKER_CLI_BUILD</code> environment variables to <code>1</code>. Then, again, to turn on the inline layer caching, use the <code>BUILDKIT_INLINE_CACHE</code> build argument.</p>
<p>CircleCI:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># _config-examples/single-stage/compose/circle.yml</span><span class="w"></span>

<span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">2.1</span><span class="w"></span>

<span class="nt">jobs</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">machine</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">ubuntu-2004:202010-01</span><span class="w"></span>
<span class="w">    </span><span class="nt">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">CACHE_IMAGE</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache</span><span class="w"></span>
<span class="w">      </span><span class="nt">DOCKER_BUILDKIT</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>
<span class="w">      </span><span class="nt">COMPOSE_DOCKER_CLI_BUILD</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>
<span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">checkout</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Log in to docker hub</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker login -u $REGISTRY_USER -p $REGISTRY_PASS</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build images</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker-compose build --build-arg BUILDKIT_INLINE_CACHE=1</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Push to docker hub</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:latest</span><span class="w"></span>
</code></pre></div>

<p>GitLab CI:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># _config-examples/single-stage/compose/.gitlab-ci.yml</span><span class="w"></span>

<span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker/compose:latest</span><span class="w"></span>
<span class="nt">services</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker:dind</span><span class="w"></span>

<span class="nt">variables</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">DOCKER_DRIVER</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">overlay2</span><span class="w"></span>
<span class="w">  </span><span class="nt">CACHE_IMAGE</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache</span><span class="w"></span>
<span class="w">  </span><span class="nt">DOCKER_BUILDKIT</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>
<span class="w">  </span><span class="nt">COMPOSE_DOCKER_CLI_BUILD</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>

<span class="nt">stages</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">build</span><span class="w"></span>

<span class="nt">docker-build</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">stage</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">build</span><span class="w"></span>
<span class="w">  </span><span class="nt">before_script</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker login -u $REGISTRY_USER -p $REGISTRY_PASS</span><span class="w"></span>
<span class="w">  </span><span class="nt">script</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker-compose build --build-arg BUILDKIT_INLINE_CACHE=1</span><span class="w"></span>
<span class="w">  </span><span class="nt">after_script</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:latest</span><span class="w"></span>
</code></pre></div>

<p>GitHub Actions:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># _config-examples/single-stage/compose/github.yml</span><span class="w"></span>

<span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Docker Build</span><span class="w"></span>

<span class="nt">on</span><span class="p">:</span><span class="w"> </span><span class="p p-Indicator">[</span><span class="nv">push</span><span class="p p-Indicator">]</span><span class="w"></span>

<span class="nt">env</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">CACHE_IMAGE</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache</span><span class="w"></span>
<span class="w">  </span><span class="nt">DOCKER_BUILDKIT</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>
<span class="w">  </span><span class="nt">COMPOSE_DOCKER_CLI_BUILD</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>

<span class="nt">jobs</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build Docker Image</span><span class="w"></span>
<span class="w">    </span><span class="nt">runs-on</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">ubuntu-latest</span><span class="w"></span>
<span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Checkout master</span><span class="w"></span>
<span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">actions/<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="30535855535b5f4544704601">[email&#160;protected]</a></span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Log in to docker hub</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker login -u ${{ secrets.REGISTRY_USER }} -p ${{ secrets.REGISTRY_PASS }}</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build Docker images</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker-compose build --build-arg BUILDKIT_INLINE_CACHE=1</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Push to docker hub</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:latest</span><span class="w"></span>
</code></pre></div>

<h2 id="multi-stage-builds">Multi-stage Builds</h2>
<p>With the <a href="https://docs.docker.com/develop/develop-images/multistage-build/">multi-stage build</a> pattern, you'll have to apply the same workflow (build, then push) for each intermediate stage since those images are discarded before the final image is created. The <code>--target</code> <a href="https://docs.docker.com/compose/compose-file/compose-file-v3/#target">option</a> can be used to build each stage of the multi-stage build separately.</p>
<p><em>Dockerfile.multi</em>:</p>
<div class="codehilite"><pre><span></span><code><span class="c"># base</span>
<span class="k">FROM</span><span class="w"> </span><span class="s">python:3.9.7</span><span class="w"> </span><span class="k">as</span><span class="w"> </span><span class="s">base</span>
<span class="k">COPY</span><span class="w"> </span>./requirements.txt /
<span class="k">RUN</span><span class="w"> </span>pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

<span class="c"># stage</span>
<span class="k">FROM</span><span class="w"> </span><span class="s">python:3.9.7-slim</span>
<span class="k">RUN</span><span class="w"> </span>apt-get update <span class="o">&amp;&amp;</span> <span class="se">\</span>
   apt-get -y install netcat <span class="o">&amp;&amp;</span> <span class="se">\</span>
   apt-get clean
<span class="k">WORKDIR</span><span class="w"> </span><span class="s">/usr/src/app</span>
<span class="k">COPY</span><span class="w"> </span>--from<span class="o">=</span>base /wheels /wheels
<span class="k">COPY</span><span class="w"> </span>--from<span class="o">=</span>base requirements.txt .
<span class="k">RUN</span><span class="w"> </span>pip install --no-cache /wheels/*
<span class="k">COPY</span><span class="w"> </span>. /usr/src/app
<span class="k">CMD</span><span class="w"> </span>gunicorn -b <span class="m">0</span>.0.0.0:5000 manage:app
</code></pre></div>

<p>CircleCI:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># _config-examples/multi-stage/circle.yml</span><span class="w"></span>

<span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">2.1</span><span class="w"></span>

<span class="nt">jobs</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">machine</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">ubuntu-2004:202010-01</span><span class="w"></span>
<span class="w">    </span><span class="nt">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">CACHE_IMAGE</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache</span><span class="w"></span>
<span class="w">      </span><span class="nt">DOCKER_BUILDKIT</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>
<span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">checkout</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Log in to docker hub</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker login -u $REGISTRY_USER -p $REGISTRY_PASS</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build base from dockerfile</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="p p-Indicator">|</span><span class="w"></span>
<span class="w">            </span><span class="no">docker build \</span><span class="w"></span>
<span class="w">              </span><span class="no">--target base \</span><span class="w"></span>
<span class="w">              </span><span class="no">--cache-from $CACHE_IMAGE:base \</span><span class="w"></span>
<span class="w">              </span><span class="no">--tag $CACHE_IMAGE:base \</span><span class="w"></span>
<span class="w">              </span><span class="no">--file ./Dockerfile.multi \</span><span class="w"></span>
<span class="w">              </span><span class="no">--build-arg BUILDKIT_INLINE_CACHE=1 \</span><span class="w"></span>
<span class="w">              </span><span class="no">&quot;.&quot;</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build stage from dockerfile</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="p p-Indicator">|</span><span class="w"></span>
<span class="w">            </span><span class="no">docker build \</span><span class="w"></span>
<span class="w">              </span><span class="no">--cache-from $CACHE_IMAGE:base \</span><span class="w"></span>
<span class="w">              </span><span class="no">--cache-from $CACHE_IMAGE:stage \</span><span class="w"></span>
<span class="w">              </span><span class="no">--tag $CACHE_IMAGE:stage \</span><span class="w"></span>
<span class="w">              </span><span class="no">--file ./Dockerfile.multi \</span><span class="w"></span>
<span class="w">              </span><span class="no">--build-arg BUILDKIT_INLINE_CACHE=1 \</span><span class="w"></span>
<span class="w">              </span><span class="no">&quot;.&quot;</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Push base image to docker hub</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:base</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Push stage image to docker hub</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:stage</span><span class="w"></span>
</code></pre></div>

<p>GitLab CI:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># _config-examples/multi-stage/.gitlab-ci.yml</span><span class="w"></span>

<span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker:stable</span><span class="w"></span>
<span class="nt">services</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker:dind</span><span class="w"></span>


<span class="nt">variables</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">DOCKER_DRIVER</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">overlay2</span><span class="w"></span>
<span class="w">  </span><span class="nt">CACHE_IMAGE</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache</span><span class="w"></span>
<span class="w">  </span><span class="nt">DOCKER_BUILDKIT</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>

<span class="nt">stages</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">build</span><span class="w"></span>

<span class="nt">docker-build</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">stage</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">build</span><span class="w"></span>
<span class="w">  </span><span class="nt">before_script</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker login -u $REGISTRY_USER -p $REGISTRY_PASS</span><span class="w"></span>
<span class="w">  </span><span class="nt">script</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker build</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--target base</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--cache-from $CACHE_IMAGE:base</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--tag $CACHE_IMAGE:base</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--file ./Dockerfile.multi</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--build-arg BUILDKIT_INLINE_CACHE=1</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">&quot;.&quot;</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker build</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--cache-from $CACHE_IMAGE:base</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--cache-from $CACHE_IMAGE:stage</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--tag $CACHE_IMAGE:stage</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--file ./Dockerfile.multi</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--build-arg BUILDKIT_INLINE_CACHE=1</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">&quot;.&quot;</span><span class="w"></span>
<span class="w">  </span><span class="nt">after_script</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:stage</span><span class="w"></span>
</code></pre></div>

<p>GitHub Actions:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># _config-examples/multi-stage/github.yml</span><span class="w"></span>

<span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Docker Build</span><span class="w"></span>

<span class="nt">on</span><span class="p">:</span><span class="w"> </span><span class="p p-Indicator">[</span><span class="nv">push</span><span class="p p-Indicator">]</span><span class="w"></span>

<span class="nt">env</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">CACHE_IMAGE</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache</span><span class="w"></span>
<span class="w">  </span><span class="nt">DOCKER_BUILDKIT</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>

<span class="nt">jobs</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build Docker Image</span><span class="w"></span>
<span class="w">    </span><span class="nt">runs-on</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">ubuntu-latest</span><span class="w"></span>
<span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Checkout master</span><span class="w"></span>
<span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">actions/<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="5d3e35383e363228291d2b6c">[email&#160;protected]</a></span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Log in to docker hub</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker login -u ${{ secrets.REGISTRY_USER }} -p ${{ secrets.REGISTRY_PASS }}</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build base from dockerfile</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="p p-Indicator">|</span><span class="w"></span>
<span class="w">          </span><span class="no">docker build \</span><span class="w"></span>
<span class="w">            </span><span class="no">--target base \</span><span class="w"></span>
<span class="w">            </span><span class="no">--cache-from $CACHE_IMAGE:base \</span><span class="w"></span>
<span class="w">            </span><span class="no">--tag $CACHE_IMAGE:base \</span><span class="w"></span>
<span class="w">            </span><span class="no">--file ./Dockerfile.multi \</span><span class="w"></span>
<span class="w">            </span><span class="no">--build-arg BUILDKIT_INLINE_CACHE=1 \</span><span class="w"></span>
<span class="w">            </span><span class="no">&quot;.&quot;</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build stage from dockerfile</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="p p-Indicator">|</span><span class="w"></span>
<span class="w">          </span><span class="no">docker build \</span><span class="w"></span>
<span class="w">            </span><span class="no">--cache-from $CACHE_IMAGE:base \</span><span class="w"></span>
<span class="w">            </span><span class="no">--cache-from $CACHE_IMAGE:stage \</span><span class="w"></span>
<span class="w">            </span><span class="no">--tag $CACHE_IMAGE:stage \</span><span class="w"></span>
<span class="w">            </span><span class="no">--file ./Dockerfile.multi \</span><span class="w"></span>
<span class="w">            </span><span class="no">--build-arg BUILDKIT_INLINE_CACHE=1 \</span><span class="w"></span>
<span class="w">            </span><span class="no">&quot;.&quot;</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Push base image to docker hub</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:base</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Push stage image to docker hub</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:stage</span><span class="w"></span>
</code></pre></div>

<h3 id="compose_1">Compose</h3>
<p>Example compose file:</p>
<div class="codehilite"><pre><span></span><code><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s">&#39;3.8&#39;</span><span class="w"></span>

<span class="nt">services</span><span class="p">:</span><span class="w"></span>

<span class="w">  </span><span class="nt">web</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">.</span><span class="w"></span>
<span class="w">      </span><span class="nt">cache_from</span><span class="p">:</span><span class="w"></span>
<span class="w">        </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache:stage</span><span class="w"></span>
<span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache:stage</span><span class="w"></span>
</code></pre></div>

<p>CircleCI:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># _config-examples/multi-stage/compose/circle.yml</span><span class="w"></span>

<span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">2.1</span><span class="w"></span>

<span class="nt">jobs</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">machine</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">ubuntu-2004:202010-01</span><span class="w"></span>
<span class="w">    </span><span class="nt">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="nt">CACHE_IMAGE</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache</span><span class="w"></span>
<span class="w">      </span><span class="nt">DOCKER_BUILDKIT</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>
<span class="w">      </span><span class="nt">COMPOSE_DOCKER_CLI_BUILD</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>
<span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">checkout</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Log in to docker hub</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker login -u $REGISTRY_USER -p $REGISTRY_PASS</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build base from dockerfile</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="p p-Indicator">|</span><span class="w"></span>
<span class="w">            </span><span class="no">docker build \</span><span class="w"></span>
<span class="w">              </span><span class="no">--target base \</span><span class="w"></span>
<span class="w">              </span><span class="no">--cache-from $CACHE_IMAGE:base \</span><span class="w"></span>
<span class="w">              </span><span class="no">--tag $CACHE_IMAGE:base \</span><span class="w"></span>
<span class="w">              </span><span class="no">--file ./Dockerfile.multi \</span><span class="w"></span>
<span class="w">              </span><span class="no">--build-arg BUILDKIT_INLINE_CACHE=1 \</span><span class="w"></span>
<span class="w">              </span><span class="no">&quot;.&quot;</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build Docker images</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker-compose -f docker-compose.multi.yml build --build-arg BUILDKIT_INLINE_CACHE=1</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Push base image to docker hub</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:base</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">run</span><span class="p">:</span><span class="w"></span>
<span class="w">          </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Push stage image to docker hub</span><span class="w"></span>
<span class="w">          </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:stage</span><span class="w"></span>
</code></pre></div>

<p>GitLab CI:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># _config-examples/multi-stage/compose/.gitlab-ci.yml</span><span class="w"></span>

<span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker/compose:latest</span><span class="w"></span>
<span class="nt">services</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker:dind</span><span class="w"></span>

<span class="nt">variables</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">DOCKER_DRIVER</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">overlay</span><span class="w"></span>
<span class="w">  </span><span class="nt">CACHE_IMAGE</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache</span><span class="w"></span>
<span class="w">  </span><span class="nt">DOCKER_BUILDKIT</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>
<span class="w">  </span><span class="nt">COMPOSE_DOCKER_CLI_BUILD</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>

<span class="nt">stages</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">build</span><span class="w"></span>

<span class="nt">docker-build</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">stage</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">build</span><span class="w"></span>
<span class="w">  </span><span class="nt">before_script</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker login -u $REGISTRY_USER -p $REGISTRY_PASS</span><span class="w"></span>
<span class="w">  </span><span class="nt">script</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker build</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--target base</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--cache-from $CACHE_IMAGE:base</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--tag $CACHE_IMAGE:base</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--file ./Dockerfile.multi</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">--build-arg BUILDKIT_INLINE_CACHE=1</span><span class="w"></span>
<span class="w">        </span><span class="l l-Scalar l-Scalar-Plain">&quot;.&quot;</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker-compose -f docker-compose.multi.yml build --build-arg BUILDKIT_INLINE_CACHE=1</span><span class="w"></span>
<span class="w">  </span><span class="nt">after_script</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:base</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:stage</span><span class="w"></span>
</code></pre></div>

<p>GitHub Actions:</p>
<div class="codehilite"><pre><span></span><code><span class="c1"># _config-examples/multi-stage/compose/github.yml</span><span class="w"></span>

<span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Docker Build</span><span class="w"></span>

<span class="nt">on</span><span class="p">:</span><span class="w"> </span><span class="p p-Indicator">[</span><span class="nv">push</span><span class="p p-Indicator">]</span><span class="w"></span>

<span class="nt">env</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">CACHE_IMAGE</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">mjhea0/docker-ci-cache</span><span class="w"></span>
<span class="w">  </span><span class="nt">DOCKER_BUILDKIT</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>
<span class="w">  </span><span class="nt">COMPOSE_DOCKER_CLI_BUILD</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">1</span><span class="w"></span>

<span class="nt">jobs</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build Docker Image</span><span class="w"></span>
<span class="w">    </span><span class="nt">runs-on</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">ubuntu-latest</span><span class="w"></span>
<span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Checkout master</span><span class="w"></span>
<span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">actions/<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="53303b3630383c2627132562">[email&#160;protected]</a></span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Log in to docker hub</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker login -u ${{ secrets.REGISTRY_USER }} -p ${{ secrets.REGISTRY_PASS }}</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build base from dockerfile</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="p p-Indicator">|</span><span class="w"></span>
<span class="w">          </span><span class="no">docker build \</span><span class="w"></span>
<span class="w">            </span><span class="no">--target base \</span><span class="w"></span>
<span class="w">            </span><span class="no">--cache-from $CACHE_IMAGE:base \</span><span class="w"></span>
<span class="w">            </span><span class="no">--tag $CACHE_IMAGE:base \</span><span class="w"></span>
<span class="w">            </span><span class="no">--file ./Dockerfile.multi \</span><span class="w"></span>
<span class="w">            </span><span class="no">--build-arg BUILDKIT_INLINE_CACHE=1 \</span><span class="w"></span>
<span class="w">            </span><span class="no">&quot;.&quot;</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Build images</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker-compose -f docker-compose.multi.yml build --build-arg BUILDKIT_INLINE_CACHE=1</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Push base image to docker hub</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:base</span><span class="w"></span>
<span class="w">      </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Push stage image to docker hub</span><span class="w"></span>
<span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">docker push $CACHE_IMAGE:stage</span><span class="w"></span>
</code></pre></div>


</main>


