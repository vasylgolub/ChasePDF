from django_mypage.page.src.pdf import Pdf

import pickle
from django_mypage.page.src.list_of_files_from_directory import ListOfFilesFromDirectory
import textwrap
from PyPDF2 import PdfFileReader
from django_mypage.page.src.file_rename import FileToRename
from pathlib import Path
import os
import re
from colorama import Fore
from colorama import Fore, Back, Style
from decimal import Decimal
# from .tools.file_stores_list import FileStoresList
# from .withdrawals_and_transactions.extractor import Extractor
# from .tools.directory_with_files_to_rename import DirectoryWithFilesToRename
import sys

# def get_total(p):
#     total = 0
#     for each in p.withdrawals.list_of_transactions:
#         extractor = Extractor(each)
#         total += extractor.amount * 100
#     return total / 100
#
#
# def go_through_each_folder_and_get_full_list_of_transactions(the_list):
#     result = []
#     for each in the_list:
#         list_of_files = ListOfFilesFromDirectory(each)
#         for path in list_of_files.sorted_full_path_list:
#             p = Pdf(path)
#             for transaction in p.get_withdrawals().list_of_withdrawals:
#                 extractor = Extractor(transaction)
#                 result.append(extractor.store)
#     return result
#
#
# def get_transactions_from_each_file_in_folder(folder_path):
#     result = []
#     list_of_files = ListOfFilesFromDirectory(folder_path)
#     sorted_list_of_files = list_of_files.sorted_full_path_list
#     for each_file in sorted_list_of_files:
#         opened_pdf = Pdf(each_file)
#         list_of_transactions_in_string = opened_pdf.get_withdrawals().list_of_withdrawals
#         for transaction_string in list_of_transactions_in_string:
#             extractor_of_each_field = Extractor(transaction_string)
#             result.append(extractor_of_each_field)
#     return result
#
#
# def get_transactions_from_file(pdf_file_path) -> list:
#     result = []
#     opened_pdf = Pdf(pdf_file_path)
#     list_of_transactions_in_string = opened_pdf.get_withdrawals().list_of_withdrawals
#     for transaction_string in list_of_transactions_in_string:
#         extractor_of_each_field = Extractor(transaction_string)
#         result.append(extractor_of_each_field)
#     return result
#
#
# def is_amount_correct(file_path):
#     total = 0
#     for each in get_transactions_from_file(file_path):
#         total += each.amount * 100
#     opened_pdf = Pdf(file_path)
#     return opened_pdf.get_withdrawals().total_withdrawals["amount"] == total/100
#
#
# def does_each_file_has_withdrawals_total_amount_correct(path_dir):
#     list_of_files = ListOfFilesFromDirectory(path_dir)
#     sorted_list_of_files = list_of_files.sorted_full_path_list
#     for each in sorted_list_of_files:
#         print(is_amount_correct(each))
#
#
# def get_list_of_files_in_dir(folder_path) -> list:
#     a_list = ListOfFilesFromDirectory(folder_path)
#     return a_list.sorted_full_path_list
#
#
# # Personal Account only
# def print_if_correct_each_pdf_file_transaction_in_folder(full_path_to_dir):
#     files_in_directory = get_list_of_files_in_dir(full_path_to_dir)
#     for each_file in files_in_directory:
#         p = Pdf(each_file, is_personal_account=True)
#         print(p.get_transaction_detail().is_total_sum_correct())


# f = open("/Users/vasylgolub/Desktop/list_of_transactions_2021", 'wb')
# for each_file_path in get_list_of_files_in_dir("/Users/vasylgolub/Desktop/pdfs/2021"):
#     for transaction in get_transactions_from_file(each_file_path):
#         pickle.dump(transaction, f)
        # print(f'{transaction.date[0]} {transaction.store} {transaction.amount}')
# f.close()




# ------------------------------------------------------------------------------

# I think I used these methods on a file that contained a list of objects.
# Each object had: date, description, amount

# def get_list_of_objects(file_path_to_file) -> list:
#     f = open(file_path_to_file, 'rb')
#     res: list = []
#     while 1:
#         try:
#             res.append(pickle.load(f))
#         except EOFError:
#             break
#     f.close()
#     return res
#
#
# def from_obj_to_sorted_dict(objs) -> dict:
#     dic = {}
#     for transaction in objs:
#         if transaction.store in dic:
#             dic[transaction.store] += 1
#         else:
#             dic[transaction.store] = 0
#     dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])}
#     return dic
#
#
# def remove_matched_items(list_of_objects, string):
#     res = []
#     for transaction in list_of_objects:
#         if string not in transaction.store:
#             res.append(transaction)
#     return res
#
#
# def get_matched_items(list_of_objects, string):
#     res = []
#     for transaction in list_of_objects:
#         if string in transaction.store:
#             res.append(transaction)
#     return res
#
#
# def match_items_with_key_words_in_a_list(objects, key_words):
#     res = []
#     for key_word in key_words:
#         res.extend(get_matched_items(objects, key_word))
#         objects = remove_matched_items(objects, key_word)
#     return res
#
#
# def remove_items_with_key_words_from_list(objects, key_words):
#     for key_word in key_words:
#         objects = remove_matched_items(objects, key_word)
#     return objects

# ------------------------------------------------------------------------------

# print(sys.prefix)
# print(sys.base_prefix)
#
# stores_key_words = ['Flooring', "Paint", 'Insurance', 'Aaa', 'The Home Depot',
#                     'Lowe\'s', 'Public Storage', 'Discount Builders', 'Meter', 'Ips Berkeley',
#                     'Fastrak', 'Rentals', 'Sherwin Williams', 'Kellymoore', 'Hardware', 'House of Color',
#                     'Auto Glass', 'Juarez Tire Shop', 'East Star Building',
#                     'U Haul Store', 'Recology', 'Jiffy Lube', 'Harbor Freight Tools']
#
# other_stores = ['Paypal', 'Apple', 'Walgreens', 'Target',
#                 'Costco', 'Coffee', 'Wholefds', 'Venmo', 'T-Mobile',
#                 'Safeway', 'One65', 'Hawaii', 'Honolulu', 'Starbucks',
#                 'IN N Out', 'Tpumps', 'Oasis', 'Vegan Picnic', 'Best Buy', 'Via', "Como", "Porlezza"]
#
# objs = get_list_of_objects("/Users/vasylgolub/Desktop/list_of_transactions_2021")



# expenses = match_items_with_key_words_in_a_list(objs, stores_key_words)
# objs = remove_items_with_key_words_from_list(objs, stores_key_words)
#
# expenses2 = match_items_with_key_words_in_a_list(objs, other_stores)
# objs = remove_items_with_key_words_from_list(objs, other_stores)
#
# tot = 0
# for t, v in from_obj_to_sorted_dict(expenses).items():
#     print(f'{t} {v}')
    # tot += t.amount
    # print(f'{t.date[0]} {t.store} {t.amount}')
# print(tot)

# for t in sorted(expenses, key=lambda x: x.amount):
#     print(f'{t.date[0]} {t.store} {t.amount}')





# for i, j in from_obj_to_sorted_dict(objects).items():
#     print(f'{i} {j}')

        # print(f'{transaction.date[0]} {transaction.store} {transaction.amount}')










# files_in_dir = get_list_of_files_in_dir("/Users/vasylgolub/Desktop/personal-pdfs/2020")

# p = Pdf("/Users/vasylgolub/Desktop/personal-pdfs/2018/April 17, 2018.pdf", is_personal_account=True)
#
# for i in p.get_transaction_detail().list_of_transactions:
#     print(i)





















# from .useful_funcs import *

# print_if_correct_each_pdf_file_transaction_in_folder("/Users/vasylgolub/Desktop/personal-pdfs/2018")
# print_if_correct_each_pdf_file_transaction_in_folder("/Users/vasylgolub/Desktop/personal-pdfs/2019")
# print_if_correct_each_pdf_file_transaction_in_folder("/Users/vasylgolub/Desktop/personal-pdfs/2020")
# does_each_file_has_withdrawals_total_amount_correct("/Users/vasylgolub/Desktop/pdfs/2018")
# does_each_file_has_withdrawals_total_amount_correct("/Users/vasylgolub/Desktop/pdfs/2019")
# does_each_file_has_withdrawals_total_amount_correct("/Users/vasylgolub/Desktop/pdfs/2020")
# does_each_file_has_withdrawals_total_amount_correct("/Users/vasylgolub/Desktop/pdfs/2021")


# my_extractor = Extractor("01/16 Card Purchase 01/13 Dj Tech 877-645-5377 CA Card 6427$239.24")
# my_extractor = Extractor("01/16 Card Purchase With Pin 01/13 Shell Service Statio San Francisco CA Card 642735.19")
# print(my_extractor.get_card_last_4_digits("01/16 Card Purchase With Pin 01/13 Shell Service Statio San Francisco CA Card 642735.19"))
# expected_result = 239.24
# print(my_extractor.get_amount())
# print(my_extractor.get_amount() == expected_result)














#####################################################################################################################
#####################################################################################################################
# print([l for l in "hello"])

# cut = lambda x: x[4:]
# print(cut('20200430-statements-7190-.pdf'))
# #
# full_name = lambda name, last_name: f"{name.title()} {last_name.title()}"
# print(full_name("vasyl", "golub"))


# list_of_files = [    '20200430-statements-7190-.pdf',
#                      '20200529-statements-7190-.pdf',
#                      '20200131-statements-7190-.pdf',
#                      '20200930-statements-7190-.pdf']
#
# def cut(name):
#     return name[4:]
#
#
# s = sorted(list_of_files, key=lambda x: x[6:7])
# for i in s:
#     print(i)


# Anonymous functions
# s = lambda x, y: x + y
#
# print(s(3, 4))

# Immediately Invoked Function Expression
# >>> (lambda x, y: x + y)(2, 3)
# 5
#####################################################################################################################
#####################################################################################################################

