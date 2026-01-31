import unittest
from datetime import datetime


class TestSanity(unittest.TestCase):
    def test_date_format(self):
        d = datetime.now()
        self.assertIsInstance(d.strftime("%Y-%m-%d"), str)


if __name__ == "__main__":
    unittest.main()
