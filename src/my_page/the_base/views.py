from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return HttpResponse('Home pageeeee')


def room(request):
    return HttpResponse("Welcome to my Room")
