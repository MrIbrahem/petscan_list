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
VENV_PATH="$HOME/www/python/venv"

source "$VENV_PATH/bin/activate" || exit 1

pip install --upgrade pip

pip install -r $HOME/www/python/src/requirements.txt

exit

webservice python3.9 start

cp $HOME/www/python/src/update.sh $HOME/update.sh
chmod +x $HOME/update.sh
