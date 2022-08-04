import re

# This class is used to extract substrings from a text that has all the info regarding a certain transaction.
# Check unit tests to see some examples.


class Extractor:
    def __init__(self, source_text):
        self.whole_text = source_text
        self.amount = self.get_amount(self.whole_text)
        # self.type = self.get_type_withdrawal(self.whole_text)
        self.date = self.get_date(self.whole_text)
        self.last_4_digits = self.get_card_last_4_digits(self.whole_text)
        self.store = self.get_store(self.whole_text)

    def get_amount(self, string=None):
        if string is None:
            string = self.whole_text

        right_side_string = string[string.rfind(" "):]

        if "Card" in right_side_string:
            right_side_string = right_side_string.replace("Card", "")

        card_4_digits = self.get_card_last_4_digits(string)
        if card_4_digits in string:
            right_side_string = right_side_string.replace(card_4_digits, "")
            # pos_card_4_digits = right_side_string.index(card_4_digits)
            # right_side_string = right_side_string[pos_card_4_digits+4:]

        if '$' in right_side_string:
            pos_dollar_sign = right_side_string.index("$")
            right_side_string = right_side_string[pos_dollar_sign+1:]

        if "," in right_side_string:
            right_side_string = right_side_string.replace(",", "")

        return float(right_side_string)

    @staticmethod
    def get_type_withdrawal(string):
        pattern = re.compile(r'\d\d/\d\d ?(.*?) ?\d\d/\d\d')
        result = pattern.search(string)
        return result.groups()[0]

    @staticmethod
    def get_date(string):
        pattern = re.compile(r'\d\d/\d\d')
        matches = pattern.finditer(string)
        result = []
        for match in matches:
            result.append(match.group())

        # If the result has only one element, that means in transaction description text there is only one date: dd/dd.
        # The returning result better have always two elements in it. So the second will be just "0" maybe. For now.
        if len(result) == 1:
            result.append("0")
        return result

    @staticmethod
    def get_card_last_4_digits(string):
        pattern = re.compile(r'Card ?\d\d\d\d')
        matches = pattern.search(string)
        if bool(matches):
            return matches.group()[-4:]
        return "0000"  # Meaning that there is no 4 digit card number in the description.

    def get_store(self, string):
        pos_4_digits = string.rfind(self.last_4_digits)
        pos_second_date = string.rfind(self.date[1])
        end = pos_4_digits
        if "Card" in string:
            end = end - 5
        return string[pos_second_date+5: end].strip()
