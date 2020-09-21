from django.urls import path
from . import views


app_name = 'template'
urlpatterns = [
    path('', views.index, name='index'),
]