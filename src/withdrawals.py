import re


class Withdrawals:
    def __init__(self, withdrawal_text_section):
        self.withdrawal_text_section = withdrawal_text_section

    def get_transactions_list(self):
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
        section_str = section_str.replace("Recurring \n", "Recurring ")
        section_str = section_str.replace("Total ATM & Debit Card Withdrawals", "\nTotal ATM & Debit Card Withdrawals")
        section_str = section_str.replace("ATM Withdrawal ", "\nATM Withdrawal ")
        section_str = section_str.replace("Payment Sent", "\nPayment Sent")
        section_str = section_str.replace("Non-Chase ATM Withdraw", "\nNon-Chase ATM Withdraw")
        return section_str

    def remove_unnecessary_info_from_some_elements(self, a_list):
        count_elements = len(a_list)
        for position in range(0, count_elements):
            it_has_unnecessary_long_text = len(a_list[position]) > 100
            if it_has_unnecessary_long_text:
                a_list[position] = self.get_lef_side_and_date_at_the_end(a_list[position])
        return a_list

    # Delegate
    @staticmethod
    def get_lef_side_and_date_at_the_end(string):
        pattern = re.compile(r'\d\d\.\d\d')
        match = pattern.search(string)
        last_five_chars = string[-5:]
        return string[: match.end()] + last_five_chars

    # Delegate
    @staticmethod
    def get_unnecessary_text(string):
        pattern = re.compile(r'\d\d\.\d\d')
        match = pattern.search(string)
        return string[match.end(): -5]
