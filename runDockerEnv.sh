#!/bin/sh

docker stop api-server
docker rm api-server

docker stop retriever-daemon
docker rm retriever-daemon

docker stop redis-server
docker rm redis-server

docker stop redis-commander
docker rm redis-commander

#docker build -t meteoserver -f Dockerfile.meteoserver .
#docker build -t meteodaemon -f Dockerfile.meteodaemon .

docker network create --driver bridge application-net

docker pull redis
docker run --name redis-server --network application-net -d -p 6379:6379 redis

docker run --name api-server --network application-net -d -p 5000:5000 meteoserver

docker run --name retriever-daemon --network application-net -d meteodaemon

docker run --name redis-commander --network application-net --env REDIS_HOSTS=PRD:redis-server:6379 -d -p 8081:8081 redis-commander:arm

docker ps

# connect for debugging
# docker exec -i -t 8dfef789c123 /bin/bash

# Daemon runs like this: python3 MeteoRetrieverDaemon.py
# And stop like this: pkill -f -TERM *Daemon*

