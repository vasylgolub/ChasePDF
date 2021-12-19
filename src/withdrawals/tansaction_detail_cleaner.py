import re


class TransactionCleaner:
    def __init__(self, whole_text=None):
        if whole_text is not None:
            self.whole_text = whole_text
            inline = self.inline_without_dates(self.whole_text)
            top, bottom, _ = self.split_in_3_sections(inline)
            self.top = self.clean_top(top)
            self.bottom = self.clean_bottom(bottom)


    def inline_without_dates(self, text=None):
        if text is None:
            text = self.whole_text
        in_lined_without_dates = re.sub(r'\d\d/\d\d', "\n", text)
        in_lined = in_lined_without_dates.replace("Ending Balance", "\nEnding Balance")  # little more inlining
        return in_lined

    def inline_and_clean(self, section_str=None):
        if section_str is None:
            section_str = self.whole_text
        list_dates = self.get_list_of_all_dates_in_text(section_str)
        in_lined = self.inline_without_dates(section_str)
        res_list = in_lined.split("\n")  # Let's make it a list

        top, bottom, res_list = self.split_in_3_sections(res_list)  # Split
        res_list = self.get_new_list_without_elements_with_long_unnecessary_text(res_list)
        res_list = self.strip_each_element(res_list)
        res_list = self.insert_each_date_in_front_of_each_element(list_dates, res_list)
        whole_text = self.put_together_type_info_with_related_store_info(res_list)
        list_res = self.remove_single_dates_and_get_list(whole_text)
        list_res = self.remove_balance_amount_from_each_transaction(list_res)

        list_res.append(self.clean_bottom(bottom))
        list_res.insert(0, self.clean_top(top))
        return list_res

    def put_together_type_info_with_related_store_info(self, a_list):
        list_of_types = ["Recurring Card Purchase", "Card Purchase", "Beginning Balance",
                         "Non-Chase ATM Withdraw", "ATM Withdrawal", "Payment Sent", "Foreign Exch"]
        inff = "Insufficient Funds Fee"
        res = ""
        for each_string in a_list:
            if self.any_element_of_this_list_is_in_this_string(list_of_types, each_string) and inff not in each_string:
                res += each_string + " "
                continue
            res += each_string + "\n"
        return res

    # ------------------------------------------------------------------------------------------------------------

    def remove_balance_amount_from_each_transaction(self, lista):
        res = []
        for each in lista:
            res.append(self.remove_balance_amount_from_transaction(each))
        return res

    @staticmethod
    def remove_balance_amount_from_transaction(string):
        pos_last_dot = string.rfind(".")
        res = string[:pos_last_dot]
        pos_last_dot = res.rfind(".")
        res = res[:pos_last_dot + 3]
        return res

    @staticmethod
    def clean_bottom(string):
        period_pos = string.find(".")
        return string[:period_pos + 3].replace("$", " ")

    @staticmethod
    def clean_top(string):
        pos_of = string.find("Beginning Balance")
        return string[pos_of:].replace("$", " ")

    @staticmethod
    def remove_single_dates_and_get_list(text):  # This function removes some dates.
        res = []
        for each in text.split("\n"):
            if len(each) < 6:  # if it is just a date
                continue
            res.append(each)
        return res

    @staticmethod
    def split_in_3_sections(a_list):
        if type(a_list) != type([]):  # if passed parameter is not a list then
            a_list = a_list.split("\n")  # Let's make it a list
        return a_list[0], a_list[-1], a_list[1:-1]

    @staticmethod
    def any_element_of_this_list_is_in_this_string(a_list, string):
        for each in a_list:
            if each in string:
                return True
        return False

    def get_new_list_without_elements_with_long_unnecessary_text(self, a_list):
        res = []
        for each in a_list:
            if self.does_have_unnecessary_long_text(each):
                res.append(self.remove_long_unnecessary_text(each))
                continue
            res.append(each)
        return res

    @staticmethod
    def strip_each_element(a_list):
        res = []
        for each in a_list:
            res.append(each.strip())
        return res

    @staticmethod
    def get_list_of_all_dates_in_text(string):
        pattern = re.compile(r'\d\d/\d\d')
        return pattern.findall(string)

    @staticmethod
    def insert_each_date_in_front_of_each_element(list_date, list_string):
        res = []
        for i in range(0, len(list_date)):
            res.append(list_date[i] + list_string[i])
        return res

    @staticmethod
    def remove_long_unnecessary_text(whole_string):
        pattern = re.compile(r'.+\d+\.\d{2}')
        res = pattern.search(whole_string)
        return res.group()

    @staticmethod
    def does_have_unnecessary_long_text(string):
        return len(string) > 200
