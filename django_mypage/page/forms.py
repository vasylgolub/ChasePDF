from django import forms
from .models import Statement


# class UploadFileForm(forms.Form):
#     file = forms.FileField(label="Upload PDF File",
#                            widget=forms.FileInput(
#                                attrs={"class": "form-control fileToUpload", "id": "formFile"}))


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"class": "form-control form-control-sm fileToUpload", "id": "formFile"}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class FileFieldForm(forms.Form):
    files = MultipleFileField()