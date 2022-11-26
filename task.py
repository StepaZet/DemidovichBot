from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    TEXT = 0
    PHOTO = 1


@dataclass
class Task:
    task_type: TaskType
    data: str
    text: str | None = None
