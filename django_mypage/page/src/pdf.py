from PyPDF2 import PdfFileReader
from colorama import Fore
import textwrap
import os
from .withdrawals_and_transactions.withdrawals.withdrawals import Withdrawals
from .withdrawals_and_transactions.transactions.transaction_detail import TransactionDetail

# This class is supposed to work on a Chase Bank statement in pdf format.
# A bank statement is a list of all transactions for a bank account over a set period, usually monthly.


class Pdf:
    def __init__(self, pdf_file_path, is_personal_account=False):
        # let's save the path just in case

        if isinstance(pdf_file_path, str):  # If it is a string then it is probably a path to the file
            self.file_full_path = pdf_file_path
            self.file_name = os.path.basename(self.file_full_path)
            opened_file = open(pdf_file_path, 'rb')
        else:
            opened_file = pdf_file_path.open()  # it's actually not a path to a file. It is a file.

        # opened_file = open(pdf_file_path, 'rb')
        read_pdf_file = PdfFileReader(opened_file)
        if read_pdf_file.isEncrypted:
            read_pdf_file.decrypt("")

        self.text = ''
        # go through each page and extract text
        for n in range(0, read_pdf_file.numPages):
            # creating a page object
            page = read_pdf_file.getPage(n)
            # extracting text from page
            self.text = self.text + " " + page.extractText()
        self.text_length = len(self.text)
        opened_file.close()

        # The chase statement pdf document is broken down into these sections.
        # The header is not included.
        self.document_sections = ["CHECKING SUMMARY",
                                  "DEPOSITS AND ADDITIONS",
                                  "CHECKS PAID",
                                  "ATM & DEBIT CARD WITHDRAWALS",
                                  "ATM & DEBIT CARD SUMMARY",
                                  "ELECTRONIC WITHDRAWALS",
                                  "OTHER WITHDRAWALS",
                                  "FEES",
                                  "DAILY ENDING BALANCE",
                                  "SERVICE CHARGE SUMMARY"]
        if is_personal_account:
            self.document_sections = ["CHECKING SUMMARY",
                                      "TRANSACTION DETAIL",
                                      "OVERDRAFT AND RETURNED ITEM FEE SUMMARY"]

        self.remove_sections_not_in_the_text()  # from document_sections

    # ----------------------------------------------------------------------------------------------------------------
    # Gate to Withdrawals class methods. This functions is related to only withdrawals info.
    def get_withdrawals(self):
        withdrawals_section = self.get_desired_section("ATM & DEBIT CARD WITHDRAWALS")
        return Withdrawals(withdrawals_section)

    # Gate to TransactionDetail class methods. This functions is related to only transaction details info in personal
    # bank account.
    def get_transaction_detail(self):
        transaction_detail_section = self.get_desired_section("TRANSACTION DETAIL")
        return TransactionDetail(transaction_detail_section)
    # ----------------------------------------------------------------------------------------------------------------

    def get_date_of_this_statement(self, text=None):
        # The header has the information regarding the statement's date.
        if text is None:
            text = self.get_header_text()
        # We cut the text till word "through".
        cut_text = text[:text.find("through")]
        months = ['January', 'February', 'March', 'April', 'May',
                  'June', 'July', 'August', 'September', 'October', 'November', 'December']
        index_of_month = 0
        for month in months:
            index_of_month = cut_text.find(month)
            if index_of_month >= 0:
                break
        # We also strip the spaces if those are present in the string
        return cut_text[index_of_month:].strip()

    # For example: sometimes the pdf file doesn't have "CHECKS PAID" section.
    def remove_sections_not_in_the_text(self):
        for i in self.document_sections:
            if i not in self.text:
                self.document_sections.remove(i)

    def get_wrapped_text(self, lines=100, txt=None):
        if txt is None:
            txt = self.text
        return textwrap.fill(txt, lines)

    def get_wrapped_and_highlighted_text(self):
        top = self.get_wrapped_text(115, self.get_header_text())
        body = ""
        for section in self.document_sections:
            desired_section = self.get_desired_section(section)
            wrapped = self.get_wrapped_text(115, desired_section)
            body += self.get_text_with_sections_highlighted(wrapped) + "\n"
        return top + "\n" + body

    def get_header_text(self):
        till_desired_position = self.text.find("CHECKING SUMMARY")
        top_of_document = self.text[:till_desired_position]
        return top_of_document

# ------------------------------------highlighting-----------------------------------------------------------
    def get_text_with_sections_highlighted(self, text=None, sections_to_highlight=None):
        # Default text value is class' text variable: self.text
        if text is None:
            text = self.text
        whole_text = text
        if sections_to_highlight is None:
            sections_to_highlight = self.document_sections
        for section in sections_to_highlight:
            whole_text = self.highlight_in_text(whole_text, section)
        return whole_text


    @staticmethod
    def highlight_in_text(whole_text, text, how_many=1):
        highlighted_words = ""
        for word in text:
            highlighted_words += f"{Fore.BLUE}{word}{Fore.RESET}"
        return whole_text.replace(text, highlighted_words, how_many)
# ------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_sides_of_text(whole_text, middle_text):
        index = whole_text.find(middle_text)
        return whole_text[:index], whole_text[index + len(middle_text):]

    def get_desired_section(self, name_of_the_section):
        start = self.text.find(name_of_the_section)

        # If we want to get the "SERVICE CHARGE SUMMARY" (business bank account only) section,
        # then get text from that point till end of whole text
        if name_of_the_section == self.document_sections[-1]:
            return self.text[start: self.text_length]
        index_of_next_section = self.document_sections.index(name_of_the_section) + 1
        next_section_name = self.document_sections[index_of_next_section]
        end = self.text.find(next_section_name)
        return self.text[start: end]

    def get_count_of_occurrences(self, target_str, text=None):
        if text is None:
            text = self.text
        return text.count(target_str)

    def get_text_to_show_what_sections_are(self):
        return self.get_text_with_sections_highlighted(self.get_wrapped_text(self.text))

    @staticmethod
    def is_file_a_pdf(file_path):
        return file_path[-4: len(file_path)] == ".pdf"
