from django.shortcuts import render
from django.http import HttpResponse
from forms import views


# Create your views here.
def index(request):

    class Obj:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            return self.name


    data = []
    for item in dir(request):
        if not item.startswith('_'):
            o = Obj(item)
            o.value = getattr(request, item)
            if callable(o.value): o.type = 'm'
            else: o.type = 'a'
            data.append(o)

    data.sort(key=lambda x: x.type)

    context = {'data': data}

    """var = 'path'
    
    f = getattr(request, var)
    if callable(f):
        print(f())
    else:
        print(f)"""

    #print(callable(request.scheme))
    return render(request, 'request/index.html', context)

