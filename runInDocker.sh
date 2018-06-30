docker stop api_server
docker rm api_server

docker stop redis_server
docker rm redis_server

docker build -t meteoserver .

docker network create --driver bridge application-net

docker pull redis
docker run --name redis_server --network application-net -d -p 6379:6379 redis

docker run --name api_server --network application-net -d -p 5000:5000 meteoserver

# connect for debugging
# docker exec -i -t 8dfef789c123 /bin/bash


