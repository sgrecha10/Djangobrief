from django.urls import path
from . import views


app_name = 'myauth'
urlpatterns = [
    path('user/', views.user_actions, name='user_actions'),
    path('authenticate/', views.user_authenticate, name='user_authenticate'),
    path('logout/', views.logout_view, name='logout'),
    path('simple/', views.simple_authenticate, name='simple_authenticate'),
    path('decorator/', views.decorator_authenticate, name='decorator_authenticate'),
    path('mixin/', views.MixinAuthenticate.as_view(), name='mixin_authenticate'),
]
