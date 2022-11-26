from database import Database
from subject_type import SubjectType
from task import Task, TaskType


class TaskProvider:
    def get_task(self, task_id: int) -> Task:
        raise NotImplementedError()


class DemidovichProvider(TaskProvider):
    def __init__(self):
        self.db = Database(SubjectType.DEMIDOVICH.value)

    def get_task(self, task_id: int) -> Task:
        task = self.db.get_by_key(task_id)
        return Task(TaskType.PHOTO, task)


class ProbabilitiesProvider(TaskProvider):
    def __init__(self):
        self.db = Database(SubjectType.PROBABILITIES.value)

    def get_task(self, task_id: int) -> Task:
        task = self.db.get_by_key(task_id)
        return Task(TaskType.TEXT, task)
