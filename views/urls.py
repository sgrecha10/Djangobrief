from django.urls import path
from . import views


app_name = 'views'
urlpatterns = [
    path('templateresponse/', views.template_response, name='templateresponse'),
    path('classview/', views.ClassView.as_view(), name='classview'),
    path('classtemplateview/', views.ClassTemplateView.as_view(), name='classtemplateview'),
    path('classredirectview/', views.ClassRedirectView.as_view(), name='classredirectview'),
]
