#!/bin/bash

SCRIPT_DIR="$(realpath "$(dirname "$0")")"

# Function to start the FastAPI server
runserver() {
    source
    uvicorn appserver.main:app --reload
}

# Function to run tests with pytest
test() {
    pytest
}

# Function to build and run the Docker container
docker() {
    # Build the Docker image with the 'latest' tag
    docker build -t claimrx:latest .
    docker run -p 8000:8000 claimrx:latest
}

dockercompose() {
  docker-compose up -d
}

# Check the argument and call the corresponding function
case "$1" in
    runserver)
        runserver
        ;;
    test)
        test
        ;;
    docker)
        docker
        ;;
    dockercompose)
        dockercompose
        ;;
    *)
        echo "Usage: $0 {runserver|test|docker|dockercompose}"
        exit 1
        ;;
esac