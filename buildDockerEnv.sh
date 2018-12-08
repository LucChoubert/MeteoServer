#!/bin/sh

docker build -t meteoserver -f Dockerfile.meteoserver .
docker build -t meteodaemon -f Dockerfile.meteodaemon .
