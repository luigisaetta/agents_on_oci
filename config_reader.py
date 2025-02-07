"""
File name: config_reader.py
Author: Luigi Saetta
Date last modified: 2024-11-23
Python Version: 3.11

Description:
    This file provide a class to handle the configuration
    read from a toml file

Inspired by:


Usage:
    Import this module into other scripts to use its functions.
    Example:


License:
    This code is released under the MIT License.

Notes:
    This is a part of a set of demos showing how to build a SQL Agent
    for Text2SQL taks

Warnings:
    This module is in development, may change in future versions.
"""

import toml
from utils import get_console_logger


class ConfigReader:
    """
    Read the configuration from a toml file
    """

    def __init__(self, file_path):
        """
        Initializes the TOML reader and loads the file into memory.
        :param file_path: Path to the TOML file
        """
        self.file_path = file_path
        self.data = None
        self.logger = get_console_logger()
        self.load_file()

    def load_file(self):
        """
        Reads the TOML file and stores it in a dictionary.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.data = toml.load(f)
        except FileNotFoundError:
            self.logger.error("Error: The file %s does not exist.", self.file_path)
            self.data = {}
        except Exception as e:
            self.logger.error("Error while reading the TOML file: %s", e)
            self.data = {}

    def find_key(self, key_name):
        """
        Finds the value of a key in the TOML dictionary.
        :param key_name: Name of the key to search for
        :return: The value associated with the key if found, otherwise None
        """

        def recursive_search(dictionary, target_key):
            for k, v in dictionary.items():
                if k == target_key:
                    return v
                if isinstance(v, dict):
                    result = recursive_search(v, target_key)
                    if result is not None:
                        return result
            return None

        # Search for the key in the already loaded file
        if self.data is None:
            self.logger.error("Error: No TOML file loaded.")
            return None
        return recursive_search(self.data, key_name)
