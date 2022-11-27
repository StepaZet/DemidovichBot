import unittest
import pickledb


class TestDB(unittest.TestCase):
    def setUp(self):
        self.test_db = pickledb.load('test.db', False)
        self.test_db.dcreate('test_dict')
        self.test_db.dump()

    def test_get_non_existent_dict(self):
        with self.assertRaises(KeyError):
            values = self.test_db.dgetall('non_existent_dict')

    def test_get_non_existent_key(self):
        with self.assertRaises(KeyError):
            value = self.test_db.dget('test_dict', 'non_existent_key')

    def test_get_existed_db(self):
        test_dict = pickledb.load('test_dict', False)
        self.assertIsNotNone(test_dict)

