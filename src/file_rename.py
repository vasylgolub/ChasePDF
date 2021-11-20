import os


class FileRename:
    def __init__(self, file_path):
        self.file_full_path = file_path
        self.file_name = os.path.basename(self.file_full_path)
