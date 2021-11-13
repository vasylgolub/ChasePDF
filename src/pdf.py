from PyPDF2 import PdfFileReader


class Pdf:
    def __init__(self, pdf_file_path):
        # let's save the path just in case
        self.file_path = pdf_file_path

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

    def get_text(self):
        return self.text

    @staticmethod
    def is_file_a_pdf(file_path):
        return file_path[-4: len(file_path)] == ".pdf"

