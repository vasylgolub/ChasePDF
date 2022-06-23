import os
from .pdf import Pdf


class FileToRename:
    def __init__(self, file_path):
        self.file_full_path = file_path
        self.current_file_name = os.path.basename(self.file_full_path)
        self.file_date = self.extract_date_from_file_pdf()

    def extract_date_from_file_pdf(self):
        the_pdf = Pdf(self.file_full_path)
        date = the_pdf.get_date_of_this_statement()
        return date

    # ------------------------------------------------------------------------------------------------
    # Let's make this method also return a message besides renaming the file
    def rename_file(self):
        new_name_for_file = self.file_date
        if self.was_file_already_renamed_to_desired_name(new_name_for_file + ".pdf", self.current_file_name):
            return "File was already renamed to desired name"

        extension = "pdf"
        dir_path = self.get_dir_path_of_where_the_file_is_stored()

        full_new_path = os.path.join(dir_path, new_name_for_file + "." + extension)
        self.finally_rename_the_file_to_new_name(full_new_path)

        return f"File renamed from {self.current_file_name} to {new_name_for_file}.{extension}"


    @staticmethod
    def was_file_already_renamed_to_desired_name(new, current):
        return new == current

    def get_dir_path_of_where_the_file_is_stored(self):
        res, _ = os.path.split(self.file_full_path)
        return res

    def finally_rename_the_file_to_new_name(self, new_path):
        os.rename(self.file_full_path, new_path)
    # ------------------------------------------------------------------------------------------------
