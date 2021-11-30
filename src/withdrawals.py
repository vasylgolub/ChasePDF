import re


class Withdrawals:
    def __init__(self, withdrawal_text_section):
        self.withdrawal_text_section = withdrawal_text_section
        self.list = self.get_list_of_information_about_withdrawals()
        self.list = self.get_new_fixed_list()

    # ------------------------------------------------------------------------------------------------
    def get_list_of_information_about_withdrawals(self):
        return self.get_cleaner_list()

    def get_cleaner_list(self):
        not_perfect_list = self.get_list_of_each_transaction_and_total()
        return self.remove_unnecessary_info_from_some_elements(not_perfect_list)

    def get_list_of_each_transaction_and_total(self):
        section_str = self.inline_based_on_key_words(self.withdrawal_text_section)
        return section_str.splitlines()

    @staticmethod
    def inline_based_on_key_words(section_str):
        section_str = section_str.replace("Recurring Card Purchase", "\nRecurring Card Purchase")
        section_str = section_str.replace("Card Purchase", "\nCard Purchase")

        # little fix because both previous operations have "Purchase" word
        section_str = section_str.replace("Recurring \n", "Recurring ")

        section_str = section_str.replace("Total ATM & Debit Card Withdrawals", "\nTotal ATM & Debit Card Withdrawals")
        section_str = section_str.replace("ATM Withdrawal ", "\nATM Withdrawal ")
        section_str = section_str.replace("Payment Sent", "\nPayment Sent")
        section_str = section_str.replace("Non-Chase ATM Withdraw", "\nNon-Chase ATM Withdraw")
        return section_str

    #------------------------------------------------------------------------------------------------
    def remove_unnecessary_info_from_some_elements(self, a_list):
        count_elements = len(a_list)
        for position in range(0, count_elements):
            it_has_unnecessary_long_text = len(a_list[position]) > 100
            if it_has_unnecessary_long_text:
                a_list[position] = self.get_lef_side_and_date_at_the_end(a_list[position])
        return a_list

    @staticmethod
    def get_left_side_only(string):
        period_pos = string.find(".")
        return string[:period_pos+3]

    # Delegate
    @staticmethod
    def does_have_unnecessary_long_text(string):
        return len(string) > 100

    # Delegate
    def get_lef_side_and_date_at_the_end(self, string):
        end_position = self.get_end_position_of_target(string)
        last_5_chars = string[-5:]
        return string[: end_position] + last_5_chars

    # def get_unnecessary_text(self, string):
    #     end_position = self.get_end_position_of_target(string)
    #     return string[end_position: -5]

    @staticmethod
    def get_end_position_of_target(string):
        pattern = re.compile(r'\d\d\.\d\d')
        return pattern.search(string).end()
    #------------------------------------------------------------------------------------------------

    def get_new_fixed_list(self):
        result_list = []
        list_of_dates = self.get_list_of_last_position_dates()
        length = len(self.list)
        for position in range(0, length):
            string = self.list[position]
            new_string = list_of_dates[position] + " " + self.get_str_with_date_removed_at_the_end(string)
            result_list.append(new_string)
        return result_list


    def get_list_of_last_position_dates(self):
        result_list = [""]  # Because the first element in list is a description
        for each in self.list:
            result_list.append(self.extract_date_at_the_end(each))
        return result_list

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
