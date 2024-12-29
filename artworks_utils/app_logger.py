import logging.config
import os

# Define the path to the configuration file
config_file = os.path.join(os.path.dirname(__file__), "logging.conf")

# Load the configuration
logging.config.fileConfig(config_file)

# Create a logger
logger = logging.getLogger("root")
