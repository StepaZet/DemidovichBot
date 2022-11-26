import unittest
import pickledb


class TestDB(unittest.TestCase):
    def setUp(self):
        self.test_db = pickledb.load('test.db', False)
        self.test_db.dcreate('test_dict')

    def test_get_non_existent_dict(self):
        with self.assertRaises(KeyError):
            values = self.test_db.dgetall('non_existent_dict')

    def test_get_existed_db(self):
        test_dict = pickledb.load('test_dict', False)
        self.assertIsNotNone(test_dict)

