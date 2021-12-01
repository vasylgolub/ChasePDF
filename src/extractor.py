import re

class Extractor:
    def __init__(self, source_text):
        self.whole_text = source_text
        self.amount = self.get_amount(self.whole_text)
        self.type = self.get_type_withdrawal(self.whole_text)


    @staticmethod
    def get_amount(string):
        last_space_pos = string.rfind(" ")
        right_side_string = string[last_space_pos+1:][4:]  # get right side + remove the first 4 digits
        if '$' in right_side_string:
            right_side_string = right_side_string.replace('$', "")
        return float(right_side_string)

    @staticmethod
    def get_type_withdrawal(string):
        pattern = re.compile(r'\d\d/\d\d\ ?(.*?)\ ?\d\d/\d\d')
        result = pattern.search(string)
        return result.groups()[0]

