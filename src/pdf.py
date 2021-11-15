from PyPDF2 import PdfFileReader
from colorama import Fore


class Pdf:
    def __init__(self, pdf_file_path):
        # let's save the path just in case
        self.file_path = pdf_file_path

        # The chase statement pdf document is broken down into these sections.
        # The header is not included.
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

        # Add the remaining text that wasn't added in the loop
        result = result + line

        return result.strip(" ")

    def get_document_header_text(self):
        till_desired_position = self.text.find("CHECKING SUMMARY")
        top_of_document = self.text[:till_desired_position]
        return top_of_document

    def get_text_with_sections_highlighted(self, text=None, words_to_highlight=None):
        if text is None:
            text = self.text

        if words_to_highlight is None:
            words_to_highlight = self.document_sections

        new_text = text
        for word in words_to_highlight:
            new_text = self.highlight_a_word_in_text(new_text, word)
        return new_text

    def get_text_of_desired_section(self, name_of_the_section):
        start = self.text.find(name_of_the_section)
        if name_of_the_section == self.document_sections[-1]:
            length_of_text = len(self.text)
            return self.text[start: length_of_text]
        index_of_next_section = self.document_sections.index(name_of_the_section) + 1
        next_section_name = self.document_sections[index_of_next_section]
        end = self.text.find(next_section_name)
        return self.text[start: end]

    def get_count_of_occurrences(self, target_str, text=None):
        if text is None:
            text = self.text
        return text.count(target_str)

    def get_text_to_show_what_sections_are(self):
        return self.get_text_with_sections_highlighted(self.get_text_in_paragraph_style(self.text))

    @staticmethod
    def is_file_a_pdf(file_path):
        return file_path[-4: len(file_path)] == ".pdf"

    @staticmethod
    def highlight_a_word_in_text(text, word):
        word_to_be_highlighted = "{}" + f"{word}" + "{}"
        return text.replace(word, word_to_be_highlighted.format(Fore.BLUE, Fore.RESET))
