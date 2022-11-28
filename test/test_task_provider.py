import unittest

from unittest.mock import patch
from task_provider import DemidovichProvider, ProbabilitiesProvider
from task import Task, TaskType


class MockDataBase:
    def __init__(self, *args, **kwargs):
        pass

    def get_by_key(self, key):
        if key == '1':
            return '1.jpg'
        elif key == '01':
            return "ref"
        else:
            raise KeyError


@patch('task_provider.Database', MockDataBase)
def test_demidovich_provider():
    provider = DemidovichProvider()
    task = provider.get_tasks('1')
    assert task == [Task(TaskType.PHOTO, '1.jpg', '')]

    task = provider.get_tasks('2')
    assert task == [Task(TaskType.TEXT, 'Задача не найдена')]

    task = provider.get_tasks('1.1')
    assert task == [Task(TaskType.PHOTO, '1.jpg', 'Задачу 1.1 не нашел, но нашел 1')]


@patch('task_provider.Database', MockDataBase)
def test_probabilities_provider():
    provider = ProbabilitiesProvider()
    task = provider.get_tasks('01')
    assert task == [Task(TaskType.TEXT, 'ref')]

    task = provider.get_tasks('02')
    assert task == [Task(TaskType.TEXT, 'Такой практики нет(')]


if __name__ == '__main__':
    unittest.main()
