from django.urls import path
from . import views


app_name = "page"

urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result_page, name='result'),
    # path('anotherpage/', views.another_page, name='anotherpage')
]

# <str:something>