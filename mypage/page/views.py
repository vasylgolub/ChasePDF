from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import NameForm, UploadFileForm
import sys
# from .handle_uploaded_file import HandleUploadedFile

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            # list_of_transactions = HandleUploadedFile(file).transactions
            # print(list_of_transactions)
            # print(file)
            for i in sys.path:
                print(i)

            return HttpResponseRedirect(reverse("page:index"))
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

