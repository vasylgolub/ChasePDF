from src.withdrawals.withdrawals_text_cleaner import WithdrawalsTextCleaner
from src.withdrawals.helper import Helper


class Withdrawals:
    def __init__(self, whole_text=None):
        if whole_text is not None:
            helper = Helper
            cleaned_withdrawals_text = WithdrawalsTextCleaner(whole_text)
            self.cleaner = WithdrawalsTextCleaner(whole_text)
            self.whole_text = whole_text
            self.whole_text_wrapped = cleaned_withdrawals_text.get_wrapped_text()
            self.title = self.whole_text_wrapped[:self.whole_text_wrapped.find("\n")]  # The title is on top
            self.list_of_transactions = cleaned_withdrawals_text.list[1:-1]

            total_withdrawals_text = cleaned_withdrawals_text.list[-1]
            self.total_withdrawals = {"text": total_withdrawals_text,
                                      "amount": helper.get_total_from_this_string(total_withdrawals_text)}

