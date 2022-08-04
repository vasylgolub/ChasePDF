from .src.useful_funcs import *


class HandleUploadedFile:
    def __init__(self, file):
        # transactions are list of objects: Extractor
        self.transactions = get_transactions_from_file(file)

        total = 0
        for each_transaction in self.transactions:
            total += each_transaction.amount

        self.total_amount = round(total, 2)
