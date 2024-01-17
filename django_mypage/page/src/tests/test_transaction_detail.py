import unittest

from ..withdrawals_and_transactions.transactions.transaction_detail import TransactionDetail


class TestTransactionDetail(unittest.TestCase):

    def test_extract_beginning_balance(self):
        sample_text = "TRANSACTION DETAILDATEDESCRIPTIONAMOUNTBALANCEBeginning Balance$116.8102/01Non-Chase ATM Withdraw 02/01 Lungo Lago Giac Porlezza CO LA Card 3232-115.461.3502/01Non-Chase ATM Fee-With-5.00-3.6502/02Online Transfer From Chk ...7190 Transaction#: 16441988603150.00146.3502/07Card Purchase 02/06 Poste Italiane Porlezza Card 3232 Euro 37.50 X 1.094133 (Exchg Rte)-41.03105.3202/07Foreign Exch Rt ADJ Fee 02/06 Poste Italiane Porlezza Card 3232-1.23104.0902/09Card Purchase 02/07 Brico Io Carlazzo Carlazzo Card 3232 Euro 24.90 X 1.079920 (Exchg Rte)-26.8977.2002/09Card Purchase 02/08 Iperal Carlazzo Carlazzo Card 3232 Euro 25.43 X 1.077074 (Exchg Rte)-27.3949.8102/09Foreign Exch Rt ADJ Fee 02/08 Iperal Carlazzo Carlazzo Card 3232-0.8248.9902/09Foreign Exch Rt ADJ Fee 02/07 Brico Io Carlazzo Carlazzo Card 3232-0.8048.1902/14Online Transfer From Chk ...7190 Transaction#: 16575245781100.00148.1902/15Monthly Service Fee-12.00136.19Ending Balance $136.19"
        expected_res = 116.81

        td_object = TransactionDetail(sample_text)

        self.assertEqual(expected_res, td_object.beginning_balance["Beginning Balance"])

    def test_extract_negative_beginning_balance(self):
        sample_text = "TRANSACTION DETAILDATEDESCRIPTIONAMOUNTBALANCEBeginning Balance-$116.8102/01Non-Chase ATM Withdraw 02/01 Lungo Lago Giac Porlezza CO LA Card 3232-115.461.3502/01Non-Chase ATM Fee-With-5.00-3.6502/02Online Transfer From Chk ...7190 Transaction#: 16441988603150.00146.3502/07Card Purchase 02/06 Poste Italiane Porlezza Card 3232 Euro 37.50 X 1.094133 (Exchg Rte)-41.03105.3202/07Foreign Exch Rt ADJ Fee 02/06 Poste Italiane Porlezza Card 3232-1.23104.0902/09Card Purchase 02/07 Brico Io Carlazzo Carlazzo Card 3232 Euro 24.90 X 1.079920 (Exchg Rte)-26.8977.2002/09Card Purchase 02/08 Iperal Carlazzo Carlazzo Card 3232 Euro 25.43 X 1.077074 (Exchg Rte)-27.3949.8102/09Foreign Exch Rt ADJ Fee 02/08 Iperal Carlazzo Carlazzo Card 3232-0.8248.9902/09Foreign Exch Rt ADJ Fee 02/07 Brico Io Carlazzo Carlazzo Card 3232-0.8048.1902/14Online Transfer From Chk ...7190 Transaction#: 16575245781100.00148.1902/15Monthly Service Fee-12.00136.19Ending Balance $136.19"
        expected_res = -116.81

        td_object = TransactionDetail(sample_text)

        self.assertEqual(expected_res, td_object.beginning_balance["Beginning Balance"])


if __name__ == '__main__':
    unittest.main()




