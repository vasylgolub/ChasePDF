from src.pdf import Pdf
import os




def is_path_correct():
    file_path = "/Users/vasylgolub/Desktop/pdfs/2020/20200131-statements-7190-.pdf"
    assert Pdf.is_path_correct(file_path) is True


# def check_if_array_of_words_is_correctly_split():
#     pass
