from django import forms
from .models import Statement


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Upload PDF File",
                           widget=forms.FileInput(
                               attrs={"class": "form-control fileToUpload", "id": "formFile"}))