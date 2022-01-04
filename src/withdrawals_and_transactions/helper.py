import re


class Helper:
    @staticmethod
    def get_float_format(string):
        dollar_sign_pos = string.find("$")
        str_num = string[dollar_sign_pos + 1:]  # exclude dollar sign
        str_num = str_num.replace(",", "")  # remove comma sign
        return float(str_num)

    @staticmethod
    def get_text_and_amount_separated(string):
        pos_last_space = string.rfind(" ")
        text = string[:pos_last_space]
        amount = string[pos_last_space+1:]
        return text, amount

    @staticmethod
    def get_beginning_balance_as_dictionary(whole_text_wrapped):
        beginning_balance_whole_text = whole_text_wrapped[:whole_text_wrapped.find("\n")]  # take only the top
        bb_text, bb_amount = Helper.get_text_and_amount_separated(beginning_balance_whole_text)  # BeginningBalance
        return {bb_text: float(bb_amount.replace(',', ''))}

    @staticmethod
    def get_ending_balance_as_dictionary(whole_text_wrapped):
        ending_balance_whole_text = whole_text_wrapped[whole_text_wrapped.rfind("\n")+1:]  # take only the bottom
        eb_text, eb_amount = Helper.get_text_and_amount_separated(ending_balance_whole_text)  # Ending_balance
        return {eb_text: float(eb_amount.replace(',', ''))}  # In case there is a comma

    #---------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_sum_of_all_transactions(transaction_list):
        res = 0
        for transaction in transaction_list:
            _, str_amount = Helper.get_text_and_amount_separated(transaction)
            res += round(Helper.get_float_format(str_amount) * 100)
        return res/100


    # -------------------------------International transactions-------------------------------------------------

    @staticmethod
    def get_string_without_Exchg_Rte_text(string):
        exchange_rate_sub_text = Helper.extract_exchange_rate_info(string)
        result = string.replace(exchange_rate_sub_text, "")  # Remove that subtext from string
        return result

    @staticmethod
    def extract_exchange_rate_info(string):
        pattern = re.compile(r'Card \d{4} .+?\)')  # 4 digits used as reference point. Match till first occurrence of )
        result = pattern.search(string)
        return result.group()[10:]  # Card and 4 digits are then removed from string

    # @staticmethod
    # def get_string_with_last_space_char_removed(string):
    #     last_space_pos = string.rfind(" ")
    #     result = string[:last_space_pos] + string[last_space_pos + 1:]
    #     return result
    #-----------------------------------Cash Back-------------------------------------------------------------
    @staticmethod
    def get_string_without_cash_back_text(string):
        cash_back_section_text = Helper.extract_cash_back_info(string)
        result = string.replace(cash_back_section_text, "")
        # return Helper.get_string_with_last_space_char_removed(result)  # Documentation: 1.0
        return result

    @staticmethod
    def extract_cash_back_info(string):
        pattern = re.compile(r'Purchase \$?\d.+ Cash Back \$?\d+\.\d\d')
        result = pattern.search(string)
        return result.group()
    #---------------------------------------------------------------------------------------------------------

    @staticmethod
    def extract_this_pattern(pattern, string):
        pattern = re.compile(pattern)
        result = pattern.search(string)
        return result.group()

    @staticmethod
    def get_string_with_space_before_deduction_amount(string):
        negative_amount = Helper.get_amount_string(string)
        result = string.replace(negative_amount, " " + negative_amount)
        return result

    @staticmethod
    def get_amount_string(string):
        pattern = re.compile(r'-\d+.\d\d$')
        result = pattern.search(string)
        return result.group()
