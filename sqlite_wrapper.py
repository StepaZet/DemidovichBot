import sqlite3


def add_task(user_id: str, query: str, res: str, mode: str) -> None:
    sqlite_db = SQLiteWrapper('sqlite.db', 'stats')
    sqlite_db.add_note_to_db(user_id, query, res, mode)


class SQLiteWrapper:
    def __init__(self, db_name, table_name):
        self.__name = table_name
        self.__db_name = db_name
        self.__sqlite_connection = sqlite3.connect(self.__db_name)
        self.__cursor = self.__sqlite_connection.cursor()
        self.__cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self.__name} (user_id TEXT, date datetime, mode TEXT, query TEXT, answer TEXT);')

    # def __init__(self, db_name, table_name, **kwargs):
    #     self.__name = table_name
    #     self.__db_name = db_name
    #     self.__sqlite_connection = sqlite3.connect(self.__db_name)
    #     self.__cursor = self.__sqlite_connection.cursor()
    #     properties_types = ', '.join([f'{key} {value}' for key, value in kwargs.items()])
    #     self.__cursor.execute(
    #         f'CREATE TABLE IF NOT EXISTS {self.__name} ({properties_types});')

    def add_note_to_db(self, user_id: str, query: str, answer: str, mode: str) -> None:
        self.__cursor.execute(f'INSERT INTO {self.__name} VALUES (?,datetime("now"),?,?,?);',
                              (user_id, mode, query, answer))
        self.__sqlite_connection.commit()

    def get_unique_users_by_days(self, days_count: int = 1) -> int:
        self.__cursor.execute(
            f'SELECT COUNT(DISTINCT user_id) FROM {self.__name} WHERE date >= datetime("now", "-{days_count} days") '
            f'AND date <= datetime("now");')
        return self.__cursor.fetchone()[0]

    def get_unique_users(self) -> int:
        self.__cursor.execute(f'SELECT COUNT(DISTINCT user_id) FROM {self.__name};')
        return self.__cursor.fetchone()[0]

    def get_unique_users_by_mode_and_days(self, mode: str, days_count: int = 1) -> int:
        self.__cursor.execute(f'SELECT COUNT(DISTINCT user_id) FROM {self.__name} WHERE mode = "{mode}" '
                              f'AND date >= datetime("now", "-{days_count} days") AND date <= datetime("now");')
        return self.__cursor.fetchone()[0]

    def get_unique_users_by_mode(self, mode: str) -> int:
        self.__cursor.execute(f'SELECT COUNT(DISTINCT user_id) FROM {self.__name} WHERE mode = "{mode}";')
        return self.__cursor.fetchone()[0]

    def get_queries_amount_by_date(self, days_count: int = 1) -> int:
        self.__cursor.execute(f'SELECT COUNT(*) FROM {self.__name} WHERE date >= datetime("now", "-{days_count} days") '
                              f'AND date <= datetime("now");')
        return self.__cursor.fetchone()[0]

    def delete_month_old_notes(self) -> None:
        self.__cursor.execute(f'DELETE FROM {self.__name} WHERE date <= datetime("now", "-1 month");')
        self.__sqlite_connection.commit()

    def get_most_popular_day(self) -> str:
        self.__cursor.execute(f'SELECT date FROM {self.__name} GROUP BY date ORDER BY COUNT(*) DESC LIMIT 1;')
        return self.__cursor.fetchone()[0]

    def clear_db(self) -> None:
        self.__cursor.execute(f'DELETE FROM {self.__name};')
        self.__sqlite_connection.commit()

    def add_values_by_dict(self, values: dict) -> None:
        properties = ', '.join(values.keys())
        placeholders = ', '.join('?' * len(values))
        sql_query = f'INSERT INTO {self.__name} ({properties}) VALUES ({placeholders})'
        self.__cursor.execute(sql_query, list(values.values()))
        self.__sqlite_connection.commit()

    def get_unique_notes_by_stat(self, main_stat, unique_param=None, *additional_stats) -> int:
        count_filter = f'DISTINCT {unique_param}' if unique_param is not None else '*'
        sql = f'SELECT COUNT({count_filter}) FROM {self.__name} WHERE {main_stat}'
        if additional_stats:
            for stat in additional_stats:
                sql += f' AND {stat}'
        self.__cursor.execute(sql)
        return self.__cursor.fetchone()[0]

