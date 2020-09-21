from django.shortcuts import render
from django.http import HttpResponse
from . import models

# Create your views here.
def index(request):
    from django.db.models import Prefetch

    """entrys = models.Entry.objects\
        .select_related('blog').prefetch_related('author')\
        .only('headline', 'blog__name', 'author__name')"""

    """entrys = models.Entry.objects\
        .select_related('blog')\
        .prefetch_related(Prefetch('author', queryset=models.Author.objects.only('name').order_by('-pk')))\
        .only('headline', 'blog__name')"""

    """entrys = models.Entry.objects\
        .select_related('blog')\
        .prefetch_related(
            Prefetch('author', to_attr='myattr'),
            Prefetch('author', queryset=models.Author.objects.order_by('-pk'), to_attr='rev'),
        )\
        .only('headline', 'blog__name')"""

    entrys = models.Entry.objects\
        .select_related('blog')\
        .prefetch_related(
            Prefetch('author', to_attr='myattr'),
        )\
        .only('headline', 'blog__name')


    # Если в запросе нет prefetch_relative, но есть select_relative - то его ОЧЕНЬ
    # удобно заменять  .values Это добавляет и JOIN и лучше всего ограничивает выборку полей одним махом
    # entrys = models.Entry.objects.values('headline', 'blog__name')
    # почти аналогично
    # (только две небольших разницы:
    # 1. в шаблоне отображения, blog__name и blog.name)
    # 2. два лишних поля по сравнению с values()
    # entrys = models.Entry.objects.select_related('blog').only('headline', 'blog__name')

    blogs = models.Blog.objects.prefetch_related(
        Prefetch('entry_set__author', to_attr='authors'),
    )

    authors = models.Author.objects.prefetch_related('entry_set__blog')

    context = {'entrys': entrys, 'blogs': blogs, 'authors': authors}
    return render(request, 'models/index.html', context)