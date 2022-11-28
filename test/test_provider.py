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


@patch('task_provider.Database', MockDataBase)
@patch('provider.Database', MockDataBase)
def test_get_tasks():
    provider = Provider()
    task = provider.get_tasks('user', '1')
    assert task == [Task(TaskType.PHOTO, '1.jpg', '')]

    task = provider.get_tasks('user', '2')
    assert task == [Task(TaskType.TEXT, 'Задача не найдена')]

    task = provider.get_tasks('user', '1.1')
    assert task == [Task(TaskType.PHOTO, '1.jpg', 'Задачу 1.1 не нашел, но нашел 1')]


@patch('task_provider.Database', MockDataBase)
@patch('provider.Database', MockDataBase)
def test_get_tasks_error():
    provider = Provider()
    with pytest.raises(ProviderError):
        provider.get_tasks('2', '1')


if __name__ == '__main__':
    unittest.main()