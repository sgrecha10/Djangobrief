from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, ListView, DetailView, View, RedirectView
from models.models import Blog
from django.forms import modelform_factory
from django.urls import reverse_lazy, reverse


# my middleware
def template_response_middleware(get_request):
    def middleware(request):
        response = get_request(request)
        # приходится передавать templatesresponse потому что class-based views тоже генерят обьекты TemplateResponse, а не HttpResponse  (внезапно!)
        # print(response.context_data.get('templatesresponse'))
        if isinstance(response, TemplateResponse):
            if response.context_data.get('templatesresponse', False):
                response.template_name = 'views/test2.html'
                response.content = response.rendered_content
        return response  # если этот мидлвер подключен первым в списке мидлверс, то обернуть этот response вот так: HttpResponse(response). А иначе браузер будет бесконечно ждать конца response
    return middleware


# колбек после рендера
def my_render_callback(request):
    print('my_render_callback')


# Create your views here.
def template_response(request):
    response = TemplateResponse(request, 'views/index.html', {'data': 'context', 'templatesresponse': True})
    response.add_post_render_callback(my_render_callback)
    print('hi')
    return response


class ClassView(View):
    def get(self, *args, **kwargs):
        form = modelform_factory(Blog, fields='__all__')
        return render(self.request, 'views/classview.html', {'data': form})

    def post(self, *args, **kwargs):
        MyForm = modelform_factory(Blog, fields='__all__')
        form = MyForm(self.request.POST)
        if form.is_valid():
            form.save()
            return redirect('views:classview')
        return render(self.request, 'views/classview.html', {'data': form})


class ClassTemplateView(TemplateView):
    template_name = 'views/classtemplateview.html'
    extra_context = {'data': 'extra_context'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context = {'data': 'get_context'}
        print('get_con')
        return context


class ClassRedirectView(RedirectView):
    url = reverse_lazy('views:classview')


"""class ClassBasedViews(DetailView):
    
    # model = Blog
    # или
    queryset = Blog.objects.all()

    template_name = 'views/classview.html'
    # extra_context = {'data': 'grecha'}
    # по умолчанию, переменная в шаблоне со списком обьектов object_list
    # что бы переопределить название:
    context_object_name = 'data'


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['newdata'] = 'New data add through get_context_data'
        return context


    def get_object(self):
        obj = super().get_object()
        print('get_object')
        obj.tagline = 'Таглайн из get_object'
        obj.save()
        return obj

    # этот метод вызывается при запросе get. есть соотв. методы для запросов head, post и других
    #def get(self, *args, **kwargs):
    #    return HttpResponse('get')
"""
