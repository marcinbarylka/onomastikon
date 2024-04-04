"""A main module for generating random names."""

from onomastikon.config import Config

from onomastikon.ono import Onomastikon

config = Config.instantiate()
Config.setup_config_files()

__all__ = ["Onomastikon", "Config", "config"]
