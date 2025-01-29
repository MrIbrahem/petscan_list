#!/bin/bash
cd $HOME
VENV_PATH="$HOME/www/python/venv"
source "$VENV_PATH/bin/activate" || exit 1

python3 $HOME/www/python/src/bot.py

