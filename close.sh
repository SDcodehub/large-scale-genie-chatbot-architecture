#!/bin/bash

# Stop and remove existing containers
echo "Stopping and removing existing containers..."
docker-compose down

# Remove all images related to the project
echo "Removing existing images..."
docker-compose rm -fclear
