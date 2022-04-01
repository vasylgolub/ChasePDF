from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import NameForm, UploadFileForm
from PyPDF2 import PdfFileReader
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']

            opened_file = file.open()
            read_pdf_file = PdfFileReader(opened_file)
            if read_pdf_file.isEncrypted:
                read_pdf_file.decrypt("")
            print(read_pdf_file)

            return HttpResponseRedirect(reverse("page:index"))
        # message = request.FILES
        # return render(request, 'page/index.html', {'message': message})
    else:
        form = UploadFileForm()
    return render(request, 'page/index.html', {'form': form})



def result_page(request):
    if request.method == "POST":
        text = request.POST['just_a_text']
        # return render(request, 'page/result.html', {'text': text})
        # assert False
        return HttpResponseRedirect(reverse("page:result"))
    else:
        return render(request, 'page/result.html')

