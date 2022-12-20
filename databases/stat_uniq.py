from databases.stat_maker_interface import IStatMaker
from databases.stat_repo import StatRepo


class UniqueStat(IStatMaker):
    name = 'unique'

    def __init__(self):
        super().__init__()
        self._repo = StatRepo()
        self.result = []

    def build(self) -> str:
        self.result.append(self._repo.get_unique_users_today())
        self.result.append(self._repo.get_unique_users_last_week())
        self.result.append(self._repo.get_unique_users_anytime())
        return '\n'.join(self._result)
