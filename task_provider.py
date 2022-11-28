import re

from database import Database
from subject_type import SubjectType
from task import Task, TaskType


class TaskProvider:
    def __init__(self, subject_type: SubjectType):
        self.__db = Database(str(subject_type.value))

    def get_tasks(self, query: str) -> list[Task]:
        numbers = sorted(list(set(_get_task_numbers_from_query(query))))
        tasks = [self._get_task_by_number(number) for number in numbers]

        if len(tasks) == 10:
            tasks[-1].text = "Больше 10 заданий не дам"

        return tasks

    def _get_task_by_number(self, number: str) -> Task:
        return self._create_task_by_number(number, self._create_task, self._create_unknown_task)

    def _create_task_by_number(self, number: str, task_creator, create_unknown_task, message: str = "") -> Task:
        try:
            return task_creator(self.__db.get_by_key(number), message)
        except KeyError:
            return create_unknown_task(number)

    def _create_task(self, task, message: str) -> Task:
        raise NotImplementedError("Unable to create task in abstract class")

    def _create_unknown_task(self, number: str) -> Task:
        raise NotImplementedError("Unable to create unknown task in abstract class")


class DemidovichProvider(TaskProvider):
    def __init__(self):
        super().__init__(SubjectType.DEMIDOVICH)

    def _create_task(self, task_text, message):
        return Task(TaskType.PHOTO, task_text, message)

    def _create_unknown_task(self, number):
        if "." in number:
            return self._create_task_by_number(
                number.split(".")[0],
                self._create_task,
                self._create_unknown_task,
                f"Задачу {number} не нашел, но нашел {number.split('.')[0]}"
            )

        return Task(TaskType.TEXT, "Задача не найдена")


class ProbabilitiesProvider(TaskProvider):
    def __init__(self):
        super().__init__(SubjectType.PROBABILITIES)

    def _create_task(self, task_text, message):
        return Task(TaskType.TEXT, task_text, message)

    def _create_unknown_task(self, number):
        return Task(TaskType.TEXT, "Такой практики нет(")


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
