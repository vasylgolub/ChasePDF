from src.withdrawals_text_cleaner import WithdrawalsTextCleaner


class Withdrawals:
    def __init__(self, whole_text):
        cleaned_withdrawals_text = WithdrawalsTextCleaner(whole_text)
        self.whole_text = whole_text
        self.whole_text_wrapped = cleaned_withdrawals_text.get_wrapped_text()
        self.title = self.whole_text_wrapped[:self.whole_text_wrapped.find("\n")]
        self.list_of_transactions = cleaned_withdrawals_text.list_format_of_whole_text[1:-1]

        total_withdrawals_text = cleaned_withdrawals_text.list_format_of_whole_text[-1]
        self.total_withdrawals = {"text": total_withdrawals_text,
                                  "amount": self.get_total_from_this_string(total_withdrawals_text)}

    @staticmethod
    def get_total_from_this_string(string):
        dollar_sign_pos = string.find("$")
        str_num = string[dollar_sign_pos + 1:]
        str_num = str_num.replace(",", "")
        return float(str_num)
