#!/bin/bash

# Stop and remove existing containers
echo "Stopping and removing existing containers..."
docker-compose down

# Remove all images related to the project
echo "Removing existing images..."
docker-compose rm -f

# Build the images
echo "Building new images..."
docker-compose build --no-cache

# Start the services
echo "Starting services..."
docker-compose up -d

# Display the logs
echo "Displaying logs..."
docker-compose logs -f