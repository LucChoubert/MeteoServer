#!/bin/sh

docker stop api-server
docker rm api-server

docker stop redis-server
docker rm redis-server

docker stop redis-commander
docker rm redis-commander

docker build -t meteoserver .

docker network create --driver bridge application-net

docker pull redis
docker run --name redis-server --network application-net -d -p 6379:6379 redis

docker run --name api-server --network application-net -d -p 5000:5000 meteoserver

docker run --name redis-commander --network application-net -d -p 8081:8081 redis-commander:arm

# connect for debugging
# docker exec -i -t 8dfef789c123 /bin/bash


