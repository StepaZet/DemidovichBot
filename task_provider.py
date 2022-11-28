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
    if len(range_match) > 0:
        for match in range_match:
            start, end = int(match[0]), int(match[1])
            numbers.extend(map(str, range(start, end + 1)))
        return numbers[:10]

    numbers_match = re.findall(numbers_pattern, query)
    if len(numbers_match) > 0:
        numbers.extend([m[0] + m[1] for m in numbers_match])

    return numbers[:10]


class DemidovichProvider(TaskProvider):
    def __init__(self):
        self.__db = Database(SubjectType.DEMIDOVICH.value)

    def get_tasks(self, query: str) -> list[Task]:
        numbers = sorted(list(set(_get_task_numbers_from_query(query))))
        tasks = [self.__get_task_by_number(number) for number in numbers]

        if len(tasks) == 10:
            tasks[-1].text = "Больше 10 заданий не дам"

        return tasks

    def __get_task_by_number(self, number: str, message: str = "") -> Task:
        try:
            return Task(TaskType.PHOTO, self.__db.get_by_key(number), message)
        except KeyError:
            if "." in number:
                return self.__get_task_by_number(number.split(".")[0], f"Задачу {number} не нашел, "
                                                                       f"но нашел {number.split('.')[0]}")
            return Task(TaskType.TEXT, "Задача не найдена")


class ProbabilitiesProvider(TaskProvider):
    def __init__(self):
        self.__db = Database(SubjectType.PROBABILITIES.value)

    def get_tasks(self, query: str) -> list[Task]:
        try:
            link = self.__db.get_by_key(query)
        except KeyError:
            return [Task(TaskType.TEXT, "Такой практики нет(")]
        return [Task(TaskType.TEXT, link)]
