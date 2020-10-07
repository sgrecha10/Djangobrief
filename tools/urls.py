from django.urls import path
from . import views


app_name = 'tools'
urlpatterns = [
    path('messages/', views.messages_view, name='messages_view'),
    path('xml/', views.xml_serialize_view, name='xml_serialize_view'),
    path('json/', views.json_serialize_view, name='json_serialize_view'),
    path('serialize-deserialize/', views.serialize_deserialize_view, name='serialize_deserialize_view'),
    path('sessions/', views.sessions_view, name='sessions_view'),
    path('static/', views.static_view, name='static_view'),
    path('validators/', views.validators_view, name='validators_view'),
    path('contenttypes/', views.contenttypes_view, name='contenttypes_view'),
]