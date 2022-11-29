from sqlite_wrapper import SQLiteDB


def chained(fn):
    def new(*args, **kwargs):
        fn(*args, **kwargs)
        return args[0]
    return new


class Statistics:
    def __init__(self):
        self._stats = ['Статистика:']
        self.sqlite_db = SQLiteDB()

    @chained
    def get_unique_users_today(self):
        self._stats.append(f'Уникальных пользователей сегодня: {self.sqlite_db.get_unique_users_by_days()}')
        return self

    @chained
    def get_unique_users_last_week(self):
        self._stats.append(f'Уникальных пользователей за неделю: {self.sqlite_db.get_unique_users_by_days(7)}')
        return self

    @chained
    def get_unique_users_anytime(self):
        self._stats.append(f'Уникальных пользователей за все время: {self.sqlite_db.get_unique_users()}')
        return self

    def __call__(self):
        return self

    def __str__(self):
        return '\n'.join(self._stats)


