class WithdrawalsHelper:
    @staticmethod
    def get_total_from_this_string(string):
        dollar_sign_pos = string.find("$")
        str_num = string[dollar_sign_pos + 1:]
        str_num = str_num.replace(",", "")
        return float(str_num)