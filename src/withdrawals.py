import re


class Withdrawals:
    def __init__(self, withdrawal_text_section):
        self.withdrawal_text_section = withdrawal_text_section

    def put_inline_each_transaction_and_total(self):
        section_str = self.withdrawal_text_section
        section_str = section_str.replace("Recurring Card Purchase", "\nRecurring Card Purchase")
        section_str = section_str.replace("Card Purchase", "\nCard Purchase")
        section_str = section_str.replace("Recurring \n", "Recurring ")
        section_str = section_str.replace("Total ATM & Debit Card Withdrawals", "\nTotal ATM & Debit Card Withdrawals")
        section_str = section_str.replace("ATM Withdrawal ", "\nATM Withdrawal ")
        section_str = section_str.replace("Payment Sent", "\nPayment Sent")
        section_str = section_str.replace("Non-Chase ATM Withdraw", "\nNon-Chase ATM Withdraw")
        return self.get_a_list_format(section_str)

    @staticmethod
    def get_a_list_format(text):
        return text.splitlines()