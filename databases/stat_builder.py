from databases.stat_maker_interface import get_stat_makers, IStatMaker


class StatBuilder:
    def __init__(self):
        self.stat_dict = {}
        for stat_maker in get_stat_makers():
            self.stat_dict[stat_maker.name] = stat_maker()

    def build(self, stat_names: list[str]) -> list[str]:
        result = []
        for stat_maker in self.get_required_stat_makers(stat_names):
            result.append(stat_maker.build())
        return result

    def get_required_stat_makers(
            self,
            stat_names: list[str]
    ) -> list[IStatMaker]:
        for stat_name in stat_names:
            if stat_name in self.stat_dict:
                yield self.stat_dict[stat_name]
