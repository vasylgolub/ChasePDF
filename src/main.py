from src.pdf import Pdf
from PyPDF2 import PdfFileReader
from pathlib import Path
import os


file_path = "/Users/vasylgolub/Desktop/pdfs/2020/20200131-statements-7190-.pdf"
# path = os.path.abspath("../../pdfs/2020/20200131.pdf")

pdf_file_object = Pdf(file_path)
index = pdf_file_object.get_text().find('Pageof*start*atmdebitwithdrawal*end*')
index2 = pdf_file_object.get_text().find("Pageof*start*atmdebitwithdrawal")
txt = pdf_file_object.get_text()


arr = txt.split(" ")
txt2 = ""
for i in range(0, len(arr), 10):
    txt2 = txt2 + " ".join(arr[i: i+10])

print(txt)
print(txt2)

# Total ATM & Debit Card Withdrawals