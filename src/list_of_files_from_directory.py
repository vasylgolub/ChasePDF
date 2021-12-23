import os
from pathlib import Path


# To be used with a directory that has pdf files already renamed properly
class ListOfFilesFromDirectory:
    def __init__(self, path_to_folder=None):
        if path_to_folder is not None:
            self.months = ['January', 'February', 'March', 'April', 'May',
                           'June', 'July', 'August', 'September', 'October', 'November', 'December']
            self.path_to_folder = path_to_folder
            self.files = os.listdir(path_to_folder)
            self.remove_non_pdf_files()
            # self.sorted_list_of_files = self.sorted()
            # self.sorted_full_path_list = self.get_sorted_full_path_list()

    def remove_non_pdf_files(self):
        self.files = [each_file for each_file in self.files if ".pdf" in each_file]

    def with_full_path(self):
        result_list = []
        for each in self.files:
            result_list.append(os.path.join(self.path_to_folder, each))
        return result_list


    def sort_by_month_then_date(self, unordered_list_of_files=None) -> list:
        months_values = {'January': 0, 'February': 100, 'March': 200, 'April': 300, 'May': 400,
                         'June': 500, 'July': 600, 'August': 700, 'September': 800, 'October': 900,
                         'November': 1000, 'December': 1100}
        if unordered_list_of_files is None:
            unordered_list = self.files

        dic_of_file_names = {}

        # Each file's name will get a unique value
        for file_name in unordered_list_of_files:
            month, day = self.extract_month_and_day_string(file_name)
            day_plus_month_value = int(day) + months_values[month]
            dic_of_file_names[day_plus_month_value] = file_name

        sorted_based_on_key = dict(sorted(dic_of_file_names.items()))
        return list(sorted_based_on_key.values())

    # ------------------------------------------------------------------------------------------------
    def sorted(self, list_to_sort=None):
        n_files_in_folder = len(self.files)  # In case we want to sort files that are less then 12
        if list_to_sort is None:
            list_to_sort = self.files
        hint = self.get_hint_on_how_to_sort_this_list_of_months(list_to_sort)
        ordered_list = [None] * n_files_in_folder
        for i in range(0, n_files_in_folder):
            ordered_list[hint[i]] = list_to_sort[i]
        return ordered_list

    @staticmethod
    def extract_month_and_day_string(file_name):
        pos_first_space = file_name.find(" ")
        month = file_name[:pos_first_space]
        day = file_name[pos_first_space:pos_first_space + 3]
        return month, day

    @staticmethod
    def it_is_the_last_day_of_this_month(day):
        return int(day) > 26


    def get_hint_on_how_to_sort_this_list_of_months(self, list_to_sort):
        result = []
        for file in list_to_sort:
            just_month, its_day = self.extract_month_and_day_string(file)
            calendar_pos = self.months.index(just_month)
            if self.it_is_the_last_day_of_this_month(its_day):
                calendar_pos += 1
            result.append(calendar_pos)
        return result
    #------------------------------------------------------------------------------------------------

    def get_sorted_full_path_list(self):
        result = []
        for each in self.sorted_list_of_files:
            full_path = self.path_to_folder + "/" + each
            result.append(full_path)
        return result
