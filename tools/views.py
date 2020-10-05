from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import serializers
from models.models import Blog
from django.http import HttpResponse
from django.conf import settings


# Create your views here.
def messages_view(request):

    messages.add_message(request, messages.INFO, 'Hello world.')
    messages.success(request, 'Profile details updated.')

    context = {'data': 'messages_view'}
    return render(request, 'tools/messages.html', context)


def xml_serialize_view(request):
    queryset = Blog.objects.all()
    data = serializers.serialize("xml", queryset)
    return HttpResponse(data, content_type='text/xml')


def json_serialize_view(request):
    queryset = Blog.objects.all()
    data = serializers.serialize("json", queryset)
    return HttpResponse(data, content_type='application/json')


def serialize_deserialize_view(request):
    queryset = Blog.objects.all()
    xml_data = serializers.serialize("xml", queryset)
    data = serializers.deserialize("xml", xml_data)

    # что бы сохранить в бд. сохранять нужно по одному обьекту
    objects = list(serializers.deserialize("xml", xml_data))
    b0 = objects[0].object  # DeserializedObject to class Model

    b0.save()

    context = {'data': data}
    return render(request, 'tools/serialize_deserialize.html', context)


def sessions_view(request):
    context = {}
    context.update({'SESSION_COOKIE_AGE': settings.SESSION_COOKIE_AGE})
    # Проверяем, что куки включены в браузере
    request.session.set_test_cookie()
    if request.session.test_cookie_worked():
        context['test_cookie'] = 'YES'
        request.session.delete_test_cookie()
    else:
        context['test_cookie'] = 'NO. Try F5'

    # Проверяем, что пользователь пришел впервые и показывваем ему message
    if not request.session.get('no_first_time', False):
        messages.success(request, 'Вы тут впервые. Это сообщение увидите только один раз  за минуту')
        request.session['no_first_time'] = True
        request.session.set_expiry(60)
    # del request.session['no_first_time']

    if request.GET.get('del_cookie') is not None:
        request.session.flush()
        return redirect('tools:sessions_view')


    # context = {'data': 'grecha'}
    return render(request, 'tools/session.html', context)