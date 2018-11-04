#!/usr/bin/env bash

source venv/bin/activate
export FLASK_APP=MeteoServer.py
export FLASK_DEBUG=1
export REDIS_HOST='pi3.local'

#Start the Daemon retrieving and historizing the meteo data
pkill -f -TERM *Daemon*
python3 MeteoRetrieverDaemon.py

#Start the server to distribute the data in the LAN
killall flask
flask run &
