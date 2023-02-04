#!/bin/bash

# the script builds the Docker images from a Dockerfile.
# -t <name> ---> assign the name <name> to the Docker image
# -f <path> ---> to specify the path for the Docker image

echo "Building all the docker images for servers and clients"
docker build -t nginx-server -f Dockerfile.webserver.server . 
docker build -t ubuntu-client -f Dockerfile.ubuntu.client .
