from .pdf import Pdf

from .list_of_files_from_directory import ListOfFilesFromDirectory
from .withdrawals_and_transactions.extractor import Extractor



def get_total(p):
    total = 0
    for each in p.withdrawals.list_of_transactions:
        extractor = Extractor(each)
        total += extractor.amount * 100
    return total / 100


# not applicable in our frontend
def go_through_each_folder_and_get_full_list_of_transactions(the_list):
    result = []
    for each in the_list:
        list_of_files = ListOfFilesFromDirectory(each)
        for path in list_of_files.sorted_full_path_list:
            p = Pdf(path)
            for transaction in p.get_withdrawals().list_of_withdrawals:
                extractor = Extractor(transaction)
                result.append(extractor.store)
    return result


# not applicable in our frontend
def get_transactions_from_each_file_in_folder(folder_path):
    result = []
    list_of_files = ListOfFilesFromDirectory(folder_path)
    sorted_list_of_files = list_of_files.sorted_full_path_list
    for each_file in sorted_list_of_files:
        opened_pdf = Pdf(each_file)
        list_of_transactions_in_string = opened_pdf.get_withdrawals().list_of_withdrawals
        for transaction_string in list_of_transactions_in_string:
            extractor_of_each_field = Extractor(transaction_string)
            result.append(extractor_of_each_field)
    return result


def get_transactions_from_file(pdf_file_or_path) -> list:
    result = []
    opened_pdf = Pdf(pdf_file_or_path)
    list_of_transactions_in_string = opened_pdf.get_withdrawals().list_of_withdrawals
    for transaction_string in list_of_transactions_in_string:
        extractor_of_each_field = Extractor(transaction_string)
        result.append(extractor_of_each_field)
    return result


def is_amount_correct(file_path):
    total = 0
    for each in get_transactions_from_file(file_path):
        total += each.amount * 100
    opened_pdf = Pdf(file_path)
    return opened_pdf.get_withdrawals().total_withdrawals["amount"] == total / 100


def does_each_file_has_withdrawals_total_amount_correct(path_dir):
    list_of_files = ListOfFilesFromDirectory(path_dir)
    sorted_list_of_files = list_of_files.sorted_full_path_list
    for each in sorted_list_of_files:
        print(is_amount_correct(each))


def get_list_of_files_in_dir(folder_path) -> list:
    a_list = ListOfFilesFromDirectory(folder_path)
    return a_list.sorted_full_path_list


# Personal Account only
def print_if_correct_each_pdf_file_transaction_in_folder(full_path_to_dir):
    files_in_directory = get_list_of_files_in_dir(full_path_to_dir)
    for each_file in files_in_directory:
        p = Pdf(each_file, is_personal_account=True)
        print(p.get_transaction_detail().is_total_sum_correct())
