#!/bin/bash

# bootstrap script for the project needs only to be called once
# setups the dependencies / packages and  python virtual env for local development

# install necessary packages
sudo apt update
sudo apt install -y python3-pip
sudo apt install -y python3-virtualenv

# setup the virtual environemnt
# TODO fix the pathing, below might fail if bootstrap script is being called from any other location
if [ -d ".venv" ]; then
  echo "Virtualenv already exists"
else
  virtualenv .venv # TODO standardize the python version
fi


