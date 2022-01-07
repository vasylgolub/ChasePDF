from django.shortcuts import render

# Create your views here.

rooms = [
    {'id': 1, "name": "viewing the list"},
    {'id': 2, "name": "whatever"}
]


def home(request):
    return render(request, 'the_base/home.html', {'my_rooms': rooms})


def room(request):
    return render(request, 'room.html')
