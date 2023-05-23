from peewee import DatabaseProxy

from api.models import db, Website

database_proxy = DatabaseProxy()
database_proxy.initialize(db)

with database_proxy:
    database_proxy.create_tables([Website])
    Website.truncate_table(restart_identity=True, cascade=True)