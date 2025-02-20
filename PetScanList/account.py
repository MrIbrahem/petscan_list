import os
import configparser
import logging
logger = logging.getLogger(__name__)

project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ---
config = configparser.ConfigParser()
config.read(f"{project}/confs/user.ini")

logger.info(f"Reading {project}/confs/user.ini")

DEFAULT = config["DEFAULT"]

username = config["DEFAULT"].get("botusername", "")
password = config["DEFAULT"].get("botpassword", "")
