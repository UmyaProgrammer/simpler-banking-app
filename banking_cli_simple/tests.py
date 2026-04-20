import unittest
from unittest.mock import patch
from banking_cli import read_float, BankingService


class TestBanking(unittest.TestCase):
    # Patch allows you to simulate user inputs.
    @patch('builtins.input', return_value='123.45')
    def test_read_float_valid(self, mock_input):
        result = read_float("Enter amount: ")
        self.assertEqual(result, 123.45)

    @patch('builtins.input', return_value='')
    def test_read_float_empty(self, mock_input):
        result = read_float("Enter amount: ")
        self.assertIsNone(result)

    @patch('builtins.input', return_value='abc')
    def test_read_float_invalid(self, mock_input):
        result = read_float("Enter amount: ")
        self.assertIsNone(result)


    # --- Test get_balance ---

    def test_get_balance_someone(self):
        service = BankingService()

        # This assumes "someone" already exists in your DB with balance = 400.00
        balance = service.get_balance("someone")

        self.assertEqual(balance, 400.00)


if __name__ == '__main__':
    unittest.main()