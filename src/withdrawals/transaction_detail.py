from src.withdrawals.tansaction_detail_cleaner import TransactionCleaner
from src.withdrawals.helper import Helper


class TransactionDetail:
    def __init__(self, whole_text=None):
        if whole_text is not None:
            helper = Helper
            cleaned_withdrawals_text = TransactionCleaner(whole_text)
            self.cleaner = TransactionCleaner(whole_text)
            self.whole_text = whole_text
            self.whole_text_wrapped = cleaned_withdrawals_text.get_wrapped_text()

            beginning_balance_whole_text = self.whole_text_wrapped[:self.whole_text_wrapped.find("\n")]
            bb_text, bb_amount = Helper.get_text_and_amount_separated(beginning_balance_whole_text)  # BeginningBalance
            self.beginning_balance = {bb_text: Helper.get_float_format(bb_amount)}

            # self.list_of_transactions = cleaned_withdrawals_text.list[1:-1]
            #
            # total_withdrawals_text = cleaned_withdrawals_text.list[-1]
            # self.total_withdrawals = {"text": total_withdrawals_text,
            #                           "amount": helper.get_total_from_this_string(total_withdrawals_text)}

