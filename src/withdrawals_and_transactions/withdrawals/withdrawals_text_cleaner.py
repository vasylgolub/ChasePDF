import re
from src.withdrawals_and_transactions.helper import Helper


class WithdrawalsTextCleaner:
    def __init__(self, whole_text=None):
        if whole_text is not None:
            self.whole_text = whole_text
            # self.list = self.make_whole_text_a_list_with_unnecessary_info_removed()

            pos = self.whole_text.find("Total ATM & Debit Card Withdrawals")
            self.total_atm_and_debit_card__withdrawals_text = self.whole_text[pos:]
            whole_text_without_total = self.whole_text[:pos]

            text_without_title = \
                whole_text_without_total.replace("ATM & DEBIT CARD WITHDRAWALSDATEDESCRIPTIONAMOUNT", "")

            self.inlined_by_date = re.sub(r'(\d\d/\d\d)', "\n\\1", text_without_title)
            self.inlined_by_date = self.inlined_by_date.strip()

            a_list = self.inlined_by_date.split("\n")
            self.withdrawals = []
            for left, right in zip(a_list[0::2], a_list[1::2]):
                self.withdrawals.append(left + right)

            self.cleaned_withdrawals = self.remove_unnecessary_info_from_some_elements2(self.withdrawals)

    def get_wrapped_text(self):
        return "\n".join(self.cleaned_withdrawals)

    def remove_unnecessary_info_from_some_elements2(self, a_list):
        count_elements = len(a_list)
        for pos in range(0, count_elements):  # Not till the last one

            if self.it_has_cash_back(a_list[pos]):
                a_list[pos] = Helper.get_string_without_cash_back_text(a_list[pos])

            if self.it_has_Exchg_Rte(a_list[pos]):
                a_list[pos] = Helper.get_string_without_Exchg_Rte_text(a_list[pos])

            if self.does_have_unnecessary_long_text(a_list[pos]):
                a_list[pos] = self.get_text_without_unnecessary_long_sub_text(a_list[pos])

        if self.does_have_unnecessary_long_text(a_list[-1]):  # If last element has unnecessary text
            a_list[-1] = self.get_left_side_only(a_list[-1])

        return a_list

#-----------------------------------------------Delegating functions-----------------------------------------------#

    @staticmethod
    def it_has_cash_back(string):
        return "Cash Back" in string

    @staticmethod
    def it_has_Exchg_Rte(string):
        return "Exchg Rte" in string

    @staticmethod
    def get_left_side_only(string):
        period_pos = string.find(".")
        return string[:period_pos+3]

    @staticmethod
    def does_have_unnecessary_long_text(string):
        return len(string) > 200

    def get_text_without_unnecessary_long_sub_text(self, string):
        end_position = self.get_end_position_of_target(string)
        last_5_chars = string[-5:]
        return string[: end_position] + last_5_chars

    @staticmethod
    def get_end_position_of_target(string):
        pattern = re.compile(r'\d\d\.\d\d')
        return pattern.search(string).end()

    def extract_date_at_the_end(self, string):
        if self.has_date_at_the_end(string):
            return string[-5:]
        return ""

    @staticmethod
    def has_date_at_the_end(string):
        last_5_chars = string[-5:]
        return last_5_chars.find("/") != -1
