---
layout: post
title: Logging in Kubernetes with Elasticsearch, Kibana, and Fluentd
date: 2019-04-06 16:20:23 +0900
category: Django
tag: Django
---

<h1 class="post-title" itemprop="name headline">Logging in Kubernetes with Elasticsearch, Kibana, and Fluentd</h1>



<h2 id="minikube">Minikube</h2>

<p>By default, the Minikube VM is configured to use 1GB of memory and 2 CPU cores. This is not sufficient for Elasticsearch, so be sure to increase the memory in your Docker <a href="https://docs.docker.com/docker-for-mac/#advanced">client</a> (for HyperKit) or directly in VirtualBox. Then, when you start Minikube, pass the memory and CPU options to it:</p>
<pre class="highlight"><code><span class="nv">$ </span>minikube start <span class="nt">--vm-driver</span><span class="o">=</span>hyperkit <span class="nt">--memory</span> 8192 <span class="nt">--cpus</span> 4

or

<span class="nv">$ </span>minikube start <span class="nt">--memory</span> 8192 <span class="nt">--cpus</span> 4
</code></pre>
<p>Once up, make sure you can view the dashboard:</p>
<pre class="highlight"><code><span class="nv">$ </span>minikube dashboard
</code></pre>
<p>Then, create a new namespace:</p>
<pre class="highlight"><code><span class="nv">$ </span>kubectl create namespace logging

namespace/logging created
</code></pre>
<p>If you run into problems with Minikube, it’s often best to remove it completely and start over.</p>
<p>For example:</p>
<pre class="highlight"><code><span class="nv">$ </span>minikube stop<span class="p">;</span> minikube delete
<span class="nv">$ </span>rm /usr/local/bin/minikube
<span class="nv">$ </span>rm <span class="nt">-rf</span> ~/.minikube
<span class="c"># re-download minikube</span>
<span class="nv">$ </span>minikube start
</code></pre>
<h2 id="elastic">Elastic</h2>
<p>We’ll start with <a href="https://www.elastic.co/products/elasticsearch">Elasticsearch</a>.</p>

<p><em>kubernetes/elastic.yaml</em>:</p>
<pre class="highlight"><code><span class="na">apiVersion</span><span class="pi">:</span> <span class="s">extensions/v1beta1</span>
<span class="na">kind</span><span class="pi">:</span> <span class="s">Deployment</span>
<span class="na">metadata</span><span class="pi">:</span>
<span class="na">name</span><span class="pi">:</span> <span class="s">elasticsearch</span>
<span class="na">spec</span><span class="pi">:</span>
<span class="na">selector</span><span class="pi">:</span>
<span class="na">matchLabels</span><span class="pi">:</span>
<span class="na">component</span><span class="pi">:</span> <span class="s">elasticsearch</span>
<span class="na">template</span><span class="pi">:</span>
<span class="na">metadata</span><span class="pi">:</span>
<span class="na">labels</span><span class="pi">:</span>
<span class="na">component</span><span class="pi">:</span> <span class="s">elasticsearch</span>
<span class="na">spec</span><span class="pi">:</span>
<span class="na">containers</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">elasticsearch</span>
<span class="na">image</span><span class="pi">:</span> <span class="s">docker.elastic.co/elasticsearch/elasticsearch:6.5.4</span>
<span class="na">env</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">discovery.type</span>
<span class="na">value</span><span class="pi">:</span> <span class="s">single-node</span>
<span class="na">ports</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">containerPort</span><span class="pi">:</span> <span class="s">9200</span>
<span class="na">name</span><span class="pi">:</span> <span class="s">http</span>
<span class="na">protocol</span><span class="pi">:</span> <span class="s">TCP</span>
<span class="na">resources</span><span class="pi">:</span>
<span class="na">limits</span><span class="pi">:</span>
<span class="na">cpu</span><span class="pi">:</span> <span class="s">500m</span>
<span class="na">memory</span><span class="pi">:</span> <span class="s">4Gi</span>
<span class="na">requests</span><span class="pi">:</span>
<span class="na">cpu</span><span class="pi">:</span> <span class="s">500m</span>
<span class="na">memory</span><span class="pi">:</span> <span class="s">4Gi</span>

<span class="nn">---</span>

<span class="na">apiVersion</span><span class="pi">:</span> <span class="s">v1</span>
<span class="na">kind</span><span class="pi">:</span> <span class="s">Service</span>
<span class="na">metadata</span><span class="pi">:</span>
<span class="na">name</span><span class="pi">:</span> <span class="s">elasticsearch</span>
<span class="na">labels</span><span class="pi">:</span>
<span class="na">service</span><span class="pi">:</span> <span class="s">elasticsearch</span>
<span class="na">spec</span><span class="pi">:</span>
<span class="na">type</span><span class="pi">:</span> <span class="s">NodePort</span>
<span class="na">selector</span><span class="pi">:</span>
<span class="na">component</span><span class="pi">:</span> <span class="s">elasticsearch</span>
<span class="na">ports</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">port</span><span class="pi">:</span> <span class="s">9200</span>
<span class="na">targetPort</span><span class="pi">:</span> <span class="s">9200</span>
</code></pre>
<p>So, this will spin up a <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks.html#single-node-discovery">single node</a> Elasticsearch pod in the cluster along with a <a href="https://kubernetes.io/docs/concepts/services-networking/service/#nodeport">NodePort</a> service to expose the pod to the outside world.</p>
<p>Create:</p>
<pre class="highlight"><code><span class="nv">$ </span>kubectl create <span class="nt">-f</span> kubernetes/elastic.yaml <span class="nt">-n</span> logging

deployment.extensions/elasticsearch created
service/elasticsearch created
</code></pre>
<p>Verify that both the pod and service were created:</p>
<pre class="highlight"><code><span class="nv">$ </span>kubectl get pods <span class="nt">-n</span> logging

NAME                          READY   STATUS    RESTARTS   AGE
elasticsearch-bb9f879-d9kmg   1/1     Running   0          75s


<span class="nv">$ </span>kubectl get service <span class="nt">-n</span> logging

NAME            TYPE       CLUSTER-IP       EXTERNAL-IP   PORT<span class="o">(</span>S<span class="o">)</span>          AGE
elasticsearch   NodePort   10.102.149.212   &lt;none&gt;        9200:30531/TCP   86s
</code></pre>
<p>Take note of the exposed port–e.g, <code class="highlighter-rouge">30531</code>. Then, grab the Minikube IP and make sure you can cURL that pod:</p>
<pre class="highlight"><code><span class="nv">$ </span>curl <span class="k">$(</span>minikube ip<span class="k">)</span>:30531
</code></pre>
<p>You should see something similar to:</p>
<pre class="highlight"><code><span class="o">{</span>
<span class="s2">"name"</span> : <span class="s2">"9b5Whvv"</span>,
<span class="s2">"cluster_name"</span> : <span class="s2">"docker-cluster"</span>,
<span class="s2">"cluster_uuid"</span> : <span class="s2">"-qMwo61ATv2KmbZsf2_Tpw"</span>,
<span class="s2">"version"</span> : <span class="o">{</span>
<span class="s2">"number"</span> : <span class="s2">"6.5.4"</span>,
<span class="s2">"build_flavor"</span> : <span class="s2">"default"</span>,
<span class="s2">"build_type"</span> : <span class="s2">"tar"</span>,
<span class="s2">"build_hash"</span> : <span class="s2">"d2ef93d"</span>,
<span class="s2">"build_date"</span> : <span class="s2">"2018-12-17T21:17:40.758843Z"</span>,
<span class="s2">"build_snapshot"</span> : <span class="nb">false</span>,
<span class="s2">"lucene_version"</span> : <span class="s2">"7.5.0"</span>,
<span class="s2">"minimum_wire_compatibility_version"</span> : <span class="s2">"5.6.0"</span>,
<span class="s2">"minimum_index_compatibility_version"</span> : <span class="s2">"5.0.0"</span>
<span class="o">}</span>,
<span class="s2">"tagline"</span> : <span class="s2">"You Know, for Search"</span>
<span class="o">}</span>
</code></pre>
<h2 id="kibana">Kibana</h2>
<p>Next, let’s get <a href="https://www.elastic.co/products/kibana">Kibana</a> up and running.</p>
<p><em>kubernetes/kibana.yaml</em>:</p>
<pre class="highlight"><code><span class="na">apiVersion</span><span class="pi">:</span> <span class="s">extensions/v1beta1</span>
<span class="na">kind</span><span class="pi">:</span> <span class="s">Deployment</span>
<span class="na">metadata</span><span class="pi">:</span>
<span class="na">name</span><span class="pi">:</span> <span class="s">kibana</span>
<span class="na">spec</span><span class="pi">:</span>
<span class="na">selector</span><span class="pi">:</span>
<span class="na">matchLabels</span><span class="pi">:</span>
<span class="na">run</span><span class="pi">:</span> <span class="s">kibana</span>
<span class="na">template</span><span class="pi">:</span>
<span class="na">metadata</span><span class="pi">:</span>
<span class="na">labels</span><span class="pi">:</span>
<span class="na">run</span><span class="pi">:</span> <span class="s">kibana</span>
<span class="na">spec</span><span class="pi">:</span>
<span class="na">containers</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">kibana</span>
<span class="na">image</span><span class="pi">:</span> <span class="s">docker.elastic.co/kibana/kibana:6.5.4</span>
<span class="na">env</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">ELASTICSEARCH_URL</span>
<span class="na">value</span><span class="pi">:</span> <span class="s">http://elasticsearch:9200</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">XPACK_SECURITY_ENABLED</span>
<span class="na">value</span><span class="pi">:</span> <span class="s2">"</span><span class="s">true"</span>
<span class="na">ports</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">containerPort</span><span class="pi">:</span> <span class="s">5601</span>
<span class="na">name</span><span class="pi">:</span> <span class="s">http</span>
<span class="na">protocol</span><span class="pi">:</span> <span class="s">TCP</span>

<span class="nn">---</span>

<span class="na">apiVersion</span><span class="pi">:</span> <span class="s">v1</span>
<span class="na">kind</span><span class="pi">:</span> <span class="s">Service</span>
<span class="na">metadata</span><span class="pi">:</span>
<span class="na">name</span><span class="pi">:</span> <span class="s">kibana</span>
<span class="na">labels</span><span class="pi">:</span>
<span class="na">service</span><span class="pi">:</span> <span class="s">kibana</span>
<span class="na">spec</span><span class="pi">:</span>
<span class="na">type</span><span class="pi">:</span> <span class="s">NodePort</span>
<span class="na">selector</span><span class="pi">:</span>
<span class="na">run</span><span class="pi">:</span> <span class="s">kibana</span>
<span class="na">ports</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">port</span><span class="pi">:</span> <span class="s">5601</span>
<span class="na">targetPort</span><span class="pi">:</span> <span class="s">5601</span>
</code></pre>
<p>Like before, this deployment will spin up a single Kibana pod that gets exposed via a NodePort service. Take note of the two environment variables:</p>
<ol>
<li><code class="highlighter-rouge">ELASTICSEARCH_URL</code> - URL of the Elasticsearch instance</li>
<li><code class="highlighter-rouge">XPACK_SECURITY_ENABLED</code> - enables <a href="https://www.elastic.co/guide/en/x-pack/current/elasticsearch-security.html">X-Pack security</a></li>
</ol>
<li><code class="highlighter-rouge">ELASTICSEARCH_URL</code> - URL of the Elasticsearch instance</li>
<li><code class="highlighter-rouge">XPACK_SECURITY_ENABLED</code> - enables <a href="https://www.elastic.co/guide/en/x-pack/current/elasticsearch-security.html">X-Pack security</a></li>
<p>Refer to the <a href="https://www.elastic.co/guide/en/kibana/current/docker.html">Running Kibana on Docker</a> guide for more info on these variables.</p>
<p>Create:</p>
<pre class="highlight"><code><span class="nv">$ </span>kubectl create <span class="nt">-f</span> kubernetes/kibana.yaml <span class="nt">-n</span> logging
</code></pre>
<p>Verify:</p>
<pre class="highlight"><code><span class="nv">$ </span>kubectl get pods <span class="nt">-n</span> logging

NAME                          READY   STATUS    RESTARTS   AGE
elasticsearch-bb9f879-d9kmg   1/1     Running   0          17m
kibana-7f6686674c-mjlb2       1/1     Running   0          60s


<span class="nv">$ </span>kubectl get service <span class="nt">-n</span> logging

NAME            TYPE       CLUSTER-IP       EXTERNAL-IP   PORT<span class="o">(</span>S<span class="o">)</span>          AGE
elasticsearch   NodePort   10.102.149.212   &lt;none&gt;        9200:30531/TCP   17m
kibana          NodePort   10.106.226.34    &lt;none&gt;        5601:32683/TCP   74s
</code></pre>
<p>Test this in your browser at <code class="highlighter-rouge">http://MINIKUBE_IP:KIBANA_EXPOSED_PORT</code>.</p>

<p>First, we need to configure RBAC (role-based access control) permissions so that Fluentd can access the appropriate components.</p>
<p><em>kubernetes/fluentd-rbac.yaml</em>:</p>
<pre class="highlight"><code><span class="na">apiVersion</span><span class="pi">:</span> <span class="s">v1</span>
<span class="na">kind</span><span class="pi">:</span> <span class="s">ServiceAccount</span>
<span class="na">metadata</span><span class="pi">:</span>
<span class="na">name</span><span class="pi">:</span> <span class="s">fluentd</span>
<span class="na">namespace</span><span class="pi">:</span> <span class="s">kube-system</span>

<span class="nn">---</span>

<span class="na">apiVersion</span><span class="pi">:</span> <span class="s">rbac.authorization.k8s.io/v1beta1</span>
<span class="na">kind</span><span class="pi">:</span> <span class="s">ClusterRole</span>
<span class="na">metadata</span><span class="pi">:</span>
<span class="na">name</span><span class="pi">:</span> <span class="s">fluentd</span>
<span class="na">namespace</span><span class="pi">:</span> <span class="s">kube-system</span>
<span class="na">rules</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">apiGroups</span><span class="pi">:</span>
<span class="pi">-</span> <span class="s2">"</span><span class="s">"</span>
<span class="na">resources</span><span class="pi">:</span>
<span class="pi">-</span> <span class="s">pods</span>
<span class="pi">-</span> <span class="s">namespaces</span>
<span class="na">verbs</span><span class="pi">:</span>
<span class="pi">-</span> <span class="s">get</span>
<span class="pi">-</span> <span class="s">list</span>
<span class="pi">-</span> <span class="s">watch</span>

<span class="nn">---</span>

<span class="na">kind</span><span class="pi">:</span> <span class="s">ClusterRoleBinding</span>
<span class="na">apiVersion</span><span class="pi">:</span> <span class="s">rbac.authorization.k8s.io/v1beta1</span>
<span class="na">metadata</span><span class="pi">:</span>
<span class="na">name</span><span class="pi">:</span> <span class="s">fluentd</span>
<span class="na">roleRef</span><span class="pi">:</span>
<span class="na">kind</span><span class="pi">:</span> <span class="s">ClusterRole</span>
<span class="na">name</span><span class="pi">:</span> <span class="s">fluentd</span>
<span class="na">apiGroup</span><span class="pi">:</span> <span class="s">rbac.authorization.k8s.io</span>
<span class="na">subjects</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">kind</span><span class="pi">:</span> <span class="s">ServiceAccount</span>
<span class="na">name</span><span class="pi">:</span> <span class="s">fluentd</span>
<span class="na">namespace</span><span class="pi">:</span> <span class="s">kube-system</span>
</code></pre>
<p>In short, this will create a ClusterRole which grants get, list, and watch permissions on pods and namespace objects. The ClusterRoleBinding then binds the ClusterRole to the ServiceAccount within the <code class="highlighter-rouge">kube-system</code> namespace. Refer to the <a href="https://kubernetes.io/docs/reference/access-authn-authz/rbac/">Using RBAC Authorization</a> guide to learn more about RBAC and ClusterRoles.</p>
<p>Create:</p>
<pre class="highlight"><code><span class="nv">$ </span>kubectl create <span class="nt">-f</span> kubernetes/fluentd-rbac.yaml
</code></pre>
<p>Now, we can create the DaemonSet.</p>
<p><em>kubernetes/fluentd-daemonset.yaml</em>:</p>
<pre class="highlight"><code><span class="na">apiVersion</span><span class="pi">:</span> <span class="s">extensions/v1beta1</span>
<span class="na">kind</span><span class="pi">:</span> <span class="s">DaemonSet</span>
<span class="na">metadata</span><span class="pi">:</span>
<span class="na">name</span><span class="pi">:</span> <span class="s">fluentd</span>
<span class="na">namespace</span><span class="pi">:</span> <span class="s">kube-system</span>
<span class="na">labels</span><span class="pi">:</span>
<span class="na">k8s-app</span><span class="pi">:</span> <span class="s">fluentd-logging</span>
<span class="na">version</span><span class="pi">:</span> <span class="s">v1</span>
<span class="s">kubernetes.io/cluster-service</span><span class="pi">:</span> <span class="s2">"</span><span class="s">true"</span>
<span class="na">spec</span><span class="pi">:</span>
<span class="na">template</span><span class="pi">:</span>
<span class="na">metadata</span><span class="pi">:</span>
<span class="na">labels</span><span class="pi">:</span>
<span class="na">k8s-app</span><span class="pi">:</span> <span class="s">fluentd-logging</span>
<span class="na">version</span><span class="pi">:</span> <span class="s">v1</span>
<span class="s">kubernetes.io/cluster-service</span><span class="pi">:</span> <span class="s2">"</span><span class="s">true"</span>
<span class="na">spec</span><span class="pi">:</span>
<span class="na">serviceAccount</span><span class="pi">:</span> <span class="s">fluentd</span>
<span class="na">serviceAccountName</span><span class="pi">:</span> <span class="s">fluentd</span>
<span class="na">tolerations</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">key</span><span class="pi">:</span> <span class="s">node-role.kubernetes.io/master</span>
<span class="na">effect</span><span class="pi">:</span> <span class="s">NoSchedule</span>
<span class="na">containers</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">fluentd</span>
<span class="na">image</span><span class="pi">:</span> <span class="s">fluent/fluentd-kubernetes-daemonset:v1.3-debian-elasticsearch</span>
<span class="na">env</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span>  <span class="s">FLUENT_ELASTICSEARCH_HOST</span>
<span class="na">value</span><span class="pi">:</span> <span class="s2">"</span><span class="s">elasticsearch.logging"</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span>  <span class="s">FLUENT_ELASTICSEARCH_PORT</span>
<span class="na">value</span><span class="pi">:</span> <span class="s2">"</span><span class="s">9200"</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">FLUENT_ELASTICSEARCH_SCHEME</span>
<span class="na">value</span><span class="pi">:</span> <span class="s2">"</span><span class="s">http"</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">FLUENT_UID</span>
<span class="na">value</span><span class="pi">:</span> <span class="s2">"</span><span class="s">0"</span>
<span class="na">resources</span><span class="pi">:</span>
<span class="na">limits</span><span class="pi">:</span>
<span class="na">memory</span><span class="pi">:</span> <span class="s">200Mi</span>
<span class="na">requests</span><span class="pi">:</span>
<span class="na">cpu</span><span class="pi">:</span> <span class="s">100m</span>
<span class="na">memory</span><span class="pi">:</span> <span class="s">200Mi</span>
<span class="na">volumeMounts</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">varlog</span>
<span class="na">mountPath</span><span class="pi">:</span> <span class="s">/var/log</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">varlibdockercontainers</span>
<span class="na">mountPath</span><span class="pi">:</span> <span class="s">/var/lib/docker/containers</span>
<span class="na">readOnly</span><span class="pi">:</span> <span class="no">true</span>
<span class="na">terminationGracePeriodSeconds</span><span class="pi">:</span> <span class="s">30</span>
<span class="na">volumes</span><span class="pi">:</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">varlog</span>
<span class="na">hostPath</span><span class="pi">:</span>
<span class="na">path</span><span class="pi">:</span> <span class="s">/var/log</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">varlibdockercontainers</span>
<span class="na">hostPath</span><span class="pi">:</span>
<span class="na">path</span><span class="pi">:</span> <span class="s">/var/lib/docker/containers</span>
</code></pre>
<p>Be sure to review <a href="https://docs.fluentd.org/v/0.12/articles/kubernetes-fluentd">Kubernetes Logging with Fluentd</a> along with the <a href="https://github.com/fluent/fluentd-kubernetes-daemonset/blob/master/fluentd-daemonset-elasticsearch-rbac.yaml">sample Daemonset</a>. Make sure <code class="highlighter-rouge">FLUENT_ELASTICSEARCH_HOST</code> aligns with the <code class="highlighter-rouge">SERVICE_NAME.NAMESPACE</code> of Elasticsearch within your cluster.</p>
<p>Deploy:</p>
<pre class="highlight"><code><span class="nv">$ </span>kubectl create <span class="nt">-f</span> kubernetes/fluentd-daemonset.yaml
</code></pre>
<p>If you’re running Kubernetes as a single node with Minikube, this will create a single Fluentd pod in the <code class="highlighter-rouge">kube-system</code>  namespace.</p>
<pre class="highlight"><code><span class="nv">$ </span>kubectl get pods <span class="nt">-n</span> kube-system

coredns-576cbf47c7-mhxbp                1/1     Running   0          120m
coredns-576cbf47c7-vx7m7                1/1     Running   0          120m
etcd-minikube                           1/1     Running   0          119m
fluentd-kxc46                           1/1     Running   0          89s
kube-addon-manager-minikube             1/1     Running   0          119m
kube-apiserver-minikube                 1/1     Running   0          119m
kube-controller-manager-minikube        1/1     Running   0          119m
kube-proxy-m4vzt                        1/1     Running   0          120m
kube-scheduler-minikube                 1/1     Running   0          119m
kubernetes-dashboard-5bff5f8fb8-d64qs   1/1     Running   0          120m
storage-provisioner                     1/1     Running   0          120m
</code></pre>
<p>Take note of the logs:</p>
<pre class="highlight"><code><span class="nv">$ </span>kubectl logs fluentd-kxc46 <span class="nt">-n</span> kube-system
</code></pre>
<p>You should see that Fluentd connect to Elasticsearch within the logs:</p>
<pre class="highlight"><code>Connection opened to Elasticsearch cluster <span class="o">=&gt;</span>
<span class="o">{</span>:host<span class="o">=&gt;</span><span class="s2">"elasticsearch.logging"</span>, :port<span class="o">=&gt;</span>9200, :scheme<span class="o">=&gt;</span><span class="s2">"http"</span><span class="o">}</span>
</code></pre>
<p>To see the logs collected by Fluentd in Kibana, click “Management” and then select “Index Patterns” under “Kibana”.</p>

<p>Click the “Create index pattern” button. Select the new Logstash index that is generated by the Fluentd DaemonSet. Click “Next step”.</p>

<p>Set the “Time Filter field name” to “@timestamp”. Then, click “Create index pattern”.</p>

<p>Click “Discover” to view your application logs.</p>
<h2 id="sanity-check">Sanity Check</h2>
<p>Let’s spin up a quick Node.js app to test.</p>
<p>Point your local Docker client at the Minikube Docker daemon, and then build the image:</p>
<pre class="highlight"><code><span class="nv">$ </span><span class="nb">eval</span> <span class="k">$(</span>minikube docker-env<span class="k">)</span>
<span class="nv">$ </span>docker build <span class="nt">-t</span> fluentd-node-sample:latest <span class="nt">-f</span> sample-app/Dockerfile sample-app
</code></pre>
<p>Create the deployment:</p>
<pre class="highlight"><code><span class="nv">$ </span>kubectl create <span class="nt">-f</span> kubernetes/node-deployment.yaml
</code></pre>
<p>Take a quick look at the app in <em>sample-app/index.js</em>:</p>
<pre class="highlight"><code><span class="kd">const</span> <span class="nx">SimpleNodeLogger</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="s1">'simple-node-logger'</span><span class="p">);</span>
<span class="kd">const</span> <span class="nx">opts</span> <span class="o">=</span> <span class="p">{</span>
<span class="na">timestampFormat</span><span class="p">:</span><span class="s1">'YYYY-MM-DD HH:mm:ss.SSS'</span>
<span class="p">};</span>
<span class="kd">const</span> <span class="nx">log</span> <span class="o">=</span> <span class="nx">SimpleNodeLogger</span><span class="p">.</span><span class="nx">createSimpleLogger</span><span class="p">(</span><span class="nx">opts</span><span class="p">);</span>

<span class="p">(</span><span class="kd">function</span> <span class="nx">repeatMe</span><span class="p">()</span> <span class="p">{</span>
<span class="nx">setTimeout</span><span class="p">(()</span> <span class="o">=&gt;</span> <span class="p">{</span>
<span class="nx">log</span><span class="p">.</span><span class="nx">info</span><span class="p">(</span><span class="s1">'it works'</span><span class="p">);</span>
<span class="nx">repeatMe</span><span class="p">();</span>
<span class="p">},</span> <span class="mi">1000</span><span class="p">)</span>
<span class="p">})();</span>
</code></pre>
<p>So, it just logs <code class="highlighter-rouge">'it works'</code> to stdout every second.</p>
<p>Back in “Discover” on the Kibana dashboard, add the following filter:</p>
<ol>
<li>Field: <code class="highlighter-rouge">kubernetes.pod_name</code></li>
<li>Operator: <code class="highlighter-rouge">is</code></li>
<li>Value: <code class="highlighter-rouge">node</code></li>
</ol>
<li>Field: <code class="highlighter-rouge">kubernetes.pod_name</code></li>
<li>Operator: <code class="highlighter-rouge">is</code></li>
<li>Value: <code class="highlighter-rouge">node</code></li>

<p>Now, you should be able to see the <code class="highlighter-rouge">it works</code> log in the stream.</p>

