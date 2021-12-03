import re


class Withdrawals:
    def __init__(self, whole_text=None):
        if whole_text is not None:
            self.whole_long_text = whole_text
            # self.list = self.get_list_of_information_about_withdrawals_section()
            self.total_withdrawals_text = self.get_fixed_list_with_dates_positioned_properly()[-1].strip()
            self.list_of_transactions = self.get_fixed_list_with_dates_positioned_properly()[1:-1]
            self.total_withdrawals = self.get_total_from_this_string(self.total_withdrawals_text)

    # ---------------------------------work the $amount-----------------------------------------------------
    @staticmethod
    def get_total_from_this_string(string):
        dollar_sign_pos = string.find("$")
        str_num = string[dollar_sign_pos + 1:]
        str_num = str_num.replace(",", "")
        return float(str_num)

    # ------------------------------------------------------------------------------------------------
    def get_list_of_information_about_withdrawals_section(self):
        not_perfect_list = self.get_list_of_each_transaction_and_total()
        return self.remove_unnecessary_info_from_some_elements(not_perfect_list)

    def get_list_of_each_transaction_and_total(self):
        section_str = self.inline_based_on_key_words()
        return section_str.splitlines()

    def inline_based_on_key_words(self, section_str=None):
        if section_str is None:
            section_str = self.whole_long_text
        section_str = section_str.replace("Recurring Card Purchase", "\nRecurring Card Purchase")
        section_str = section_str.replace("Card Purchase", "\nCard Purchase")

        # little fix because both previous operations have "Purchase" word
        section_str = section_str.replace("Recurring \n", "Recurring ")

        section_str = section_str.replace("Total ATM & Debit Card Withdrawals", "\nTotal ATM & Debit Card Withdrawals")
        section_str = section_str.replace("ATM Withdrawal ", "\nATM Withdrawal ")
        section_str = section_str.replace("Payment Sent", "\nPayment Sent")
        section_str = section_str.replace("Non-Chase ATM Withdraw", "\nNon-Chase ATM Withdraw")
        return section_str

    #----------------------------------------
    def remove_unnecessary_info_from_some_elements(self, a_list):
        count_elements = len(a_list)
        for pos in range(0, count_elements - 1):  # Not till the last one

            if self.it_has_cash_back(a_list[pos]):
                cash_back_section_text = self.extract_cash_back_info(a_list[pos])
                a_list[pos] = a_list[pos].replace(cash_back_section_text, "")
                a_list[pos] = self.get_string_with_last_space_removed(a_list[pos])

            if self.does_have_unnecessary_long_text(a_list[pos]):
                a_list[pos] = self.get_lef_side_and_date_at_the_end(a_list[pos])

        if self.does_have_unnecessary_long_text(a_list[-1]):  # If last element has unnecessary text
            a_list[-1] = self.get_left_side_only(a_list[-1])

        return a_list
    #-----------------------------------------Fix Dates-------------------------------------------------------

    def get_fixed_list_with_dates_positioned_properly(self):
        result_list = []
        list_of_dates = self.extract_dates()
        length = len(self.get_list_of_information_about_withdrawals_section())
        for position in range(0, length):
            string = self.get_list_of_information_about_withdrawals_section()[position]
            new_string = list_of_dates[position] + " " + self.get_str_with_date_removed_at_the_end(string)
            result_list.append(new_string)
        return result_list


    def extract_dates(self):
        result_list = [""]  # Because the first element in list is a description
        for each in self.get_list_of_information_about_withdrawals_section():
            result_list.append(self.extract_date_at_the_end(each))
        return result_list

    #-----------------------------------Cash Back-------------------------------------------------------------
    @staticmethod
    def extract_cash_back_info(string):
        pattern = re.compile(r'Purchase \$?\d.+ Cash Back \$?\d\d\.\d\d')
        result = pattern.search(string)
        return result.group()

    def get_cash_back_position_and_info_text_about(self, a_list):
        count_elements = len(a_list)
        result = []
        for pos in range(0, count_elements - 1):
            if self.it_has_cash_back(a_list[pos]):
                result.append([pos, self.extract_cash_back_info(a_list[pos])])
        return result

#-------------------------------------------------DELEGATES---------------------------------------------------------#
    @staticmethod
    def get_string_with_last_space_removed(string):
        last_space_pos = string.rfind(" ")
        result = string[:last_space_pos] + string[last_space_pos+1:]
        return result

    @staticmethod
    def it_has_cash_back(string):
        return "Cash Back" in string

    @staticmethod
    def get_left_side_only(string):
        period_pos = string.find(".")
        return string[:period_pos+3]

    @staticmethod
    def does_have_unnecessary_long_text(string):
        return len(string) > 100

    def get_lef_side_and_date_at_the_end(self, string):
        end_position = self.get_end_position_of_target(string)
        last_5_chars = string[-5:]
        return string[: end_position] + last_5_chars

    @staticmethod
    def get_end_position_of_target(string):
        pattern = re.compile(r'\d\d\.\d\d')
        return pattern.search(string).end()

    def get_str_with_date_removed_at_the_end(self, string):
        if self.has_date_at_the_end(string):
            return string[:-5]
        return string

    def extract_date_at_the_end(self, string):
        if self.has_date_at_the_end(string):
            return string[-5:]
        return ""

    @staticmethod
    def has_date_at_the_end(string):
        last_5_chars = string[-5:]
        return last_5_chars.find("/") != -1
