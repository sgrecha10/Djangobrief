from django.urls import path
from . import views
from django.http import HttpResponse


app_name = 'template'
urlpatterns = [
    path('', views.index, name='index'),
]

