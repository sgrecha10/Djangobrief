from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Permission
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm

from django.conf import settings
from django.views.generic import View, FormView, CreateView
from models.models import models
from . import forms
from django.forms import EmailField

from django.urls import reverse_lazy

# Create your views here.
def user_actions(request):
    # создание пользователя. Если username существует, то IntegrityError
    # user = User.objects.create_user(username='anna', email='anna@mail.ru', password='123')
    # user.save()

    # изменение пользователя, кроме password
    # user = get_object_or_404(User, username='anna')
    # user.first_name = 'Анна'
    # user.last_name = 'Чернышева'
    # user.is_staff = True # для доступа в admin
    # user.save()

    # изменение пароля
    # user = get_object_or_404(User, username='anna')
    # user.set_password('333')
    # user.save()

    # проверка прав пользователя
    # user = get_object_or_404(User, username='anna')
    # print(user.has_perm('models.add_blog'))

    # назначение прав пользователю
    # user = get_object_or_404(User, username='anna')
    # permission = get_object_or_404(Permission, codename='add_blog')
    # user.user_permissions.add(permission)
    # user.save()

    users = User.objects.all()
    context = {'users': users}
    return render(request, 'myauth/user_action.html', context)


def user_authenticate(request):
    if request.method == 'POST':
        form = forms.UserAuthenticate(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)  # функция проверяет, есть ли такой пользователь
            if user is not None:
                login(request, user) # функция авторизовывает пользователя в системе
                # вообще, тут надо редирект на успешную страницу
                return HttpResponse('Вы авторизованы, ' + request.user.username)
            else:
                # возвращаем "invalid name"
                return HttpResponse('Нет такого пользователя')
    else:
        form = forms.UserAuthenticate()

    context = {'form': form}
    return render(request, 'myauth/user_authenticate.html', context)


def logout_view(request):
    logout(request)
    # вообще тут надо редирект на успешную страницу.
    # return redirect('myauth:user_authenticate')
    return HttpResponse('Вы разлогинены')


# Добавляем дополнительное поле email в шаблонную форму регистрации новых юзеров
class MyUserCreationForm(UserCreationForm):
    email = EmailField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


class MyUserRegistration(FormView):
    form_class = MyUserCreationForm
    template_name = 'myauth/registration.html'
    success_url = reverse_lazy('myauth:user_actions')
    email = EmailField()

    def form_valid(self, form):
        form.save()
        # Функция super( тип [ , объект или тип ] )
        # Возвратите объект прокси, который делегирует вызовы метода родительскому или родственному классу типа .
        return super(MyUserRegistration, self).form_valid(form)

    def form_invalid(self, form):
        return super(MyUserRegistration, self).form_invalid(form)


class MyUserRegistration2(FormView):
    form_class = forms.UserRegistrationForm
    template_name = 'myauth/registration2.html'
    success_url = reverse_lazy('myauth:user_actions')

    def form_valid(self, form):
        print('form_valid')
        return redirect('myauth:user_actions')

    def form_invalid(self, form):
        print('form_invalid')
        return super().form_invalid(form)


def simple_authenticate(request):
    if request.user.is_authenticated:
        return HttpResponse('Мы вас узнали, вы - ' + request.user.username)
    else:
        return HttpResponse('Пользователь НЕ авторизован')


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='mynext')
def decorator_authenticate(request):
    return HttpResponse('Мы вас узнали, вы - ' + request.user.username)


class MixinAuthenticate(LoginRequiredMixin, View):
    login_url = '/newpathlogin/'
    redirect_field_name = 'onemorenext'

    def get(self, *args, **kwargs):
        return HttpResponse('Мы вас узнали, вы - ' + self.request.user.username)


class MyLoginView(LoginView):
    template_name = 'myauth/loginview.html' # по умолчанию registration/login.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = reverse('myauth:simple_authenticate')
        return context