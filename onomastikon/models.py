"""Models for Onomastikon"""
from pony import orm

from onomastikon import config

db = config.create_db_connection()


class Country(db.Entity):
    country = orm.Required(str)
    country_iso = orm.Required(str)