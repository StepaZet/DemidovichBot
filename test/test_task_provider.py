import pytest

from providers.task import Task, TaskType


def assert_single_task_equals(tasks: list[Task],
                              data: str,
                              task_type: TaskType):
    assert len(tasks) == 1
    assert tasks[0].data == data
    assert tasks[0].task_type == task_type


def test_get_existing_demidovich_task(dem_provider):
    task = dem_provider.get_tasks('1')
    assert_single_task_equals(task, "1.jpg", TaskType.PHOTO)


def test_get_non_existing_demidovich_returns_text(dem_provider):
    task = dem_provider.get_tasks('2')
    assert_single_task_equals(task, "Задача не найдена 🤥", TaskType.TEXT)


def test_get_demidovich_dot_subtask_returns_no_dot(dem_provider):
    task = dem_provider.get_tasks('1.1')
    assert_single_task_equals(task, "1.jpg", TaskType.PHOTO)


def test_probabilities_provider(prob_provider):
    task = prob_provider.get_tasks('01')
    assert task == [Task(TaskType.TEXT, 'ref', "Вот твое задание 01 😘")]

    task = prob_provider.get_tasks('02')
    assert task == [Task(TaskType.TEXT, 'Такой практики нет 🤥')]


if __name__ == '__main__':
    pytest.main()
