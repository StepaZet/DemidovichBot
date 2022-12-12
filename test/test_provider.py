import unittest
import pytest

from provider import ProviderError
from task import Task, TaskType


def assert_single_task_equals(tasks: list[Task],
                              data: str,
                              task_type: TaskType):
    assert len(tasks) == 1
    assert tasks[0].data == data
    assert tasks[0].task_type == task_type


def test_get_existing_task(provider):
    task = provider.get_tasks('user', '1')
    assert_single_task_equals(task, "1.jpg", TaskType.PHOTO)


def test_get_non_existing_task(provider):
    task = provider.get_tasks('user', '2')
    assert_single_task_equals(task, "Задача не найдена 🤥", TaskType.TEXT)


def test_get_dot_subtask(provider):
    task = provider.get_tasks('user', '1.1')
    assert_single_task_equals(task, "1.jpg", TaskType.PHOTO)


def test_get_tasks_error(provider):
    with pytest.raises(ProviderError):
        provider.get_tasks('2', '1')


if __name__ == '__main__':
    unittest.main()
