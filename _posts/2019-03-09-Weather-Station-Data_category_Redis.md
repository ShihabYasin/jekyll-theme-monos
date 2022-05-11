---
layout: post
title: Get-Weather-Station-Data
date: 2019-03-09 16:20:23 +0900
category: Redis
tag: Redis
---

## Project Description:   

* Find code [here](https://github.com/ShihabYasin/Weather-Station-Data)

1. Getting METAR code (in JSON) from various [National Weather Service Stations](http://tgftp.nws.noaa.gov/data/observations/metar/stations/).
2. Cache result (using redis etc.) for 5 min to reduce api hit on actual server.

### Used Redis(cache.memoize), Flask, Docker, docker-compose etc.   

## Assumptions & Pre-requisites:

------------------------------------------------------------------------
1. You have docker and docker-compose installed in OS environment.
2. Remove docker-image named ```redis``` if exists. In Ubuntu its like: ```sudo docker rmi -f redis```. Remove any existing '**redis**' docker image.
3. Remove unused docker container. In Ubuntu its like: ```sudo docker container prune```
4. Remove docker-container named ```v1_api_container``` if exists. In Ubuntu its like: ```sudo docker rm -f v1_api_container```
5. Remove docker-container named ```redis_container``` if exists. In Ubuntu its like: ```sudo docker rm -f redis_container```
6. Kill any service running in port 6379. In Ubuntu its like: ```sudo fuser -n tcp -k 6379```
7. Kill any service running in port 8080. In Ubuntu its like: ```sudo fuser -n tcp -k 8080```
8. Remove docker-image named ```v1_api``` if exists. :  In Ubuntu its like: ```sudo docker rmi -f v1_api```

## How to run in Docker: Tested On Ubuntu(Ubuntu 18.04.2 LTS):

------------------------------------------------------------------------
* **RUN START BUILD:** As superuser
```commandline
sudo docker-compose up -d --build
```

* **START:** AS superuser
```commandline
sudo docker-compose start
```

* **STOP:** AS superuser
```commandline
sudo docker-compose stop
```

## Example Usage:

1. Params description: 
scode: Sation code name from [here](http://tgftp.nws.noaa.gov/data/observations/metar/stations/).
2. When nocache is not 0, fetch updated data from server (hit on server).


```
GET http://localhost:8080/metar/info?scode=SVJM&nocache=1
```
```json
{
    "data": [
        [
            {
                "last_observation": "2022/04/28 at 03:03 GMT",
                "station": "SVJM",
                "temperature": "25.00 C (77.00 F)",
                "wind": "The wind is blowing from 260 degrees (true) with 4 knot."
            },
            200
        ]
    ]
}
```
