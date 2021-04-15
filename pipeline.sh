#!/bin/bash

##
# This pipeline will setup run all tests and download an example log file from NASA.
# After setup it will build and run the log parser using docker-compose.
#
# Hint:
# The pipeline assumes that python3 and pip3 are installed.
##

printf "Setting up dependencies...\n"
pip3 install -r requirements.txt

printf "Setup complete! Running tests...\n"
result=$(python3 -m unittest discover app/ 2>&1 | tail -n 3)
printf "Test Result:%s\n$result\n"
if [[ ! $result =~ "OK" ]]; then
   printf "Tests failed, aborting...\n"
   exit 1
fi
printf "\nAll Tests run successfully! "

if [ ! -f logs/NASA_access_log_Jul95 ]; then
    printf "Downloading log file NASA_access_log_Jul95...\n"
    wget -P logs/ ftp://ita.ee.lbl.gov/traces/NASA_access_log_Jul95.gz
    gunzip logs/NASA_access_log_Jul95.gz
    printf "Download complete! "
fi

printf "Running app with docker-compose...\n"
docker-compose up --build
