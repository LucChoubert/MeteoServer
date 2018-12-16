#!/bin/bash

while :
do
   echo "Press [CTRL+C] to stop.."
   curl http://pi3.local:5000/meteo/biot/web > /dev/null
   sleep 0
done

