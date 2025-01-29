import os
import configparser

project = "/data/project/petscan-list"
# ---
if not os.path.isdir(project):
    project = "I:/core/bots/core1"
# ---
config = configparser.ConfigParser()
config.read(f"{project}/confs/user.ini")

DEFAULT = config["DEFAULT"]

username = config["DEFAULT"].get("botusername", "")
password = config["DEFAULT"].get("botpassword", "")
