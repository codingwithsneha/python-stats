import unittest
from datetime import datetime, timedelta


class TestDates(unittest.TestCase):
    def test_past_dates_only(self):
        today = datetime.now()
        past = today - timedelta(days=365)
        self.assertLess(past, today)


if __name__ == "__main__":
    unittest.main()
