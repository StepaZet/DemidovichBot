from subject_type import SubjectType
from stat_type import StatType
from task import Task


class Provider:
    def get_task(self, subject_type: SubjectType, task_id: int) -> Task:
        raise NotImplementedError()

    def get_statistic(self, stat_type: StatType) -> str:
        raise NotImplementedError()
