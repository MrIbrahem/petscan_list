import os
import configparser

# Use environment variable for project path with a fallback
project = os.getenv('PETSCAN_PROJECT_PATH', "/data/project/petscan-list")

# Check if the directory exists, otherwise use the current directory
if not os.path.isdir(project):
    project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()

# Path to the configuration file
config_path = os.path.join(project, 'confs', 'user.ini')

# Read configuration file with error handling
try:
    config.read(config_path)
    DEFAULT = config['DEFAULT']
    
    username = DEFAULT.get('botusername', '')
    password = DEFAULT.get('botpassword', '')
except (configparser.Error, KeyError) as e:
    # Handle error (e.g., log it, raise an exception, or use default values)
    print(f"Error reading config file: {e}")
    username = os.getenv('botusername','')
    password = os.getenv('botpassword','')
