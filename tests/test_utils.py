import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import seriesbr.helpers.utils as utils


class TestUtils(unittest.TestCase):
    def test_concatenate_by_separator_if_iterable(self):
        test = [utils.cat([1, 2, 3, 4], ","), utils.cat(2, ","), utils.cat((4, 5), ",")]
        correct = ["1,2,3,4", 2, "4,5"]
        self.assertListEqual(test, correct)

    def test_is_isterable(self):
        to_test = [[1], (1,), 1, {1: 1}, "1"]
        test = list(map(utils.isiterable, to_test))
        correct = [True, True, False, True, True]
        self.assertListEqual(test, correct)


if __name__ == "__main__":
    unittest.main()
