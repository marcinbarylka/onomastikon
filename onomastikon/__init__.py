"""A main module for generating random names."""

from onomastikon.config import copy_files, setup_config_files
from onomastikon.ono import Onomastikon

setup_config_files()
copy_files()

__all__ = ["Onomastikon"]
