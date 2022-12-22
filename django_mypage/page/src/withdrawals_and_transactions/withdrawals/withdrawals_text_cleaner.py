import re
from ..helper import Helper


class WithdrawalsTextCleaner:
    def __init__(self, whole_text=None):
        if whole_text is not None:
            self.whole_text = whole_text

            self.total_info = self.get_total_info_from_whole_text("Total ATM & Debit Card Withdrawals")
            whole_text_without_total = self.remove_total_info_from_whole_text()  # And everything that is after it.
            whole_text_without_total_and_title = \
                whole_text_without_total.replace("ATM & DEBIT CARD WITHDRAWALSDATEDESCRIPTIONAMOUNT", "")

            self.inlined_by_date = re.sub(r'(\d\d/\d\d)(?!\d)', "\n\\1", whole_text_without_total_and_title).strip()
            a_list = self.inlined_by_date.split("\n")
            self.withdrawals = []
            for left, right in zip(a_list[0::2], a_list[1::2]):
                self.withdrawals.append(left + right)

            cleaned_withdrawals = self.remove_unnecessary_info_from_some_elements(self.withdrawals)
            self.cleaned_withdrawals = self.add_space_after_4_digit_card(cleaned_withdrawals)
    # ------------------------------------------------------------------------------------------------------

    @staticmethod
    def add_space_after_4_digit_card(withdrawals):
        res = []
        for each in withdrawals:
            res.append(re.sub(r'(Card ?\d{4})', "\\1 ", each))
        return res


    def get_total_info_from_whole_text(self, tot_info_text):
        pos = self.whole_text.find(tot_info_text)
        res = self.whole_text[pos:]
        if self.does_have_unnecessary_long_text(res):
            pos_period = res.find('.')
            res = res[:pos_period + 3]
        return res

    def remove_total_info_from_whole_text(self):
        pos = self.whole_text.find("Total ATM & Debit Card Withdrawals")
        return self.whole_text[:pos]
    # ------------------------------------------------------------------------------------------------------

    def get_wrapped_text(self):
        return "\n".join(self.cleaned_withdrawals)

    def remove_unnecessary_info_from_some_elements(self, a_list):
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
        return string[: end_position]

    @staticmethod
    def get_end_position_of_target(string):
        pattern = re.compile(r'\d?\d\.\d\d')
        return pattern.search(string).end()

