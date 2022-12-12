import unittest

from task import Task, TaskType
from test_provider import assert_single_task_equals


def test_get_existing_demidovich_task(dem_provider):
    task = dem_provider.get_tasks('1')
    assert_single_task_equals(task, "1.jpg", TaskType.PHOTO)


def test_get_non_existing_demidovich_task(dem_provider):
    task = dem_provider.get_tasks('2')
    assert_single_task_equals(task, "Задача не найдена 🤥", TaskType.TEXT)


def test_get_demidovich_dot_subtask(dem_provider):
    task = dem_provider.get_tasks('1.1')
    assert_single_task_equals(task, "1.jpg", TaskType.PHOTO)


def test_probabilities_provider(prob_provider):
    task = prob_provider.get_tasks('01')
    assert task == [Task(TaskType.TEXT, 'ref', "Вот твое задание 01 😘")]

    task = prob_provider.get_tasks('02')
    assert task == [Task(TaskType.TEXT, 'Такой практики нет 🤥')]


if __name__ == '__main__':
    unittest.main()
