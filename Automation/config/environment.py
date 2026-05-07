"""
config/environment.py

Loads framework configuration from config.yaml
"""

from pathlib import Path
import yaml
import os


class ConfigNode:
    """
    Converts dictionary into dot-access object.
    """

    def __init__(self, data):

        for key, value in data.items():

            if isinstance(value, dict):

                value = ConfigNode(value)

            setattr(self, key, value)


CONFIG_PATH = (
    Path(__file__)
    .parent
    .joinpath("config.yaml")
)


with open(CONFIG_PATH, "r") as file:

    raw_config = yaml.safe_load(file)


config = ConfigNode(raw_config)

config.execution_type = os.getenv(
    "EXECUTION_TYPE",
    "local"
)

config.remote_url = os.getenv(
    "REMOTE_URL",
    "http://localhost:4444/wd/hub"
)