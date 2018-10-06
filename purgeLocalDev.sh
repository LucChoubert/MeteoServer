#!/bin/sh

#Delete the virtual environment
deactivate
rm -rf project-env
rm -rf MeteoFranceInterface/__pycache__
rm -rf __pycache__

echo --------------------------------------------------------
echo You have purged the local environment
echo You can reinstall with installLocalDev.sh
echo --------------------------------------------------------
