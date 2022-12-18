from stat_repo import StatRepo


def get_statistic() -> str:
    res = (
        StatRepo()
        .get_unique_users_today()
        .get_unique_users_last_week()
        .get_unique_users_anytime()
        .build()
    )
    return res
