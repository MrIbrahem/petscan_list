cd $HOME

rm -rf $HOME/www/python/src

git clone https://github.com/MrIbrahem/petscan_list.git $HOME/www/python/src

source $HOME/www/python/venv/bin/activate

pip install --upgrade pip

pip install -r $HOME/www/python/src/requirements.txt

exit

webservice python3.9 start

chmod +x $HOME/www/python/src/update.sh
