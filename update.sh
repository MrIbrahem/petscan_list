#!/bin/bash
cd $HOME
backup_dir="$HOME/www/python/src_backup_$(date +%Y%m%d_%H%M%S)"

# Backup existing source if it exists
if [ -d "$HOME/www/python/src" ]; then
    mv "$HOME/www/python/src" "$backup_dir" || exit 1
fi
# Make repository URL configurable
REPO_URL=${REPO_URL:-"https://github.com/MrIbrahem/petscan_list.git"}
REPO_BRANCH=${REPO_BRANCH:-"main"}

if ! git clone -b "$REPO_BRANCH" "$REPO_URL" "$HOME/www/python/src"; then
    echo "Failed to clone repository" >&2
    if [ -d "$backup_dir" ]; then
        mv "$backup_dir" "$HOME/www/python/src"
    fi
    exit 1
fi

# ~/www/python/venv/bin/python3 -m pip install -r $HOME/www/python/src/requirements.txt

if source "$HOME/www/python/venv/bin/activate"; then
    python3 -m pip install --upgrade pip
    python3 -m pip install -r $HOME/www/python/src/requirements.txt
    # exit 1
else
    echo "Failed to activate virtual environment" >&2
fi

webservice python3.9 restart

