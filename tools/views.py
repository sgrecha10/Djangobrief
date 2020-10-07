from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import serializers
from models.models import Blog
from django.http import HttpResponse
from django.conf import settings
from .forms import TestValidatorForm
from django.contrib.contenttypes.models import ContentType
from .models import TaggedItem, MyUser




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


def static_view(request):
    context = {}
    return render(request, 'tools/static.html', context)


def validators_view(request):
    if request.method == 'POST':
        form = TestValidatorForm(request.POST)
        if form.is_valid():
            print('Валидно')
    else:
        form = TestValidatorForm()

    context = {'form': form}
    return render(request, 'tools/validators.html', context)


def contenttypes_view(request):
    data = {}
    user_type = ContentType.objects.get(app_label='auth', model='user')
    # print(user_type.model_class())
    anna = user_type.get_object_for_this_type(username='anna')
    # print(anna.first_name)
    data.update({'anna.first_name': anna.first_name})

    # теперь самое интересное, обобщенные связи generic relations
    # t1 = TaggedItem(content_object=anna, tag='тег1')
    # t1.save()
    # t2 = TaggedItem(content_object=anna, tag='тег2')
    # t2.save()

    # получаем все теги пользователя anna
    t = TaggedItem.objects.filter(content_type=user_type, object_id=anna.pk)
    data.update({'anna - tag': list(t)})

    # получаем всех пользователей, которым принадлежит тег
    # это возможно если в модели пользователя есть поле GenericRelation
    # т.к. в User такого поля нет, то создаем в этом приложении прокси от него с нужным полем MyUser
    # при использовании прокси модели в TaggedItem нужно определить for_concrete_model=False
    user_type_2 = ContentType.objects.get(app_label='tools', model='myuser')
    anna_2 = user_type_2.get_object_for_this_type(username='anna')
    print(anna_2.first_name)
    # t1 = TaggedItem(content_object=anna_2, tag='тег5')
    # t1.save()
    # t2 = TaggedItem(content_object=anna_2, tag='тег6')
    # t2.save()

    # сначала так же отображаем все теги пользователя anna (через прокси)
    t = TaggedItem.objects.filter(content_type=user_type_2, object_id=anna_2.pk)
    data.update({'anna_2 - tag': list(t)})

    # теперь можно отобразить все теги пользователя анна и вот тае еще:
    data.update({'anna_2.tags.all()': list(anna_2.tags.all())})

    # а вот все таки и обратная обобщенная связь в действии:
    t1 = TaggedItem.objects.get(tag='тег5')
    users_t1 = MyUser.objects.filter(tags=t1)
    data.update({'users_t1': list(users_t1)})

    context = {'data': data}
    return render(request, 'tools/contenttypes.html', context)
