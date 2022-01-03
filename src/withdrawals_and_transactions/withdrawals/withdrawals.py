from src.withdrawals_and_transactions.withdrawals.withdrawals_text_cleaner import WithdrawalsTextCleaner
from src.withdrawals_and_transactions.helper import Helper


class Withdrawals:
    def __init__(self, whole_text=None):
        if whole_text is not None:
            helper = Helper
            cleaned_withdrawals_text = WithdrawalsTextCleaner(whole_text)
            self.whole_text = whole_text
            self.whole_text_wrapped = cleaned_withdrawals_text.get_wrapped_text()
            self.title = self.whole_text_wrapped[:self.whole_text_wrapped.find("\n")]  # The title is on top
            self.list_of_transactions = cleaned_withdrawals_text.cleaned_withdrawals

            total_withdrawals_text = cleaned_withdrawals_text.total_atm_and_debit_card__withdrawals_text
            self.total_withdrawals = {"text": total_withdrawals_text,
                                      "amount": helper.get_float_format(total_withdrawals_text)}

