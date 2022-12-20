import datetime

from peewee import * # noqa
from BaseModel import BaseModel
from IStatMaker import IStatMaker


class Stat(BaseModel):
    user_id = TextField(column_name='user_id')
    date = DateTimeField(column_name='date', default=datetime.datetime.now)
    mode = TextField(column_name='mode')
    query = TextField(column_name='query')
    answer = TextField(column_name='answer')

    class Meta:
        table_name = 'stats'


def add_stat(**kwargs):
    repo = StatRepo()
    repo.add_note_to_db(**kwargs)


class StatRepo(IStatMaker):
    name = 'main'

    def __init__(self):
        super().__init__()
        self._db = Stat

    def get_unique_users_by_days(self, days_count: int = 1) -> 'StatRepo':
        now = datetime.datetime.now()
        last_date = now - datetime.timedelta(days=days_count)
        query = (
            self._db
            .select(fn.Count(fn.Distinct(self._db.user_id)))
            .where(self._db.date.day <= now.day
                   | self._db.date.day >= last_date.day)
            .scalar()
        )
        self._result.append(
            f'За {days_count} дней: {query} уникальных пользователей')
        return self

    def get_unique_users_anytime(self) -> 'StatRepo':
        query = (
            self._db
            .select(fn.Count(fn.Distinct(self._db.user_id)))
            .scalar()
        )
        self._result.append(f'За все время: {query} уникальных пользователей')
        return self

    def get_unique_users_today(self) -> 'StatRepo':
        return self.get_unique_users_by_days(1)

    def get_unique_users_last_week(self) -> 'StatRepo':
        return self.get_unique_users_by_days(7)

    def add_note_to_db(self, **kwargs) -> None:
        self._db.create(**kwargs)

    def clear_db(self) -> None:
        self._db.delete().execute()

    def build(self) -> str:
        (self.get_unique_users_today()
            .get_unique_users_by_days(7)
            .get_unique_users_anytime())
        return '\n'.join(self._result)
