class StatisticRepository:
    def __init__(self, db):
        self.__db = db

    def add_task(self, user_id: str, query: str, res: str, mode: str) -> None:
        self.__db.add_note_to_db(user_id, query, res, mode)

    def get_unique_users_by_day(self) -> int:
        return self.__db.get_unique_notes_by_stat(1)

    def get_unique_users_by_week(self) -> int:
        return self.__db.get_unique_notes_by_stat(7)

    def get_unique_users_anytime(self) -> int:
        return self.__db.get_unique_notes_by_stat()



