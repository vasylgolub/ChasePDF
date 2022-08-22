from .src.useful_funcs import *
from .src.pdf import Pdf


class HandleUploadedFile:
    def __init__(self, file):
        # transactions are list of objects: Extractor
        self.opened_pdf = Pdf(file)
        self.date_of_the_statement = self.opened_pdf.get_date_of_this_statement()

        total = 0
        for each_transaction in self.transactions:
            total += each_transaction.amount

        self.total_amount = round(total, 2)
