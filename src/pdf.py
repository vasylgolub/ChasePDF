from PyPDF2 import PdfFileReader
from colorama import Fore


class Pdf:
    def __init__(self, pdf_file_path):
        # let's save the path just in case
        self.file_path = pdf_file_path

        # The chase statement pdf document is broken down into these sections, called:
        self.document_sections = ["CHECKING SUMMARY",
                                  "DEPOSITS AND ADDITIONS",
                                  "ATM & DEBIT CARD WITHDRAWALS",
                                  "ATM & DEBIT CARD SUMMARY",
                                  "ELECTRONIC WITHDRAWAL",
                                  "FEES",
                                  "DAILY ENDING BALANCE",
                                  "SERVICE CHARGE SUMMARY"]

        opened_file = open(pdf_file_path, 'rb')
        read_pdf_file = PdfFileReader(opened_file)
        if read_pdf_file.isEncrypted:
            read_pdf_file.decrypt("")

        self.text = ''
        # go through each page and extract text
        for i in range(0, read_pdf_file.numPages):
            # creating a page object
            page = read_pdf_file.getPage(i)
            # extracting text from page
            self.text = self.text + " " + page.extractText()
        opened_file.close()


    def get_text_in_paragraph(self):
        array_of_strings = self.text.split(" ")
        result = ""
        line = ""

        for string in array_of_strings:
            line = line + " " + string
            if len(line) > 100:
                result = result + line + "\n"
                line = ""
        result = result + line
        return result.strip(" ")

    @staticmethod
    def is_file_a_pdf(file_path):
        return file_path[-4: len(file_path)] == ".pdf"

