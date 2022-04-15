from .src.useful_funcs import *


class HandleUploadedFile:
    def __init__(self, file):
        self.transactions = get_transactions_from_file(file)
