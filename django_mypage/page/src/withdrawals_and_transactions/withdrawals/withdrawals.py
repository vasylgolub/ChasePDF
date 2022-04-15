from ..withdrawals.withdrawals_text_cleaner import WithdrawalsTextCleaner
from ..helper import Helper

class Withdrawals:
    def __init__(self, whole_text=None):
        if whole_text is not None:
            helper = Helper
            cleaned_withdrawals_text = WithdrawalsTextCleaner(whole_text)
            self.whole_text = whole_text
            self.title = "ATM & DEBIT CARD WITHDRAWALS"
            self.list_of_withdrawals = cleaned_withdrawals_text.cleaned_withdrawals
            total_withdrawals_text = cleaned_withdrawals_text.total_info
            self.total_withdrawals: dict = {"text": total_withdrawals_text,
                                            "amount": helper.get_float_format(total_withdrawals_text)}
            self.whole_text_wrapped = \
                self.title + "\n" + cleaned_withdrawals_text.get_wrapped_text() + "\n" + total_withdrawals_text
