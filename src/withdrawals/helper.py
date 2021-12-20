import re


class Helper:
    @staticmethod
    def get_total_from_this_string(string):
        dollar_sign_pos = string.find("$")
        str_num = string[dollar_sign_pos + 1:]
        str_num = str_num.replace(",", "")
        return float(str_num)

    # -------------------------------International transactions-------------------------------------------------

    @staticmethod
    def get_string_without_Exchg_Rte_text(string):
        pattern = re.compile(r'Card \d{4} .+?\)')  # 4 digits used as reference point. Match till first occurrence of )
        result = pattern.search(string)
        extracted_exchange_rate_info = result.group()[10:]  # Card and 4 digits are then removed from string

        exchange_rate_sub_text = extracted_exchange_rate_info
        result = string.replace(exchange_rate_sub_text, "")  # Remove that subtext from string
        return result

    @staticmethod
    def get_string_with_last_space_char_removed(string):
        last_space_pos = string.rfind(" ")
        result = string[:last_space_pos] + string[last_space_pos + 1:]
        return result

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