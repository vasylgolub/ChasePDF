from src.pdf import Pdf
from src.list_of_files_from_directory import ListOfFilesFromDirectory

file_path = "/Users/vasylgolub/Desktop/pdfs/2020/20200131-statements-7190-.pdf"
my_pdf = Pdf(file_path)
my_list_of_files = ListOfFilesFromDirectory("")


def test_is_path_correct():
    assert Pdf.is_file_a_pdf(file_path) is True


def test_if_the_paragraph_doesnt_loose_any_chars_when_selecting_the_header():
    original_text = my_pdf.text
    result = my_pdf.get_header_text()
    for i in my_pdf.document_sections:
        result += my_pdf.get_desired_section(i)
    assert original_text == result


# Instead of comparing text to text, we just compare
# the length size of original text with the sum of
# text of each section extracted from the original text.
# This is just to see if extraction is accurate.
def test_if_extraction_is_accurate():
    whole_text_len = len(my_pdf.text)

    # We start by adding header's text length
    all_sections_len = len(my_pdf.get_header_text())

    # length of other sections put together
    for each in my_pdf.document_sections:
        section = my_pdf.get_desired_section(each)
        all_sections_len += len(section)

    assert whole_text_len == all_sections_len


def test_if_returns_desired_text_for_count_of_occurrences():
    result = my_pdf.get_desired_section("CHECKING SUMMARY")
    expected_result = "CHECKING SUMMARY Chase Total Business CheckingINSTANCESAMOUNTBeginning " \
                      "Balance$7,501.88Deposits and Additions114,462.51ATM & Debit " \
                      "Card Withdrawals134-6,896.00Electronic " \
                      "Withdrawals5-657.61Fees4-21.10Ending Balance154$4,389.68"
    assert result == expected_result


def test_if_all_sections_are_present_in_the_document():
    result = True
    # example: True and True and False and True: will give False value at the end to result variable
    for each in my_pdf.document_sections:
        is_it_present_in_text = my_pdf.text.find(each) != -1
        result = result and is_it_present_in_text
    assert result


def test_count_of_occurrences():
    test_text = "This is a text for testing. text for testing"
    result = my_pdf.get_count_of_occurrences("text", test_text)
    assert result == 2

    test_text = "textThis is a text for testing. text for testing"
    result = my_pdf.get_count_of_occurrences("text", test_text)
    assert result == 3

    test_text = "texttexttext"
    result = my_pdf.get_count_of_occurrences("text", test_text)
    assert result == 3

    test_text = "adfadfad"
    result = my_pdf.get_count_of_occurrences("text", test_text)
    assert result == 0


def test_split_text_in_three():
    text = "this is a test text"
    left, right = my_pdf.get_sides_of_text(text, "test")
    assert text == left + "test" + right


#--------------------------------------------------------------------------------------------------------------
def test_get_sorted_list_of_files():
    list_of_files = ['20200430-statements-7190-.pdf',
                     '20200529-statements-7190-.pdf',
                     '20200131-statements-7190-.pdf',
                     '20200930-statements-7190-.pdf']
    expected_list_of_files = ['20200131-statements-7190-.pdf',
                              '20200430-statements-7190-.pdf',
                              '20200529-statements-7190-.pdf',
                              '20200930-statements-7190-.pdf']

    print(my_list_of_files.get_sorted_list_based_on_month(list_of_files))
    assert my_list_of_files.get_sorted_list_based_on_month(list_of_files) == expected_list_of_files


def test_function_et_date_of_this_statement():
    text = "... August 31, 2019 through September 30 ..."
    expected_result = "August 31, 2019"
    result = my_pdf.get_date_of_this_statement(text).strip()
    assert result == expected_result

    text = "...August 31, 2019through September 30 ..."
    result = my_pdf.get_date_of_this_statement(text).strip()
    assert result == expected_result
