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