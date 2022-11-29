import unittest
import sqlite3


class TestSQLite(unittest.TestCase):
    def setUp(self) -> None:
        sqlite_connection = sqlite3.connect('sqlite_test.db')
        self.__cursor = sqlite_connection.cursor()

    def test_get_non_existent_table(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.__cursor.execute('SELECT * FROM non_existent_table')

    def test_create_table(self):
        table_name = 'test_table'
        self.__cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, value TEXT)')
        self.__cursor.execute(f'SELECT * FROM {table_name}')
        self.assertIsNotNone(self.__cursor.fetchall())

    def test_add_value(self):
        table_name = 'test_table'
        self.__cursor.execute(f'INSERT INTO {table_name} VALUES (3, "test3")')
        self.__cursor.execute(f'SELECT * FROM {table_name}')
        self.assertEqual(self.__cursor.fetchone(), (3, 'test3'))

    def test_delete_value_from_table(self):
        table_name = 'test_table'
        self.__cursor.execute(f'INSERT INTO {table_name} VALUES (2, "test2")')
        self.__cursor.execute(f'SELECT * FROM {table_name}')
        self.assertIsNotNone(self.__cursor.fetchone())
        self.__cursor.execute(f'DELETE FROM {table_name} WHERE id = 2')
        self.__cursor.execute(f'SELECT * FROM {table_name}')
        self.assertIsNone(self.__cursor.fetchone())
