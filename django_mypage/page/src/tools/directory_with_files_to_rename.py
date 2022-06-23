import os
from ..file_rename import FileToRename


# When you just have downloaded new pdf files from Chase website, use this class to rename all those files inside
# the folder. And it will rename them according to their date related.
class DirectoryWithFilesToRename:
    def __init__(self, directory_path):
        self._directory = directory_path
        self._files = os.listdir(directory_path)

        # Remove files that are not pdfs
        for each_file in self._files:
            if each_file[-4:] != ".pdf":
                os.remove(self._directory + "/" + each_file)

    def start_renaming(self):
        for each_file_name in self._files:
            f = FileToRename(self._directory + "/" + each_file_name)
            f.rename_file()
        self._files = os.listdir(self._directory)  # Update list of files

    def get_list_of_target_files(self):
        return self._files
