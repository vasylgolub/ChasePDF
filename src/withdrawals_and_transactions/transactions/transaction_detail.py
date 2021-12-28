from src.withdrawals_and_transactions.transactions.transaction_details_cleaner import TransactionCleaner
from src.withdrawals_and_transactions.helper import Helper


class TransactionDetail:
    def __init__(self, whole_text=None):
        if whole_text is not None:
            cleaned_withdrawals_text = TransactionCleaner(whole_text)
            # self.cleaner = TransactionCleaner(whole_text)
            self.whole_text = whole_text
            self.whole_text_wrapped = cleaned_withdrawals_text.get_wrapped_text()
            self.beginning_balance = Helper.get_beginning_balance_as_dictionary(self.whole_text_wrapped)
            self.ending_balance = Helper.get_ending_balance_as_dictionary(self.whole_text_wrapped)
            self.list_of_transactions = cleaned_withdrawals_text.list[1:-1]
            self.total_sum_transactions = Helper.get_sum_of_all_transactions(self.list_of_transactions)


    def get_summary_in_text(self):
        beg = self.beginning_balance["Beginning Balance"]
        tot = self.total_sum_transactions
        end = self.ending_balance["Ending Balance"]
        beg_and_tot = (beg * 100 + tot * 100) / 100
        lines = "-------------------------------"
        textual_result = f"Beginning Balance: {beg: 12} +\n" \
                         f"Sum of all Transactions: {tot} =\n" \
                         f"{lines}\n" \
                         f"Result:{beg_and_tot: 24}\n" \
                         f"{lines}\n" \
                         f"Ending Balance: {end: 15}"
        return textual_result

    def is_total_sum_correct(self):
        beg = self.beginning_balance["Beginning Balance"]
        tot = self.total_sum_transactions
        end = self.ending_balance["Ending Balance"]
        return (beg * 100 + tot * 100 - end * 100) == 0
