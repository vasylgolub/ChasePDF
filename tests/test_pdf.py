from src.pdf import Pdf
from src.list_of_files_from_directory import ListOfFilesFromDirectory
from src.withdrawals_text_cleaner import WithdrawalsTextCleaner
from src.extractor import Extractor
from src.withdrawals_helper import WithdrawalsHelper

# file_path = "/Users/vasylgolub/Desktop/pdfs/2020/20200131-statements-7190-.pdf"
list_of_files = ListOfFilesFromDirectory("/Users/vasylgolub/Desktop/pdfs/2019")
file_path = list_of_files.with_full_path()[0]
my_pdf = Pdf(file_path)
my_withdrawals = WithdrawalsTextCleaner()
my_withdrawals_helper = WithdrawalsHelper


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
def test_get_lef_side_and_date_at_the_end():
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

    expected_line = "Card Purchase With Pin 02/26 Guitar Center #220 San Francisco CA Card 642714.0902/27"
    expected_line2 = "Card Purchase With Pin 02/01 Safeway #3031 Daly City CA Card 64277.0302/03"
    expected_line3 = "Card Purchase 02/13 Paypal *Theau 402-935-7733 CA Card 642759.0002/14"

    assert my_withdrawals.get_lef_side_and_date_at_the_end(line1) == expected_line
    assert my_withdrawals.get_lef_side_and_date_at_the_end(line2) == expected_line2
    assert my_withdrawals.get_lef_side_and_date_at_the_end(line3) == expected_line3



def test_extract_date_at_the_end_of_a_string():
    txt_test = "Card Purchase 02/01 Tst* Vegan Picnic - San Francisco CA Card 642718.2902/03"
    assert my_withdrawals.extract_date_at_the_end(txt_test) == "02/03"


def test_extract_date_at_the_end_of_a_string2():
    txt_test2 = "Card Purchase With Pin 02/28 Nst Best Buy 0630 Colma CA Card 6427243.48"
    assert my_withdrawals.extract_date_at_the_end(txt_test2) == ""


def test_get_str_with_date_removed_at_the_end():
    txt_test = "Card Purchase 02/27 Wingstop Daly City #517 Daly City CA Card 642713.1502/27"
    expected_string = "Card Purchase 02/27 Wingstop Daly City #517 Daly City CA Card 642713.15"
    assert my_withdrawals.get_str_with_date_removed_at_the_end(txt_test) == expected_string


def test_get_str_with_date_removed_at_the_end_that_doesnt_need_removal():
    txt_test = "Total ATM & Debit Card Withdrawals $5,375.22"
    expected_string = "Total ATM & Debit Card Withdrawals $5,375.22"
    assert my_withdrawals.get_str_with_date_removed_at_the_end(txt_test) == expected_string


def test_get_total_from_string():
    txt_test = " Total ATM & Debit Card Withdrawals $6,896.00"
    print(my_withdrawals_helper.get_total_from_this_string(txt_test))
    assert my_withdrawals_helper.get_total_from_this_string(txt_test) == 6896.00


def test_get_left_side_only():
    string_test = "Total ATM & Debit Card Withdrawals $4,261.68 1010897020200000006234Pageof*start*atmanddebitcard" \
                  "summary*end*atmanddebitcardsummary*start*otherwithdrawals*end*otherwithdrawals*start*feessection*" \
                  "end*feessection*start*postfeesmessage*end*postfeesmessage*start*dailyendingbalance2*end*daily" \
                  "endingbalance2*start*servicechargesummary3*end*servicechargesummary3May 30, 2020 through June 30, " \
                  "2020Account Number: 000000253227190"
    assert my_withdrawals.get_left_side_only(string_test) == "Total ATM & Debit Card Withdrawals $4,261.68"


# Bug fix
def test_extract_cash_back():
    test_text = "Card Purchase W/Cash 06/26 Lowe's #3095 San Francisco CA Card 6427 " \
                "Purchase $107.42 Cash Back $40.00" \
                "147.4206/26"
    result = "Purchase $107.42 Cash Back $40.00"
    assert my_withdrawals.extract_cash_back_info(test_text) == result

    test_text = "Card Purchase W/Cash 09/29 Target T-2768 2675 G San Francisco CA Card 6427 " \
                "Purchase $74.28 Cash Back $40.00" \
                "114.2810/01"
    result = "Purchase $74.28 Cash Back $40.00"
    assert my_withdrawals.extract_cash_back_info(test_text) == result


#-------------------------------------------extractor class---------------------------------------------------------
def test_get_amount():
    test_text = "01/16 Card Purchase 01/13 Dj Tech 877-645-5377 CA Card 6427$239.24"
    expected_result = 239.24
    assert Extractor.get_amount(test_text) == expected_result

    test_text = "01/16 Card Purchase With Pin 01/13 Shell Service Statio San Francisco CA Card 642735.19"
    expected_result = 35.19
    assert Extractor.get_amount(test_text) == expected_result

    test_text = "01/16 Card Purchase With Pin 01/13 Shell Service Statio San Francisco CA Card 64243,735.19"
    expected_result = 3735.19
    assert Extractor.get_amount(test_text) == expected_result


def test_get_type_withdrawal():
    test_text = "01/16 Card Purchase 01/13 Dj Tech 877-645-5377 CA Card 6427$239.24"
    expected_result = "Card Purchase"
    test_text2 = "03/19ATM Withdrawal03/18 5655 Geary Blvd San Francisco CA Card 642740.00"
    expected_result2 = "ATM Withdrawal"
    assert Extractor.get_type_withdrawal(test_text) == expected_result
    assert Extractor.get_type_withdrawal(test_text2) == expected_result2


def test_get_date():
    test_text = "01/16 Card Purchase 01/13 Dj Tech 877-645-5377 CA Card 6427$239.24"
    expected_result = ["01/16", "01/13"]
    test_text2 = "03/19ATM Withdrawal03/18 5655 Geary Blvd San Francisco CA Card 642740.00"
    expected_result2 = ["03/19", "03/18"]
    assert Extractor.get_date(test_text) == expected_result
    assert Extractor.get_date(test_text2) == expected_result2


def test_get_last_4_digits():
    test_text = "01/16 Card Purchase 01/13 Dj Tech 877-645-5377 CA Card 6427$239.24"
    expected_result = "6427"
    assert Extractor.get_last_4_digits(test_text) == expected_result

    test_text = "01/16 Card Purchase 01/13 Dj Tech 877-645-5377 CA Card6427$239.24"
    expected_result = "6427"
    assert Extractor.get_last_4_digits(test_text) == expected_result

    test_text = "Tech 877-645-534377 34324524CA Card64274334$239.24"
    expected_result = "6427"
    assert Extractor.get_last_4_digits(test_text) == expected_result


def test_get_store():
    my_extractor = Extractor("01/16 Card Purchase With Pin 01/13 Shell Service Statio San Francisco CA Card 642735.19")
    expected_result = "Shell Service Statio San Francisco CA Card"
    assert my_extractor.store == expected_result

    my_extractor = Extractor("01/16 Card Purchase With Pin 01/13Shell Service Statio San Francisco CA Card 642735.19")
    expected_result = "Shell Service Statio San Francisco CA Card"
    assert my_extractor.store == expected_result

    my_extractor = Extractor("01/16 Card Purchase With Pin 01/13Shell Service Statio San Francisco CA Card642735.19")
    expected_result = "Shell Service Statio San Francisco CA Card"
    assert my_extractor.store == expected_result

