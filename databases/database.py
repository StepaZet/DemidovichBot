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
        self.name = table_name
        self._db = pickledb.load('database.db', False, sig=False)
        self._create_if_not_exists(table_name)

    def get_by_key(self, identifier: str):
        return self._db.dget(self.name, identifier)

    def get_all(self) -> list:
        return self._db.dgetall(self.name)

    def set(self, identifier: str, value):
        if self._db.dexists(self.name, identifier):
            self._db.dpop(self.name, identifier)
        self._db.dadd(self.name, (identifier, value))
        self._db.dump()

    def _create_if_not_exists(self, table_name):
        try:
            self._db.dgetall(table_name)
        except KeyError:
            self._db.dcreate(table_name)
            self._db.dump()
