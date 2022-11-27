import pickledb
import os


class Database:
    def __init__(self, table_name: str | None):
        """
        Creates or gets table with given name from database

        Database tables:
        Users: (user_id: mode)
        Demidovich: (task_id: task)
        Probabilities: (task_id: task)

        :param table_name: Name of table
        """
        if not os.path.exists('database.db'):
            raise FileNotFoundError('Database file not found')
        self.__db = pickledb.load('database.db', False)
        self._create_if_not_exists(table_name)
        self.__table_name = table_name

    def get_by_key(self, identifier: str):
        return self.__db.dget(self.__table_name, identifier)

    def get_all(self) -> list:
        return self.__db.dgetall(self.__table_name)

    def set(self, identifier: str, value):
        if self.__db.dexists(self.__table_name, identifier):
            self.__db.drem(self.__table_name, identifier)
        self.__db.dadd(self.__table_name, (identifier, value))
        self.__db.dump()

    def _create_if_not_exists(self, table_name):
        try:
            self.__db.dgetall(table_name)
        except KeyError:
            self.__db.dcreate(table_name)
            self.__db.dump()
