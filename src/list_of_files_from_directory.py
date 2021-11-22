import os


class ListOfFilesFromDirectory:
    def __init__(self, path_to_folder):
        self.months = ['January', 'February', 'March', 'April', 'May',
                       'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.list_of_files = []

        if os.path.exists(path_to_folder):
            self.path_to_folder = path_to_folder
        else:
            self.path_to_folder = "WRONG PATH"
        if not os.path.isdir(path_to_folder):
            self.path_to_folder = "IT'S NOT DIRECTORY"
        else:
            self.list_of_files = os.listdir(path_to_folder)
        self.remove_non_pdf_files()


    def remove_non_pdf_files(self):
        self.list_of_files = [each_file
                              for each_file in self.list_of_files
                              if ".pdf" in each_file]

    def get_list_of_files_with_full_path(self):
        result_list = []
        for each in self.list_of_files:
            result_list.append(os.path.join(self.path_to_folder, each))
        return result_list

    # ------------------------------------------------------------------------------------------------
    def sorted(self, list_to_sort=None):
        if list_to_sort is None:
            list_to_sort = self.list_of_files
        hint = self.get_hint_on_how_to_sort_this_list_of_months(list_to_sort)
        ordered_list = [None] * 12
        for i in range(0, 12):
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

