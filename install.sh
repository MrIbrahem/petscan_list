#!/bin/bash
set -e  # Exit on error

# Define variables
VENV_DIR="$HOME/www/python/venv"
SRC_DIR="$HOME/www/python/src"

# Cleanup existing directories
rm -rf www/python

toolforge webservice python3.11 shell
mkdir www
mkdir www/python
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip==24.0 wheel==0.42.0

git clone https://github.com/MrIbrahem/petscan_list.git "$SRC_DIR"

pip install -r "$SRC_DIR/requirements.txt"













