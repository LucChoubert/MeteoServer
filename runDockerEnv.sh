#!/bin/sh

docker stop redis-server
docker rm redis-server

docker stop retriever-daemon
docker rm retriever-daemon

docker stop api-server
docker rm api-server

docker stop webui-server
docker rm webui-server

docker stop redis-commander
docker rm redis-commander

docker stop portainer
docker rm portainer

#docker build -t meteoserver -f Dockerfile.meteoserver .
#docker build -t meteodaemon -f Dockerfile.meteodaemon .
#docker build -t webui -f Dockerfile.webui .

docker network create --driver bridge application-net

docker pull redis


#RUN the various elements of the environment
#Redis Server
docker run --name redis-server --network application-net -d -p 6379:6379 redis

#Daemon getting the data from MeteoFrance and storing in Redis
docker run --name retriever-daemon --network application-net -d meteodaemon

#Meteo API Server
docker run --name api-server --network application-net -d  meteoserver

#NGINX server for the UI and facade to API server
docker run --name webui-server --network application-net -d -p 80:80  webui

## Tools Section

#Web Interface for Redis database view
docker run --name redis-commander --network application-net --env REDIS_HOSTS=PRD:redis-server:6379 -d -p 8081:8081 redis-commander:arm

#Web Interface for Docker GUI administration
docker run --name portainer --network application-net -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer


docker ps

# connect for debugging
# docker exec -i -t 8dfef789c123 /bin/bash

# Daemon runs like this: python3 MeteoRetrieverDaemon.py
# And stop like this: pkill -f -TERM *Daemon*

