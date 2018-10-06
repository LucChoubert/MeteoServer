#!/bin/sh

#Create the virtual environment
python3 -m venv project-env

#Switch to the environment
source project-env/bin/activate

#Install the dependencies
pip3 install -r requirements.txt

echo --------------------------------------------------------
echo You have installed successfully the localdev environment
echo You can run the server with runLocalDev.sh
echo --------------------------------------------------------

