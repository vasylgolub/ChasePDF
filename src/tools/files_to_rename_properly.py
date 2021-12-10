import os
from src.file_rename import FileToRename


# When you just have downloaded new pdf files from Chase website, use this class to rename all those files inside
# the folder. And it will rename them according to their date related.
class DirectoryWithFilesToRename:
    def __init__(self, directory_path):
        self._directory = directory_path
        self._files = os.listdir(directory_path)

    def start_renaming(self):
        for each_file_name in self._files:
            f = FileToRename(self._directory + "/" + each_file_name)
            f.rename_file()
