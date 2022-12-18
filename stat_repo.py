import datetime

from peewee import * # noqa
from BaseModel import BaseModel


class Stat(BaseModel):
    user_id = TextField(column_name='user_id')
    date = DateTimeField(column_name='date', default=datetime.datetime.now)
    mode = TextField(column_name='mode')
    query = TextField(column_name='query')
    answer = TextField(column_name='answer')

    class Meta:
        table_name = 'stats'


# class IStatMaker:
#     def isTrigger(self, str):
#         pass
#
#     def makeStat(self, str):
#         pass
#
#
#
# stats: IStatMaker = []
#
# for stat in stats:
#     if (stat.isTrigger("")):
#         stat.makeStat("")

class StatRepo:
    def __init__(self):
        self._db = Stat
        self._result = ['Статистика:']

    def get_unique_users_by_days(self, days_count: int = 1):
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

    def get_unique_users_anytime(self):
        query = (
            self._db
            .select(fn.Count(fn.Distinct(self._db.user_id)))
            .scalar()
        )
        self._result.append(f'За все время: {query} уникальных пользователей')
        return self

    def get_unique_users_today(self):
        return self.get_unique_users_by_days(1)

    def get_unique_users_last_week(self):
        return self.get_unique_users_by_days(7)

    def add_note_to_db(self, **kwargs) -> None:
        self._db.create(
            # user_id=user_id,
            # query=query,
            # answer=answer,
            # mode=mode
            **kwargs
        )

    def __str__(self):
        return '\n'.join(self._result)
