from src.pdf import Pdf
from src.list_of_files_from_directory import ListOfFilesFromDirectory
from src.withdrawals import Withdrawals

# file_path = "/Users/vasylgolub/Desktop/pdfs/2020/20200131-statements-7190-.pdf"
list_of_files = ListOfFilesFromDirectory("/Users/vasylgolub/Desktop/pdfs/2019")
file_path = list_of_files.with_full_path()[0]
my_pdf = Pdf(file_path)
# my_list_of_files = ListOfFilesFromDirectory("")


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
    a_pdf = Pdf(file_path)
    a_pdf.text = "CHECKING SUMMARY Chase Total Business CheckingINSTANCESAMOUNTBeginning Balance$1,598. and " \
                 "DEPOSITS AND ADDITIONSDATEDESCRIPTIONAMOUNT06/03Payment Received 06/03 "
    result = a_pdf.get_desired_section("CHECKING SUMMARY")
    expected_result = "CHECKING SUMMARY Chase Total Business CheckingINSTANCESAMOUNTBeginning Balance$1,598. and "
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
# list must have 12 elements
def test_get_sorted_list_of_files():
    list_of_unordered_files = ['June 01, 2019.pdf', 'June 29, 2019.pdf', 'May 01, 2019.pdf', 'January 01, 2019.pdf',
                               'October 01, 2019.pdf', 'March 01, 2019.pdf', 'March 30, 2019.pdf',
                               'November 01, 2019.pdf', 'November 30, 2019.pdf', 'August 01, 2019.pdf',
                               'August 31, 2019.pdf', 'February 01, 2019.pdf']

    expected_list_of_files = ['January 01, 2019.pdf',
                              'February 01, 2019.pdf',
                              'March 01, 2019.pdf',
                              'March 30, 2019.pdf',
                              'May 01, 2019.pdf',
                              'June 01, 2019.pdf',
                              'June 29, 2019.pdf',
                              'August 01, 2019.pdf',
                              'August 31, 2019.pdf',
                              'October 01, 2019.pdf',
                              'November 01, 2019.pdf',
                              'November 30, 2019.pdf']
    result = list_of_files.sorted(list_of_unordered_files)
    assert result == expected_list_of_files


def test_function_et_date_of_this_statement():
    text = "... August 31, 2019 through September 30 ..."
    expected_result = "August 31, 2019"
    result = my_pdf.get_date_of_this_statement(text).strip()
    assert result == expected_result

    text = "...August 31, 2019through September 30 ..."
    result = my_pdf.get_date_of_this_statement(text).strip()
    assert result == expected_result


#-------------------------------------------Withdrawals class---------------------------------------------------------
def test_get_cleaner_list():
    line1 = "Card Purchase With Pin 02/26 Guitar Center #220 San Francisco CA Card 642714.09 " \
                "46Pageof*start*atmdebitwithdrawal*end*atmdebitwithdrawal*start*atmanddebitcardsummary*end*" \
                "atmanddebitcardsummary*start*electronicwithdrawal*end*electronicwithdrawal*start*" \
                "otherwithdrawals*end*otherwithdrawals*start*feessection*end*feessection*start*" \
                "postfeesmessage*end*postfeesmessageFebruary 01, 2020 through February 28, 2020Account Number: " \
                "000000253227190ATM & DEBIT CARD WITHDRAWALS (continued)DATEDESCRIPTIONAMOUNT02/27"
    line2 = "Card Purchase With Pin 02/01 Safeway #3031 Daly City CA Card 64277.03 " \
            "26Pageof*start*atmdebitwithdrawal*end*atmdebitwithdrawalFebruary 01, 2020 through February 28, " \
            "2020Account Number: 000000253227190ATM & DEBIT CARD WITHDRAWALS (continued)DATEDESCRIPTIONAMOUNT02/03"
    line3 = "Card Purchase 02/13 Paypal *Theau 402-935-7733 CA Card 642759.00 " \
            "1015440030200000006336Pageof*start*atmdebitwithdrawal*end*atmdebitwithdrawalFebruary 01, " \
            "2020 through February 28, 2020Account Number: 000000253227190ATM & DEBIT CARD WITHDRAWALS " \
            "(continued)DATEDESCRIPTIONAMOUNT 02/14"
    list_of_text_to_clean = [line1, line2, line3]

    expected_line = "Card Purchase With Pin 02/26 Guitar Center #220 San Francisco CA Card 642714.0902/27"
    expected_line2 = "Card Purchase With Pin 02/01 Safeway #3031 Daly City CA Card 64277.0302/03"
    expected_line3 = "Card Purchase 02/13 Paypal *Theau 402-935-7733 CA Card 642759.0002/14"
    expected_list = [expected_line, expected_line2, expected_line3]
    my_withdrawals = Withdrawals("")
    assert my_withdrawals.remove_unnecessary_info_from_some_elements(list_of_text_to_clean)[0] == expected_list[0]
    assert my_withdrawals.remove_unnecessary_info_from_some_elements(list_of_text_to_clean)[1] == expected_list[1]
    assert my_withdrawals.remove_unnecessary_info_from_some_elements(list_of_text_to_clean)[2] == expected_list[2]
