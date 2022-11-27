from subject_type import SubjectType
from database import Database
from stat_type import StatType
from task import Task
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
        self.db = Database("Users")

    def set_user_mode(self, user_id: str, mode: SubjectType):
        self.db.set(user_id, mode)

    def get_tasks(self, user_id: str, query: str) -> list[Task]:
        try:
            mode = self.db.get_by_key(user_id)
        except Exception as e:
            raise ProviderError("User has not a mode to get task") from e

        return self.subjects[SubjectType(mode)].get_tasks(query)

    def get_statistic(self, stat_type: StatType) -> str:
        raise NotImplementedError()
