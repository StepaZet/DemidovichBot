import unittest
import pytest

from unittest.mock import patch
from provider import Provider, ProviderError
from task import Task, TaskType


class MockDataBase:
    def __init__(self, *args, **kwargs):
        pass

    def get_by_key(self, key):
        if key == '1':
            return '1.jpg'
        elif key == 'user':
            return 'Demidovich'
        else:
            raise KeyError


def assert_single_task_equals(tasks: list[Task],
                              data: str,
                              task_type: TaskType):
    assert len(tasks) == 1
    assert tasks[0].data == data
    assert tasks[0].task_type == task_type


@patch('task_provider.Database', MockDataBase)
@patch('provider.Database', MockDataBase)
def test_get_tasks():
    provider = Provider()
    task = provider.get_tasks('user', '1')
    assert_single_task_equals(task, "1.jpg", TaskType.PHOTO)

    task = provider.get_tasks('user', '2')
    assert_single_task_equals(task, "Задача не найдена 🤥", TaskType.TEXT)

    task = provider.get_tasks('user', '1.1')
    assert_single_task_equals(task, "1.jpg", TaskType.PHOTO)


@patch('task_provider.Database', MockDataBase)
@patch('provider.Database', MockDataBase)
def test_get_tasks_error():
    provider = Provider()
    with pytest.raises(ProviderError):
        provider.get_tasks('2', '1')


if __name__ == '__main__':
    unittest.main()
