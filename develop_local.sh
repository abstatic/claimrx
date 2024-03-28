#!/bin/bash

set -euox

# script to do local development
# activates the virtualenv
# starts redis, DB
# starts the development server
# autopep8 on the code when running

SCRIPT_DIR="$(realpath "$(dirname "$0")")"

 Function to start the FastAPI server
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
    docker build -t <your_docker_image_name>:latest .

    # Run the Docker container, forwarding the desired port
    # Replace 8000:8000 with your actual port mapping if different
    docker run -p 8000:8000 <your_docker_image_name>:latest
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
    *)
        echo "Usage: $0 {runserver|test|docker}"
        exit 1
        ;;
esac