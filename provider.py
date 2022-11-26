from subject_type import SubjectType
from stat_type import StatType
from task import Task
from task_provider import TaskProvider, \
    DemidovichProvider,\
    ProbabilitiesProvider


class Provider:
    def __init__(self):
        self.subjects: dict[SubjectType, TaskProvider] = {
            SubjectType.DEMIDOVICH: DemidovichProvider(),
            SubjectType.PROBABILITIES: ProbabilitiesProvider(),
        }

    def get_task(self, subject_type: SubjectType, task_id: int) -> Task:
        return self.subjects[subject_type].get_task(task_id)

    def get_statistic(self, stat_type: StatType) -> str:
        raise NotImplementedError()
