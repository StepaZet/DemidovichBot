import pytest
import os

from database import Database


@pytest.fixture(scope='function')
def test_db():
    if not os.path.exists('database.db'):
        with open('database.db', 'w') as f:
            f.write('{}')

    db = Database('test')
    db.set('test', 'test')
    yield db
    os.remove('database.db')


def test_get_by_key(test_db):
    assert test_db.get_by_key('test') == 'test'


def test_get_all(test_db):
    test_db.set('test2', 'test2')
    assert test_db.get_all() == {'test': 'test', 'test2': 'test2'}


def test_set(test_db):
    assert test_db.get_by_key('test') == 'test'


def test_get_non_existing_key_raises_key_error(test_db):
    with pytest.raises(KeyError):
        test_db.get_by_key('test1')


def test_set_existing_key_updates_value(test_db):
    test_db.set('test', 'test1')
    assert test_db.get_by_key('test') == 'test1'


if __name__ == '__main__':
    pytest.main()
