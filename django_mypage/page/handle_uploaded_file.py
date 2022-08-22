from .src.useful_funcs import *
from .src.pdf import Pdf


class HandleUploadedFile:
    def __init__(self, file):
        # transactions are list of objects: Extractor
        self.opened_pdf = Pdf(file)
        self.date_of_the_statement = self.opened_pdf.get_date_of_this_statement()


    def get_transactions(self):
        result = []
        list_of_transactions_in_string = self.opened_pdf.get_withdrawals().list_of_withdrawals
        for transaction_string in list_of_transactions_in_string:
            extractor_of_each_field = Extractor(transaction_string)
            result.append(extractor_of_each_field)
        return result
