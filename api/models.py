from peewee import DatabaseProxy, Model, CharField, IntegerField, SqliteDatabase
from pydantic import BaseModel as PydanticBaseModel, HttpUrl

database_proxy = DatabaseProxy()
database_file = 'api/shortener_url.db'

db = SqliteDatabase(database_file)
database_proxy.initialize(db)


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Website(BaseModel):
    url = CharField()
    short_url = CharField()
    title = CharField()
    views = IntegerField()

    def to_pydantic(self):
        return WebsitePydantic(id=self.id, url=self.url, short_url=self.short_url, title=self.title, views=self.views)


class WebsitePydantic(PydanticBaseModel):
    id: int
    url: HttpUrl
    short_url: str
    title: str
    views: int

