from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


app_name = 'myauth'
urlpatterns = [
    path('user/', views.user_actions, name='user_actions'),
    path('authenticate/', views.user_authenticate, name='user_authenticate'),
    path('registration/', views.MyUserRegistration.as_view(), name='user_registration'),
    path('registration2/', views.MyUserRegistration2.as_view(), name='user_registration2'),
    path('logout_func/', views.logout_view, name='logout_func'),
    path('simple/', views.simple_authenticate, name='simple_authenticate'),
    path('decorator/', views.decorator_authenticate, name='decorator_authenticate'),
    path('mixin/', views.MixinAuthenticate.as_view(), name='mixin_authenticate'),
    path('loginview/', views.MyLoginView.as_view(), name='loginview'),
    path('', include('django.contrib.auth.urls')),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('myauth:password_change_done')), name='password_change'
         ),
]
