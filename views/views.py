from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, ListView, DetailView, View, RedirectView, \
    FormView, CreateView, UpdateView, DeleteView
from models.models import Blog
from django.forms import modelform_factory
from django.urls import reverse_lazy, reverse
from . import forms


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


class ClassDetailView(DetailView):
    # обьект выбирается передачей pk или slug из urlconf.
    # По другим полям выборка не работает (можно переопределить в get_object)
    # Указывать где то в этом классе способ выбора не требуется.

    # model = Blog
    # или
    queryset = Blog.objects.all()

    template_name = 'views/classdetailview.html'
    # extra_context = {'data': 'grecha'}

    # по умолчанию, переменная в шаблоне со списком обьектов object_list
    # переопределить можно так:
    context_object_name = 'data'
    # или в get_context_object_name()

    def get_template_names(self, *args, **kwargs):
        temp_name = super().get_template_names(*args, **kwargs)
        # print(temp_name)
        # temp_name = ['views/index.html'] можно заменить шаблон прямо тут
        return temp_name

    def get_queryset(self):
        # если переназначить q то работает только если фильтр в q совпадает с pk из urlconf. иначе 404
        q = super().get_queryset()
        print(q)
        return q

    def get_object(self, queryset=None):
        # обьект для отображения экземпляра классы определяется этим методом
        print(self.kwargs['ug'])
        obj = Blog.objects.get(pk=self.kwargs['ug'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newdata'] = 'New data add through get_context_data'
        return context

    """def get_object(self):
        obj = super().get_object()
        print('get_object')
        obj.tagline = 'Таглайн из get_object'
        obj.save()
        return obj"""


class ClassListView(ListView):
    template_name = 'views/classlistview.html'
    model = Blog
    context_object_name = 'data'  # по умолчанию self.object_list
    paginate_by = 2

    """def get_queryset(self):
        return self.model.objects.short_list()"""


    """def get(self, *args, **kwargs):
        # print('get')
        g = super().get(*args, **kwargs)
        print(g.template_name)
        return g"""


class ClassFormView(FormView):
    template_name = 'views/formview.html'
    form_class = forms.ContactForm
    success_url = reverse_lazy('views:templateresponse')

    def form_valid(self, form):
        # тут можно, например, отправить мейл пользователю.
        # form.send_email()
        print('Все валидно', form.cleaned_data['email'])
        return super().form_valid(form)


class ClassCreateView(CreateView):
    template_name = 'views/createform.html'
    model = Blog
    fields = '__all__'
    success_url = reverse_lazy('views:templateresponse')
    # template_name_suffix = '_create_form'

    def form_valid(self, form):
        # print(self.object) #  обьекта еще нет, возвращает None
        return super().form_valid(form)

    def get_success_url(self):
        # print(self.object.tagline)  # а тут есть, метод вызывается после form_valid
        return super().get_success_url()


class ClassUpdateView(UpdateView):
    template_name = 'views/updateform.html'
    model = Blog
    fields = '__all__'
    success_url = reverse_lazy('views:templateresponse')


class ClassDeleteView(DeleteView):
    template_name = 'views/deleteform.html'
    model = Blog
    fields = '__all__'
    success_url = reverse_lazy('views:templateresponse')