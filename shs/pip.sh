#!/bin/bash

# use bash strict mode
set -euo pipefail

# Activate the virtual environment and install dependencies
source $HOME/www/python/venv/bin/activate

pip install --upgrade pip
pip install -r "$HOME/www/python/src/requirements.txt"

# toolforge-jobs run
# toolforge-jobs run pipup --image python3.11 --command "~/shs/pip.sh" --wait
