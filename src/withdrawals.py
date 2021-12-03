from src.withdrawals_text_cleaner import WithdrawalsTextCleaner


class Withdrawals:
    def __init__(self, whole_text):
        cleaned_withdrawals_text = WithdrawalsTextCleaner(whole_text)
        self.whole_text = whole_text
        self.whole_text_wrapped = cleaned_withdrawals_text.get_wrapped_text()
