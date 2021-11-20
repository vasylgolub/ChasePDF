import os
from src.pdf import Pdf


class FileRename:
    def __init__(self, file_path):
        self.file_full_path = file_path
        self.file_name = os.path.basename(self.file_full_path)
        self.file_date = self.extract_date_from_file_pdf()

    def extract_date_from_file_pdf(self):
        the_pdf = Pdf(self.file_full_path)
        date = the_pdf.get_date_of_this_statement()
        return date
