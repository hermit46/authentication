#!/bin/sh

# To build the docker image & run
docker build -t authentication . && docker run -p "8000:8000" authentication 

docker images