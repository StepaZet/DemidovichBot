import sqlite3
from database import Database


def add_task(user_id: str, query: str, res: str, mode: str) -> None:
    sqlite_db = SQLiteDB()
    sqlite_db.add_note_to_db(user_id, query, res, mode)


class SQLiteDB:
    def __init__(self):
        self.__sqlite_connection = sqlite3.connect('sqlite.db')
        self.__cursor = self.__sqlite_connection.cursor()
        self.__cursor.execute('CREATE TABLE IF NOT EXISTS stats (user_id TEXT, date datetime, mode TEXT, query TEXT, answer TEXT);')

    def add_note_to_db(self, user_id: str, query: str, answer: str, mode: str) -> None:
        self.__cursor.execute(f'INSERT INTO stats VALUES (?,datetime("now"),?,?,?);', (user_id, mode, query, answer))
        self.__sqlite_connection.commit()

    def get_queries_amount_by_user_and_date(self, user_id: int, days_count: int) -> int:
        self.__cursor.execute(f'SELECT COUNT(*) FROM stats WHERE user_id = "{user_id}" '
                       f'AND date >= datetime("now", "-{days_count} days") AND date <= datetime("now");')
        return self.__cursor.fetchone()[0]

    def get_unique_users_by_days(self, days_count: int = 1) -> int:
        self.__cursor.execute(f'SELECT COUNT(DISTINCT user_id) FROM stats WHERE date >= datetime("now", "-{days_count} days") '
                       f'AND date <= datetime("now");')
        return self.__cursor.fetchone()[0]

    def get_unique_users(self) -> int:
        self.__cursor.execute(f'SELECT COUNT(DISTINCT user_id) FROM stats;')
        return self.__cursor.fetchone()[0]

    def get_unique_users_by_mode_and_days(self, mode: str, days_count: int = 1) -> int:
        self.__cursor.execute(f'SELECT COUNT(DISTINCT user_id) FROM stats WHERE mode = "{mode}" '
                       f'AND date >= datetime("now", "-{days_count} days") AND date <= datetime("now");')
        return self.__cursor.fetchone()[0]

    def get_unique_users_by_mode(self, mode: str) -> int:
        self.__cursor.execute(f'SELECT COUNT(DISTINCT user_id) FROM stats WHERE mode = "{mode}";')
        return self.__cursor.fetchone()[0]

    def get_queries_amount_by_date(self, days_count: int = 1) -> int:
        self.__cursor.execute(f'SELECT COUNT(*) FROM stats WHERE date >= datetime("now", "-{days_count} days") '
                       f'AND date <= datetime("now");')
        return self.__cursor.fetchone()[0]

    def delete_month_old_notes(self) -> None:
        self.__cursor.execute(f'DELETE FROM stats WHERE date <= datetime("now", "-1 month");')
        self.__sqlite_connection.commit()

    def get_most_popular_day(self) -> str:
        self.__cursor.execute(f'SELECT date FROM stats GROUP BY date ORDER BY COUNT(*) DESC LIMIT 1;')
        return self.__cursor.fetchone()[0]

    def clear_db(self) -> None:
        self.__cursor.execute(f'DELETE FROM stats;')
        self.__sqlite_connection.commit()
