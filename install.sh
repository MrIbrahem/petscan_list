#!/bin/bash
toolforge webservice python3.11 shell
mkdir www
mkdir www/python
python3 -m venv $HOME/www/python/venv
source $HOME/www/python/venv/bin/activate
pip install --upgrade pip wheel

git clone https://github.com/MrIbrahem/petscan_list.git $HOME/www/python/src

pip install -r $HOME/www/python/src/requirements.txt













