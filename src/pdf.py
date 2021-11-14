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


    def get_text_in_paragraph_style(self, txt=None):
        if txt is None:
            txt = self.text

        array_of_strings = txt.split(" ")
        result = ""
        line = ""

        for string in array_of_strings:
            line = line + " " + string
            if len(line) > 100:
                result = result + line + "\n"
                line = ""
        result = result + line
        return result.strip(" ")

    def get_document_header(self):
        till_desired_position = self.text.find("CHECKING SUMMARY")
        top_of_document = self.text[:till_desired_position]
        return self.get_text_in_paragraph_style(top_of_document)

    def get_text_with_sections_highlighted(self):
        new_text = self.text
        for each in self.document_sections:
            new_text = self.highlight_a_word_in_text(new_text, each)
        return new_text

    @staticmethod
    def is_file_a_pdf(file_path):
        return file_path[-4: len(file_path)] == ".pdf"

    @staticmethod
    def highlight_a_word_in_text(text, word):
        colored_word = "{}" + f"{word}" + "{}"
        return text.replace(word, colored_word.format(Fore.BLUE, Fore.RESET))