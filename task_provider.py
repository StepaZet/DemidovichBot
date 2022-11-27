import re

from database import Database
from subject_type import SubjectType
from task import Task, TaskType


class TaskProvider:
    def get_tasks(self, query: str) -> list[Task]:
        raise NotImplementedError()


def _get_task_numbers_from_query(query: str) -> list[str]:
    range_pattern = re.compile(r"(\d+)-(\d+)")
    numbers_pattern = re.compile(r"(\d+)(\.\d+)?")
    numbers = []

    range_match = re.findall(range_pattern, query)
    if range_match is not None:
        for match in range_match:
            start, end = match.split("-")[0], match.split("-")[1]
            numbers.extend(map(str, range(int(start), int(end) + 1)))
        return numbers[:10]

    numbers_match = re.findall(numbers_pattern, query)
    if numbers_match is not None:
        numbers.extend([m[0] + m[1] for m in numbers_match])

    return numbers[:10]


class DemidovichProvider(TaskProvider):
    def __init__(self):
        self.db = Database(SubjectType.DEMIDOVICH.value)

    def get_tasks(self, query: str) -> list[Task]:
        numbers = sorted(list(set(_get_task_numbers_from_query(query))))
        problems = [self.db.get_by_key(number) for number in numbers]
        tasks = [Task(TaskType.PHOTO, p) for p in problems]

        if len(tasks) == 10:
            tasks[-1].text = "Больше 10 заданий не дам"

        return tasks


class ProbabilitiesProvider(TaskProvider):
    def __init__(self):
        self.db = Database(SubjectType.PROBABILITIES.value)

    def get_tasks(self, query: str) -> list[Task]:
        link = self.db.get_by_key(query)
        return [Task(TaskType.TEXT, link)]
