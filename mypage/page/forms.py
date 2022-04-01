from django import forms


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()


class NameForm(forms.Form):
    # name = forms.CharField(label='Your name')
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea, required=False)
    sender = forms.EmailField(required=False)
    cc_myself = forms.BooleanField(required=False)
