---
layout: post
title: Jekyll-Site-Offline-Editing
date: 2020-12-08 16:20:23 +0900
category: Docker
tag: Docker
---


# Jekyll-Site-Offline-Editing
Offline Editing Jekyll Site Instructions. You may use it for Github website.

* Checkout codebase [here](https://github.com/ShihabYasin/Jekyll-Site-Offline-Editing) 




## 1. Check Makefile for run instructions as below:

<pre class="code" style="background-color: rgb(217,238,239,255);">
.PHONY: clean build run stop inspect

IMAGE_NAME = jekylmygi
CONTAINER_NAME = container_jekylmygithub

build:   # 1. BUILD DOCKER IMAGE
	docker build -t $(IMAGE_NAME) .

run:     # 2. RUN DOCKER CONTAINER
	#docker run -d --rm -p 4000:4000 --name $(CONTAINER_NAME) $(IMAGE_NAME)
	docker run --rm -p 4000:4000 -v /home/tigerit/MyGithub/old_shihabyasin.github.io/_posts:/home/user/my-awesome-site/_posts --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:    # 3. STOP DOCKER CONTAINER
	docker stop $(CONTAINER_NAME)

list:    # 4. GET LIST OF DOCKER IMAGES & CONTAINERS
	# list all docker image and container
	docker image ls && docker container ls
</pre>


## 2. This is a test site, live edit your post (in _posts folder) and check your site offline at ```http://127.0.0.1:4000/``` in browser after running your docker container.

## Extra: 
### Dockerfile Used:

<pre class="code" style="background-color: rgb(217,238,239,255);">
FROM ubuntu:20.04
RUN apt update
RUN apt install -y ruby-full
RUN apt-get install -y build-essential zlib1g-dev
RUN gem install jekyll bundler

ENV HOME=/home/user
ENV GEM_HOME=/home/user/gems
ENV PATH=/home/user/gems/bin:$PATH
EXPOSE 4000
RUN ruby --version
RUN gem --version
RUN gem install bundler:1.17.2 # change if need 
WORKDIR /home/user/
RUN mkdir -p /home/user/my-awesome-site
RUN jekyll new my-awesome-site
RUN ls /home/user
WORKDIR /home/user/my-awesome-site
COPY . /home/user/my-awesome-site/

CMD [ "bundle", "exec", "jekyll", "serve", "--force_polling", "-H", "0.0.0.0", "-P", "4000" ]
</pre>


