from src.pdf import Pdf

file_path = "/Users/vasylgolub/Desktop/pdfs/2020/20200131-statements-7190-.pdf"


def test_is_path_correct():
    assert Pdf.is_file_a_pdf(file_path) is True


def test_if_the_paragraph_didnt_loose_any_chars():
    my_pdf = Pdf(file_path)
    original_text = my_pdf.text.strip(" ")
    text_from_paragraph = my_pdf.get_text_in_paragraph()
    text_from_paragraph_joined = "".join(text_from_paragraph.split("\n"))
    assert original_text == text_from_paragraph_joined
