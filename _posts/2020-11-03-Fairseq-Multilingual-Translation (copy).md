---
layout: post 
title: Test Automation of Python project in Dockerized Jenkins
date: 2020-12-05 16:20:23 +0900 
category: DevOps
tag: deeplearning
---
# Test Automation of Python project in Dockerized Jenkins

Python project's Test Automation in Dockerized Jenkins.
### Ideas:


_* All files hosted [here](https://github.com/ShihabYasin/Jenkins-Pytest-Docker)_



1.Create a Dockerized Jenkins container.

* ```JenkinsDockerfile```: Lightweight Dockerfile to Dockerize Jenkins 

```dockerfile
FROM jenkins/jenkins:lts
USER root
RUN apt-get update -qq \
    && apt-get install -qqy apt-transport-https ca-certificates curl gnupg2 software-properties-common
	
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
   
RUN apt-get update  -qq
RUN apt-get install docker-ce -y
```

2.Write sample automation tests for sample project.
* ```src/compute.py```: Contains sample compute project.

```python
from src.lib import validateInputs

def add(a, b):
    validateInputs (a, b)
    return a + b

def subtract(a, b):
    validateInputs (a, b)
    return a - b

def multiply(a, b):
    validateInputs (a, b)
    return a * b

def divide(a, b):
    validateInputs (a, b)
    return a / b
```

* ```tests/test_compute.py```: Contains sample automation tests.Ref: [pytest](https://docs.pytest.org/)

```python
from src.compute import add, divide, subtract, multiply
import pytest

def test_add():
    result = add (30, 40)
    assert result == 70


def test_add_string():
    with pytest.raises (TypeError):
        add ("MyString", 98)


def test_divide():
    result = divide (33, 5)
    assert result == 6.6


def test_divide_by_zero():
    with pytest.raises (ZeroDivisionError) as e:
        divide (9, 0)


def test_divide_string():
    with pytest.raises (TypeError):
        divide ("MyString", 2)


def test_multiply():
    result = multiply (8, 4)
    assert result == 32


def test_multiply_string():
    with pytest.raises (TypeError):
        multiply ("MyString", 4)


def test_subtract_positive():
    result = subtract (7, 6)
    assert result == 1


def test_subtract_negative():
    result = subtract (4, 9)
    assert result == -5


def test_subtract_string():
    with pytest.raises (TypeError):
        subtract ("MyString", 6)

```

* ```pytest.ini```: includes a single line “junit_family=xunit1” to ignore warnings, pytest configuration file.

```ini
# Configuration of pytest
[pytest]
junit_family=xunit1
```

* ```Push project to Github.```


3.Create a Dockerized test project image from ```Dockerfile```.

```dockerfile
FROM python:3.6-slim
MAINTAINER shihabyasin@gmail.com
COPY . /python-project-compute
WORKDIR /python-project-compute
RUN pip install --no-cache-dir -r requirements.txt
RUN ["pytest", "-v", "--junitxml=reports/result.xml"]
CMD tail -f /dev/null
```

4.Run test project image from Jenkins container.

* On **Add build** step choose **Execute shell** in Jenkins & paste:

```shell
IMAGE_NAME="python-project-compute-image"
CONTAINER_NAME="python-project-compute-image-container"
docker build -t $IMAGE_NAME .
docker run -d --name $CONTAINER_NAME $IMAGE_NAME
rm -rf reports; mkdir reports
docker cp $CONTAINER_NAME:/python-project-compute/reports/result.xml reports/
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME
docker rmi $IMAGE_NAME
```

* **JUnit plugin** is required on Jenkins

5.Inspect test result:

* Test result will reside in ```reports/result.xml``` file on the test container, Jenkins container will collect this test result to publish.

### Setup:

1.Build Jenkins docker image.

```shell
sudo su
docker build -t jenkins-docker-image -f JenkinsDockerfile .
```

2.Run Jenkins docker image

```shell
docker run -d -p 8080:8080 --name jenkins-docker-container -v /var/run/docker.sock:/var/run/docker.sock jenkins-docker-image
```

* Use ```docker rm <container-id>``` to remove any existing ```similar named``` container.

3.Visit ```http://localhost:8080/```, get Jenkins initial setup password, submit Jenkins initial setup password.

```shell
docker exec -it jenkins-docker-container cat /var/jenkins_home/secrets/initialAdminPassword
```

* Check ```jenkins-docker-container``` is running:```docker container ls```


4.Install suggested plugins, provide username, password.


### How to Use:

1.Run stopped container(```jenkins-docker-container```) if not running already.Check all stopped container:```docker ps -a```

```shell
docker start <jenkins-docker-container-id>
```

2.Login here ```http://localhost:8080/``` & use Jenkins

3.Create a Freestyle project Job in Jenkins, set Git repo link, on ```Post build action``` set **JUnit test result report** and path(```reports/result.xml```), enter credentials selecting **Add->Jenkins**, provide username, password of your Git.

4.Click **Build Now** in project menu, see **Console Output**.

5.(Optional) Edit on src to add new functions & tests, push on Github, run build in Jenkins, get build output.