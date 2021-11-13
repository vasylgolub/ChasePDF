from src.pdf import Pdf

file_path = "/Users/vasylgolub/Desktop/pdfs/2020/20200131-statements-7190-.pdf"


def test_is_path_correct():
    assert Pdf.is_file_a_pdf(file_path) is True

# def check_if_array_of_words_is_correctly_split():
#     pass
