import unittest

from two_fer import two_fer, two_fer_1

# Tests adapted from `problem-specifications//canonical-data.json`


class TwoFerTest(unittest.TestCase):
    def test_no_name_given(self):
        self.assertEqual(two_fer(), "One for you, one for me.")

    def test_a_name_given(self):
        self.assertEqual(two_fer("Alice"), "One for Alice, one for me.")

    def test_another_name_given(self):
        self.assertEqual(two_fer("Bob"), "One for Bob, one for me.")

    def test_no_name_given_1(self):
        self.assertEqual(two_fer_1(), "One for you, one for me.")

    def test_a_name_given_1(self):
        self.assertEqual(two_fer_1("Alice"), "One for Alice, one for me.")

    def test_another_name_given_1(self):
        self.assertEqual(two_fer_1("Bob"), "One for Bob, one for me.")


if __name__ == "__main__":
    unittest.main()