---
layout: post
title: Django Caching
date: 2019-03-16 16:20:23 +0900
category: Django
tag: Django
---

<h1 class="pw-post-title ig ih ii bn ij ik il im in io ip iq ir is it iu iv iw ix iy iz ja jb jc jd je gj" id="30fc">Application Logging with Fluentd Elasticsearch and Kibana</h1>


<h2 class="lw ju ii bn jv lx ly lz jz ma mb mc kd lc md me kh lg mf mg kl lk mh mi kp mj gj" id="0c5c">Steps:</h2>
<li class="mk ml ii kt b ku kv ky kz lc mm lg mn lk mo lo mp mq mr ms gj" id="d9e9">Install from APT repository</li>
<pre class="mt mu mv mw ga mx bt my"><span class="gj lw ju ii mz b do na nb l nc" id="2810">curl -L <a class="au lv" href="https://toolbelt.treasuredata.com/sh/install-ubuntu-bionic-td-agent3.sh" rel="noopener ugc nofollow" target="_blank">https://toolbelt.treasuredata.com/sh/install-ubuntu-bionic-td-agent3.sh</a> | sh<br/></span></pre>
<li class="mk ml ii kt b ku lp ky lq lc nd lg ne lk nf lo mp mq mr ms gj" id="6d5b">Launch the daemon using systemd.</li>
<pre class="mt mu mv mw ga mx bt my"><span class="gj lw ju ii mz b do na nb l nc" id="3a71">sudo systemctl start td-agent</span></pre>
<li class="mk ml ii kt b ku lp ky lq lc nd lg ne lk nf lo mp mq mr ms gj" id="68a7">Check the status of service using below command</li>
<pre class="mt mu mv mw ga mx bt my"><span class="gj lw ju ii mz b do na nb l nc" id="cdb7">systemctl status td-agent</span></pre>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="30c4"><strong class="kt ij">Init.d</strong></p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="f98d">After installation of td-agent you will be provided with startup scripts (/etc/init.d/td-agent) to manage td-agent daemon.</p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="d7db"><strong class="kt ij">Setting up Elasticsearch</strong></p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="4750">Before installing ELK make sure you have Java 8 if not you can install it using sudo apt install openjdk-8-jdk. <a class="au lv" href="https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html" rel="noopener ugc nofollow" target="_blank">Installation</a></p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="7d41"><strong class="kt ij">Setting up Kibana using Docker</strong></p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="a823">Kibana and Elasticsearch release are linked with each other so for every release of ELK a same version of kibana will be published. Every version of kibana is only compatible with the same version of ELK.</p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="bd56">For avoiding a mess on our system if things go terribly wrong we will use the docker image of kibana at <a class="au lv" href="https://hub.docker.com/_/kibana" rel="noopener ugc nofollow" target="_blank">Docker Image Kibana</a>. As I have ELK 7.1.1 I will pull Kibana with tag 7.1.1 using docker pull.</p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="530a">To run kibana use below command</p>
<pre class="mt mu mv mw ga mx bt my"><span class="gj lw ju ii mz b do na nb l nc" id="dbfa">docker run -d — name kibana — net somenetwork -p 5601:5601 kibana:7.1.1</span></pre>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="1d6c">You can skip specifying network unless you are linking two containers.</p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="5f11">If you want to use Elasticsearch running on your host machine use below command to connect to your local Elasticsearch instance:</p>
<pre class="mt mu mv mw ga mx bt my"><span class="gj lw ju ii mz b do na nb l nc" id="4162">docker run -d --name kibana --net host -e “ELASTICSEARCH_HOSTS=http://localhost:9200” kibana:7.1.1</span></pre>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="45ef">You can verify kibana container running and connecting to your Elasticsearch using below command:</p>
<pre class="mt mu mv mw ga mx bt my"><span class="gj lw ju ii mz b do na nb l nc" id="fe37">docker logs -f kibana</span></pre>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="45bd"><strong class="kt ij">NOTE</strong>: By default, kibana image assumes ELK container with “elasticsearch” name exists within the same network and so tries to connect using <a class="au lv" href="http://elasticsearch:9200" rel="noopener ugc nofollow" target="_blank">http://elasticsearch:9200</a> using the service discovery feature of docker. <a class="au lv" href="https://docs.docker.com/network/" rel="noopener ugc nofollow" target="_blank">Docker Networks</a></p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="c70b"><strong class="kt ij">NodeJS API Server</strong></p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="1c4b"><strong class="kt ij">Configure FluentD</strong></p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="5937">Configuring Fluentd or td-agent is straight forward and all the plugins configuration are written in fluentd.conf or td-agent.conf. Config location can be either :</p>
<pre class="mt mu mv mw ga mx bt my"><span class="gj lw ju ii mz b do na nb l nc" id="9cdc">/etc/td-agent/td-agent.conf </span><span class="gj lw ju ii mz b do nj nk nl nm nn nb l nc" id="b514">// or</span><span class="gj lw ju ii mz b do nj nk nl nm nn nb l nc" id="41ab">/etc/fluentd/fluent.conf</span></pre>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="cf26">As we are using Elastic search plugin for sending data out to Elasticsearch we will need fluentd-plugin-elasticsearch output plugin which you can install using gem.</p>
<pre class="mt mu mv mw ga mx bt my"><span class="gj lw ju ii mz b do na nb l nc" id="73d4">gem install fluent-plugin-elasticsearch 2.4.0</span></pre>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="df09">More about Fluentd plugins <a class="au lv" href="https://docs.fluentd.org/output" rel="noopener ugc nofollow" target="_blank">Output Plugins</a></p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="4deb">Final td-agent.conf:</p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="67c2"><strong class="kt ij">Searching logs in Kibana</strong></p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="da45">Once the plugin configuration is setuped you can reload fluentd to reflect new plugins configuration. You can open kibana dashboard on your machine at localhost:5601</p>
<p class="pw-post-body-paragraph kr ks ii kt b ku lp kw kx ky lq la lb lc lr le lf lg ls li lj lk lt lm ln lo ib gj" id="6444">And search for messages in the search box using DSL.</p>