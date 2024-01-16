import unittest

from ..withdrawals_and_transactions.extractor import Extractor


class TestSum(unittest.TestCase):

    def test_extract_store_online_transfer(self):
        full_text = "02/14Online Transfer From Chk ...7190 Transaction#: 16575245781 100.00"
        expected_res = "Online Transfer From Chk ...7190 Transaction#: 16575245781"
        print(full_text)
        self.assertEqual(expected_res, Extractor(full_text).store)


    def test_extract_store_when_monthly_service_fee(self):
        full_text = "02/15Monthly Service Fee -12.00"
        expected_res = "Monthly Service Fee"
        self.assertEqual(expected_res, Extractor(full_text).store)


    def test_extract_store_when_non_chase_atm_fee(self):
        full_text = "02/01Non-Chase ATM Fee-With -5.00"
        expected_res = "Non-Chase ATM Fee-With"
        self.assertEqual(expected_res, Extractor(full_text).store)


if __name__ == '__main__':
    unittest.main()