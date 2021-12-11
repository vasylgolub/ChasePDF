import re


class WithdrawalsTextCleaner:
    def __init__(self, whole_text=None):
        if whole_text is not None:
            self.whole_text = whole_text
            self.list = self.make_whole_text_a_list_with_unnecessary_info_removed()

    def get_wrapped_text(self):
        return "\n".join(self.list)

    # ------------------------------------------------------------------------------------------------
    def make_whole_text_a_list_with_unnecessary_info_removed(self):
        result = self.get_fixed_list_with_dates_positioned_properly()
        result[0] = "ATM & DEBIT CARD WITHDRAWALS"
        result[-1] = result[-1].strip()
        return result

    def a_list_with_some_text_removed_but_not_with_dates_in_the_right_place(self):
        not_perfect_list = self.inline_based_on_key_words().splitlines()
        return self.remove_unnecessary_info_from_some_elements(not_perfect_list)

    def inline_based_on_key_words(self, section_str=None):
        if section_str is None:
            section_str = self.whole_text
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

    #-----------------------------------Cash Back-------------------------------------------------------------
    @staticmethod
    def extract_cash_back_info(string):
        pattern = re.compile(r'Purchase \$?\d.+ Cash Back \$?\d+\.\d\d')
        result = pattern.search(string)
        return result.group()

    def get_cash_back_position_and_info_text_about(self, a_list):
        count_elements = len(a_list)
        result = []
        for pos in range(0, count_elements - 1):
            if self.it_has_cash_back(a_list[pos]):
                result.append([pos, self.extract_cash_back_info(a_list[pos])])
        return result
    #-----------------------------------------Fix Dates-------------------------------------------------------

    def get_fixed_list_with_dates_positioned_properly(self):
        result_list = []
        list_of_dates = self.extract_dates()
        length = len(self.a_list_with_some_text_removed_but_not_with_dates_in_the_right_place())
        for position in range(0, length):
            string = self.a_list_with_some_text_removed_but_not_with_dates_in_the_right_place()[position]
            new_string = list_of_dates[position] + " " + self.get_str_with_date_removed_at_the_end(string)
            result_list.append(new_string)
        return result_list


    def extract_dates(self):
        result_list = [""]  # Because the first element in list is a description
        for each in self.a_list_with_some_text_removed_but_not_with_dates_in_the_right_place():
            result_list.append(self.extract_date_at_the_end(each))
        return result_list

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
        return len(string) > 200

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
