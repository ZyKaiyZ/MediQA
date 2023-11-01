#!/bin/bash
docker stop $(docker ps -aq)

docker rm $(docker ps -aq)

docker rmi -f $(docker images -aq)

docker-compose up --build -d