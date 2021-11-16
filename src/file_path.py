import os


class ListOfFiles:
    def __init__(self, path_to_folder):
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
        self.list_of_files = self.get_sorted_list_based_on_month()

    def remove_non_pdf_files(self):
        self.list_of_files = [each_file
                              for each_file in self.list_of_files
                              if ".pdf" in each_file]

    def get_sorted_list_based_on_month(self, list_to_sort=None):
        if list_to_sort is None:
            return sorted(self.list_of_files, key=lambda x: x[4:])
        return sorted(list_to_sort, key=lambda x: x[4:])
