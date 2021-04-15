## Intro

This is a simple python based micro-service to parse server log files.

## Requirements

Python3 and pip3 are required to run the tests and the app on your machine.
Docker and docker-compose are necessary if you wish to run the app as intended.

## Pipeline

To use the application conveniently please run the provided ``pipeline.sh`` script.
This will run all tests, download NASA's log file, build the docker image and start container using docker-compose.

## Hint

The micro-service will parse the log file on startup and cache the result for future calls. 
This might take up to 30 seconds. 
Thank you for your patients.
