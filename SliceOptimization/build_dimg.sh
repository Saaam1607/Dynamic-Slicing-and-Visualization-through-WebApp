#!/bin/bash

echo "Building all the docker images for servers and clients"
docker build -t nginx-server -f Dockerfile.webserver.server .
docker build -t ubuntu-client -f Dockerfile.ubuntu.client .