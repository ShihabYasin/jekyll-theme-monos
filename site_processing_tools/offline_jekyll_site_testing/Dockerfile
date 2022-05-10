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
RUN gem install bundler:1.17.2
WORKDIR /home/user/
RUN mkdir -p /home/user/my-awesome-site
RUN jekyll new my-awesome-site
RUN ls /home/user
WORKDIR /home/user/my-awesome-site
COPY . /home/user/my-awesome-site/

CMD [ "bundle", "exec", "jekyll", "serve", "--force_polling", "-H", "0.0.0.0", "-P", "4000" ]