from django.apps import AppConfig
from django.core.signals import request_started
from django.dispatch import receiver

# создаем свой сигнал вне представлений, что бы он был доступен в представлениях для отправки и для функции получателя
import django.dispatch
my_little_signal = django.dispatch.Signal(providing_args=["top", "size"])


class ToolsConfig(AppConfig):
    name = 'tools'

    def ready(self):
        # здесь регистрируем сигнал и присоединяем его к обработчику.
        # как тут использовать декоратор я не понял, потому что функция-обработчик должна быть определена не здесь.
        # если функция-обработчик будет определена в другой файле, то ее нужно импортировать
        request_started.connect(my_callback_signal) # можно и так зарегистрировать сигнал, без декоратора

        # а вот так можно отключить сигнал при необходимости
        # request_started.disconnect(my_callback_signal)

        # регистрируем собственный сигнал
        my_little_signal.connect(my_callback_signal_2)

        # так регистрируем собственную функцию проверки
        # register(example_check)


# функции обработчики сигналов (кое где предлагают даже создать спецфайл для обработчиков handlers.py)
def my_callback_signal(sender, **kwargs):
    print('my_callback_signal')


def my_callback_signal_2(sender, **kwargs):
    print('my_little_signal. top %s, size %s' % (kwargs['top'], kwargs['size']))


# вообще, можно определить функции обработчики и сразу зарегистрировать сигнал с
# помощью декоратора. но регистрировать сигнал нужно в ready() поэтому это не очень правильно
"""@receiver(request_started)
def my_callback_signal(sender, **kwargs):
    print('my_callback_signal')

@receiver(my_little_signal)
def my_callback_signal_2(sender, **kwargs):
    print('my_little_signal. top %s, size %s' % (kwargs['top'], kwargs['size']))"""


# создаем и регистрируем функцию собственной проверки при старте сервера и по команде check
from django.core.checks import Error, register
#@register()
def example_check(app_configs, **kwargs):
    errors = []
    if True:
        errors.append(Error('an error', obj='myobj', hint='A hint', id='myapp.E001'))
    return errors




