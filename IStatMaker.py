from functools import lru_cache


class IStatMaker:
    name = None

    def __init__(self):
        self._result = []

    def build(self):
        pass


@lru_cache
def get_stat_makers() -> list[type['IStatMaker']]:
    return [stat_maker for stat_maker in IStatMaker.__subclasses__()]  # TODO: мб сделать один статический метод по получению сабклассов?