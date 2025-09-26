#!/bin/bash
cd $HOME

source "$HOME/www/python/venv/bin/activate" || exit 1

python3 $HOME/www/python/src/bot.py

