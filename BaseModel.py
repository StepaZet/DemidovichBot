from peewee import *  # noqa


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase('sqlite.db')
