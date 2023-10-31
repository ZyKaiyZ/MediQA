#!/bin/bash
docker system prune -a

docker-compose up --build -d