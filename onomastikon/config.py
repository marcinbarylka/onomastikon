"""A first run config"""

import logging
import os
from dataclasses import dataclass

import appdirs
import toml

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_db_connection(): ...


@dataclass
class Config:
    name: str
    version: str
    copied: bool
    separate_names: bool
    database: str

    def __post_init__(self):
        self._meta = Config.get_project_meta()
        self._local = appdirs.user_data_dir(
            self._meta["name"], self._meta["authors"][0]
        )
        self._config = appdirs.user_config_dir(
            self._meta["name"], self._meta["authors"][0]
        )
        self._config_file = os.path.join(self._config, "config.toml")

    @staticmethod
    def setup_config_files():
        """Create the configuration files."""
        _meta = Config.get_project_meta()
        _local = appdirs.user_data_dir(_meta["name"], _meta["authors"][0])
        _config = appdirs.user_config_dir(_meta["name"], _meta["authors"][0])

        version = _meta["version"]

        # check if the directories exist, if not create them
        for _dir in [_local, _config]:
            if not os.path.exists(_dir):
                os.makedirs(_dir, exist_ok=True)

        # check if the config file exists, if not create it
        _config_file = os.path.join(_config, "config.toml")
        if os.path.exists(_config_file):
            _version = toml.load(_config_file)["onomastikon"]["version"]
            if _version != version:
                logging.info("New version detected, updating configuration")
                Config.create_config_file(_config_file, _meta)
        else:
            Config.create_config_file(_config_file, _meta)

    @staticmethod
    def create_config_file(_config_file, _meta):
        config_data = {
            "onomastikon": {
                "version": _meta['version'],
                "copied": False,
                "separate_names": True,
                "database": "onomastikon.db"
            }
        }

        with open(_config_file, "w") as file:
            file.write(
                f"# {_meta['name']} Configuration File\n"
                f"# Version: {_meta['version']}\n"
                f"# Authors: {_meta['authors']}\n\n"
            )
            toml.dump(config_data, file)
        logging.info(f"Configuration file created at {_config_file}")

    @staticmethod
    def get_project_meta() -> dict:
        """Return the project metadata."""
        with open("pyproject.toml", "r") as file:
            _meta = toml.load(file)
        return {
            "name": _meta["tool"]["poetry"]["name"],
            "version": _meta["tool"]["poetry"]["version"],
            "description": _meta["tool"]["poetry"]["description"],
            "authors": _meta["tool"]["poetry"]["authors"],
        }

    @staticmethod
    def force_update_config():
        """Force update the configuration file."""
        _meta = Config.get_project_meta()
        _config = appdirs.user_config_dir(
            _meta["name"], _meta["authors"][0]
        )
        _config_file = os.path.join(_config, "config.toml")
        Config.create_config_file(_config_file, _meta)

    @staticmethod
    def instantiate():
        """Instantiate the configuration object."""
        c = Config(
            name="onomastikon", version="", copied=False, separate_names=True, database=""
        )
        c.read_config()
        return c

    def read_config(self):
        """Read the configuration file."""
        with open(self._config_file, "r") as file:
            config = toml.load(file)
        for key, value in config["onomastikon"].items():
            setattr(self, key, value)