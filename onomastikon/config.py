"""A first run config"""

import os
import shutil

import toml

import appdirs


def setup_config_files():
    """Create the configuration files."""
    _meta = get_project_meta()
    _local = appdirs.user_data_dir(_meta["name"], _meta["authors"][0])
    _config = appdirs.user_config_dir(_meta["name"], _meta["authors"][0])

    # check if the directories exist, if not create them
    for _dir in [_local, _config]:
        if not os.path.exists(_dir):
            os.makedirs(_dir, exist_ok=True)

    # check if the config file exists, if not create it
    _config_file = os.path.join(_config, "config.toml")
    if not os.path.exists(_config_file):
        with open(_config_file, "w") as file:
            file.write(
                f"# {_meta['name']} Configuration File\n"
                f"# Version: {_meta['version']}\n"
                f"# Authors: {_meta['authors']}\n"
            )
            file.write("\n\n[onomastikon]\n")
            file.write(f"version = \"{_meta['version']}\"\n")
            file.write("copied = false\n")


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


def copy_files():
    """Copy the data files to the user's data directory."""
    _meta = get_project_meta()
    _local = appdirs.user_data_dir(_meta["name"], _meta["authors"][0])
    _config = appdirs.user_config_dir(_meta["name"], _meta["authors"][0])

    _data = os.path.join(_local, "data")
    if not os.path.exists(_data):
        os.makedirs(_data, exist_ok=True)

    _data_files = ["data/first_names.csv", "data/last_names.csv"]

    # check if the version in the config file matches the current version
    _version_changed = False
    _config_file = os.path.join(_config, "config.toml")
    with open(_config_file, "r") as file:
        _config_data = toml.load(file)
        if _meta["version"] == _config_data["onomastikon"]["version"]:
            _version_changed = True

    # check if the data files have been copied
    if _version_changed or not _config_data["onomastikon"]["copied"]:
        for _file in _data_files:
            _source = os.path.join(os.getcwd(), _file)
            _destination = os.path.join(_data, os.path.basename(_file))
            shutil.copyfile(_source, _destination)

        # update the config file
        _config_data["onomastikon"]["copied"] = True
        with open(_config_file, "w") as file:
            toml.dump(_config_data, file)
