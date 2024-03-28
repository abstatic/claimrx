#!/bin/bash
set -euox

SCRIPT_DIR="$(realpath "$(dirname "$0")")"

# bootstrap script for the project needs only to be called once
# install necessary packages
sudo apt update
sudo apt install -y python3-pip
sudo apt install -y python3-virtualenv
sudo apt install -y sqlite3

# setup the virtual environemnt
# TODO fix the pathing, below might fail if bootstrap script is being called from any other location
if [ -d ".venv" ]; then
  echo "Virtualenv already exists"
else
  virtualenv .venv # TODO standardize the python version
fi

# activate virtual env and install pip deps
source $SCRIPT_DIR/.venv/bin/activate

pip install -r $SCRIPT_DIR/requirements.txt
