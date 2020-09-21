from django.urls import path
from . import views


app_name = 'forms'

urlpatterns = [
    path('usualforms/', views.usualforms, name='usualforms'),
    path('modelforms/', views.modelforms, name="modelforms"),
    path('modelforms/author/<int:author_id>/', views.modelformsauthor, name="modelformauthor"),
    path('modelforms/book/<int:book_id>/', views.modelformbook, name="modelformbook"),
    path('customforms/', views.customforms, name='customforms'),
    path('formsets/', views.setforms, name='setforms'),
    path('modelformsets/', views.setmodelforms, name='setmodelforms'),
    path('inlineformsets/', views.inlineformset, name='inlineformset'),
    path('uploadfiles/', views.uploadfiles, name='uploadfiles'),
    path('uploadfilesmodel/', views.uploadfilesmodel, name='uploadfilesmodel'),
]
