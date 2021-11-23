import unittest

from Nato import transmit, receive

# Tests adapted from `problem-specifications//canonical-data.json`


class NatoTest(unittest.TestCase):

    def test_a_name_transmit(self):
        self.assertEqual(transmit("Hello, World!"), "HOTEL ECHO LIMA LIMA OSCAR WHISKEY OSCAR ROMEO LIMA DELTA")


    def test_a_name_transmit_two(self):
        self.assertEqual(transmit("NCC-1701-D"), "NOVEMBER CHARLIE CHARLIE ONE SEVEN ZERO ONE DELTA")


    def test_a_name_recieve(self):
        self.assertEqual(receive("HOTEL ECHO LIMA LIMA OSCAR WHISKEY OSCAR ROMEO LIMA DELTA"), "HELLOWORLD")


    def test_a_name_recieve_two(self):
        self.assertEqual(receive("NOVEMBER CHARLIE CHARLIE ONE SEVEN ZERO ONE DELTA"), "NCC1701D")

    


if __name__ == "__main__":
    unittest.main()
