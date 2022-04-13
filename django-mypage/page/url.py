from django.urls import path
from . import views


app_name = "page"

urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result_page, name='result')
]

# <str:something>