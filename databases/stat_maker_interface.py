from __future__ import annotations

from functools import lru_cache
from abc import ABC, abstractmethod


class IStatMaker(ABC):
    name = None

    def __init__(self):
        self._result = []

    @abstractmethod
    def build(self):
        raise NotImplementedError()


@lru_cache
def get_stat_makers() -> list[type[IStatMaker]]:
    return [stat_maker for stat_maker in IStatMaker.__subclasses__()]
