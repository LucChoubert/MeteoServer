#!/usr/bin/env bash

source venv/bin/activate
export FLASK_APP=MeteoServer.py
export FLASK_DEBUG=1

killall flask
flask run
