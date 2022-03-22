from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    # return HttpResponse("ciao")
    lista = [0, 1, 2]
    context = {'lista': lista}
    return render(request, 'page/index.html', context)
