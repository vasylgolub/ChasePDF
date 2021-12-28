import re
from src.withdrawals_and_transactions.helper import Helper


class TransactionCleaner:
    def __init__(self, whole_text=None):
        if whole_text is not None:
            self.whole_text = whole_text
            inline = self.substitute_dates_with_new_lines(self.whole_text)
            inline = inline.replace("Ending Balance", "\nEnding Balance")  # little more inlining

            top, bottom, middle = self.split_in_3_sections(inline)
            self.beginning_balance = self.clean_top(top)
            self.ending_balance = self.clean_bottom(bottom)

            self.transactions = self.get_new_list_without_elements_with_long_unnecessary_text(middle)  # Cleaning
            self.transactions = self.strip_each_element(self.transactions)  # Cleaning
            self.transactions = self.insert_each_date_in_front_of_each_el(self.transactions)  # Reassembling

            text = self.put_together_type_info_with_related_store_info(self.transactions)  # Make it a string again

            self.transactions = self.remove_single_dates_and_get_list(text)  # Remove single dd/dd
            self.transactions = self.detach_balance_amount_from_each_transaction(self.transactions)

            self.balances = self.get_balances_from_transactions()
            # self.transactions = self.remove_balance_amount_from_transaction()



            # self.transactions = self.get_clean_transactions_in_list_format(self.whole_text)
            # self.put_space_before_amount_in_each_transaction()

            # # Extract (Exchg Rte) detail txt
            # for transaction in self.transactions:
            #     pos_el = self.transactions.index(transaction)
            #     if self.string_matches_pattern(r'Card \d{4} .+?\)', transaction):
            #         self.transactions[pos_el] = Helper.get_string_without_Exchg_Rte_text(transaction)
            #
            # # Extract Cash Back detail txt
            # for transaction in self.transactions:
            #     pos_el = self.transactions.index(transaction)
            #     if self.string_matches_pattern(r'Purchase \$?\d.+ Cash Back \$?\d+\.\d\d', transaction):
            #         self.transactions[pos_el] = Helper.get_string_without_cash_back_text(transaction)
            #
            # # Put space before -d+.dd
            # for transaction in self.transactions:
            #     pos_el = self.transactions.index(transaction)
            #     if self.string_matches_pattern(r'-\d+.\d\d$', transaction):
            #         self.transactions[pos_el] = Helper.get_string_with_space_before_deduction_amount(transaction)
            #
            # # Remove two spaces
            # new_list = []
            # for transaction in self.transactions:
            #     new_str = transaction.replace("   ", " ")
            #     new_str = new_str.replace("  ", " ")
            #     new_list.append(new_str)
            #
            # self.transactions = new_list
            #
            # self.list = [self.top] + self.transactions + [self.bottom]

    # def get_wrapped_text(self):
    #     return "\n".join(self.list)


    def get_balances_from_transactions(self, transactions=None):
        if transactions is None:
            transactions = self.transactions
        res = []
        for transaction in transactions:
            res.append(transaction[transaction.rfind(" "):])
        return res

    def put_together_type_info_with_related_store_info(self, a_list):
        list_of_types = ["Recurring Card Purchase", "Card Purchase", "Beginning Balance",
                         "Non-Chase ATM Withdraw", "ATM Withdrawal", "Payment Sent", "Foreign Exch",
                         "Payment Received", "Check Deposit"]
        inff = "Insufficient Funds Fee"
        res = ""
        for each_string in a_list:
            if self.any_element_of_this_list_is_in_this_string(list_of_types, each_string) and inff not in each_string:
                res += each_string + " "
                continue
            res += each_string + "\n"
        return res

    @staticmethod
    def string_matches_pattern(pattern_str, string):
        pattern = re.compile(pattern_str)
        found = pattern.search(string)
        return bool(found)

    @staticmethod
    def put_space(pattern, transaction_string):
        pattern = re.compile(pattern)
        found = pattern.search(transaction_string)
        string = found.group()
        return transaction_string.replace(string, string + " ")
    # ------------------------------------------------------------------------------------------------------------

    def substitute_dates_with_new_lines(self, text=None):
        if text is None:
            text = self.whole_text
        res = re.sub(r'\d\d/\d\d', "\n", text)
        return res

    def detach_balance_amount_from_each_transaction(self, lista):
        res = []
        for each in lista:
            without_balance = self.remove_balance_amount_from_transaction(each)
            balance = each.replace(without_balance, "")
            res.append(self.remove_balance_amount_from_transaction(each) + " " + balance)
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
    def split_in_3_sections(a_list):
        if type(a_list) != type([]):  # if passed parameter is not a list then
            a_list = a_list.split("\n")  # Let's make it a list
        return a_list[0], a_list[-1], a_list[1:-1]

    @staticmethod
    def remove_single_dates_and_get_list(text):  # This function removes some dates.
        res = []
        for each in text.split("\n"):
            if len(each) < 6:  # if it is just a date
                continue
            res.append(each)
        return res

    @staticmethod
    def any_element_of_this_list_is_in_this_string(a_list, string):
        for each in a_list:
            if each in string:
                return True
        return False

    # Remove text that is present on every new page.
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

    def insert_each_date_in_front_of_each_el(self, list_string):
        res = []
        list_date = self.get_list_of_all_dates_in_text(self.whole_text)
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
    # ------------------------------------------------------------------------------------------------------------

    @staticmethod
    def make_it_in_textual_format(amount) -> str:
        amount = round(amount * 100)
        amount_str = str(amount)
        right_side = amount_str[-2:]  # Decimal
        left_side = amount_str[:-2]

        if len(left_side) > 3:
            left_side = left_side.replace(left_side[-3:], "," + left_side[-3:])  # Ex: 1324 -> 1,324

        return left_side + "." + right_side
