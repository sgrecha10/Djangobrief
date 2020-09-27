from django.urls import path
from . import views


app_name = 'views'
urlpatterns = [
    path('templateresponse/', views.template_response, name='templateresponse'),
    path('classview/', views.ClassView.as_view(), name='classview'),
    path('classtemplateview/', views.ClassTemplateView.as_view(), name='classtemplateview'),
    path('classredirectview/', views.ClassRedirectView.as_view(), name='classredirectview'),
    path('classdetailview/', views.ClassDetailView.as_view(), {'ug': 11}, name='classdetailview'),
    path('classlistview/', views.ClassListView.as_view(), name='classlistview'),
    path('classformview/', views.ClassFormView.as_view(), name='classformview'),
    path('classcreateview/', views.ClassCreateView.as_view(), name='classcreateview'),
    path('classupdateview/', views.ClassUpdateView.as_view(), {'pk': 8}, name='classupdateview'),
    path('classdeleteview/', views.ClassDeleteView.as_view(), {'pk': 12}, name='classdeleteview'),
]
