import pytest
from task_provider import DemidovichProvider, ProbabilitiesProvider
from unittest.mock import patch
from provider import Provider


class MockDataBase:
    def __init__(self, *args, **kwargs):
        pass

    def get_by_key(self, key):
        if key == '1':
            return '1.jpg'
        elif key == '01':
            return "ref"
        elif key == 'user':
            return 'Demidovich'
        else:
            raise KeyError


@pytest.fixture(scope="session")
def dem_provider():
    with patch('task_provider.Database', MockDataBase):
        return DemidovichProvider()


@pytest.fixture(scope="session")
def prob_provider():
    with patch('task_provider.Database', MockDataBase):
        return ProbabilitiesProvider()


@pytest.fixture(scope="session")
def provider():
    with patch('task_provider.Database', MockDataBase):
        with patch('provider.Database', MockDataBase):
            return Provider()
