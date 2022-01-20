from helpers.valid_input import ValidInput

import unittest


class MyTestCase(unittest.TestCase):
    def test_input_number(self):
        valid_input = ValidInput('number', [1, 2]).input('Test: ')
        self.assertIn(valid_input, [1, 2])

    def test_input_str(self):
        valid_input = ValidInput('str', [1, 2]).input('Test: ')
        self.assertIn(valid_input, ['y', 'Y'])


if __name__ == '__main__':
    unittest.main()
