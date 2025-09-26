#!/bin/bash
set -e  # Exit on error

# Cleanup existing directories
rm -rf www/python

webservice python3.11 shell
mkdir www
mkdir www/python
python3 -m venv "$HOME/www/python/venv"
source "$HOME/www/python/venv/bin/activate"
pip install --upgrade pip==24.0 wheel==0.42.0

git clone https://github.com/MrIbrahem/petscan_list.git "$HOME/www/python/src"

pip install -r "$HOME/www/python/src/requirements.txt"

webservice python3.11 start
