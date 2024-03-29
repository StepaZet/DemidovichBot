from __future__ import annotations

import re

from abc import ABC, abstractmethod
from databases.database import Database
from functools import lru_cache
from providers.subject_type import SubjectType
from providers.task import Task, TaskType


@lru_cache()
def get_providers() -> list[type[TaskProvider]]:
    return [provider for provider in TaskProvider.__subclasses__()]


class TaskProvider(ABC):
    button_name = None
    button_message = None
    subject_type = None

    def __init__(self, subject_type: SubjectType):
        self._db = Database(str(subject_type.value))

    @staticmethod
    def get_provider_by_subject_type(
            subject_type: SubjectType
    ) -> TaskProvider:
        for _provider in get_providers():
            if _provider.subject_type == subject_type:
                return _provider()
        raise ValueError(f"Provider for {subject_type} not found")

    def get_tasks(self, query: str) -> list[Task]:
        numbers = sorted(list(set(_get_task_numbers_from_query(query))))
        tasks = [self._get_task_by_number(number) for number in numbers]

        if len(tasks) == 10:
            tasks[-1].text = "Больше 10 заданий не дам"

        return tasks

    def _get_task_by_number(self, number: str) -> Task:
        return self._create_task_by_number(
            number, self._create_task, self._create_unknown_task,
            f'Вот твое задание {number} 😘'
        )

    def _create_task_by_number(self, number: str, task_creator,
                               create_unknown_task, message: str = "") -> Task:
        try:
            return task_creator(self._db.get_by_key(number), message)
        except KeyError:
            return create_unknown_task(number)

    @abstractmethod
    def _create_task(self, task, message: str) -> Task:
        raise NotImplementedError()

    @abstractmethod
    def _create_unknown_task(self, number: str) -> Task:
        raise NotImplementedError()


class DemidovichProvider(TaskProvider):
    button_name = 'Демидович'
    button_message = 'Выбран Демидович\nНапиши номер(а) задачи(задачек)'
    subject_type = SubjectType.DEMIDOVICH

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
                f"Задачу {number} не нашел, но, возможно, она есть на "
                f"картинке с номером {number.split('.')[0]}🙄"
            )

        return Task(TaskType.TEXT, "Задача не найдена 🤥")


class ProbabilitiesProvider(TaskProvider):
    button_name = 'Тервер (ФИИТ)'
    button_message = 'Выбран Тервер (ФИИТ)\nНапиши номер(а) практики(практик)'
    subject_type = SubjectType.PROBABILITIES

    def __init__(self):
        super().__init__(SubjectType.PROBABILITIES)

    def _create_task(self, task_text, message):
        return Task(TaskType.TEXT, task_text, message)

    def _create_unknown_task(self, number):
        return Task(TaskType.TEXT, "Такой практики нет 🤥")


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
