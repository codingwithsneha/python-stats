import unittest
import contribute


class TestContribute(unittest.TestCase):

    def test_arguments(self):
        args = contribute.arguments(['-nw'])
        self.assertTrue(args.no_weekends)
        self.assertEqual(args.max_commits, 10)

    def test_contributions_per_day(self):
        args = contribute.arguments([])
        commits = contribute.contributions_per_day(args)
        self.assertTrue(1 <= commits <= 20)


if __name__ == "__main__":
    unittest.main()
