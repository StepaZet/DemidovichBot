class Database:
    def __init__(self, table_name):
        """
        Creates or gets table with given name from database

        Database tables:
        Users: (user_id: mode)
        Demidovich: (task_id: task)
        Probabilities: (task_id: task)

        :param table_name: Name of table
        """
        pass

    def get_by_key(self, identifier: int):
        pass

    def get_all(self) -> list:
        pass

    def set(self, identifier: int, value):
        pass