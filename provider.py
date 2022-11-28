from subject_type import SubjectType
from database import Database
from stat_type import StatType
from task import Task
from event import Event
from sqlite_wrapper import SQLiteDB
from task_provider import TaskProvider, \
    DemidovichProvider,\
    ProbabilitiesProvider


class ProviderError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Provider:
    def __init__(self):
        self.subjects: dict[SubjectType, TaskProvider] = {
            SubjectType.DEMIDOVICH: DemidovichProvider(),
            SubjectType.PROBABILITIES: ProbabilitiesProvider(),
        }
        self.__db = Database("Users")
        self.event = Event()

    def set_user_mode(self, user_id: str, mode: SubjectType):
        self.__db.set(user_id, mode.value)

    def get_tasks(self, user_id: str, query: str) -> list[Task]:
        try:
            mode = self.__db.get_by_key(user_id)
        except KeyError as e:
            raise ProviderError("User has not a mode to get task") from e
        res = self.subjects[SubjectType(mode)].get_tasks(query)
        res_data = [task.data for task in res]
        self.event(user_id, query, str(res_data), mode)
        return res

    def get_statistic(self, stat_type: StatType) -> str:
        raise NotImplementedError()
