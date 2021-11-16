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
