from django.db import models
import datetime
from django.db.models import Count


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def get_absolute_url(self):
        return '/%s/' % self.name


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)


"""Ниже другая группа моделей"""

class BlogManager(models.Manager):
    def my_create(self, *args, **kwards):
        print('Мы тут!')
        return super().create(*args, **kwards)

    """def get_queryset(self):
        return super().get_queryset().filter(name__contains='вариант')"""

    def with_counts(self):
        print('мы тут')
        return super().get_queryset().annotate(counts=Count('entry'))

    def short_list(self):
        return self.model.objects.all()[:4]
        # return super().get_queryset()[:3]


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    objects = BlogManager()

    def __str__(self):
        return self.name

    """def clean_fields(self, exclude=None):
        print("Клинфилдс")
        return super().clean_fields(exclude=exclude)

    def clean(self):
        print("Клин")
        return super().clean()"""

    @classmethod
    def createcls(cls, *args, **kwargs):
        print("Сработал классовый метод")
        return cls(*args, **kwargs)

    @property
    def myattr(self):
        return self.name, self.pk


class ThemeBlog(Blog):
    theme = models.CharField(max_length=200)


class Author(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField()

    class Meta:
        #  тут можно и не составные индексы определять, походу самый удобный и наглядный способ.
        index_together = [
            ['name', 'email'],
            ['email'],
        ]

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    text = models.TextField()
    pub_date = models.DateField(default=datetime.date.today)
    mod_date = models.DateField(default=datetime.date.today)
    author = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.headline

    def clean_fields(self, exclude=None):
        print("Клинфилдс")
        return super().clean_fields(exclude=exclude)

    def clean(self):
        print("Клин")
        return super().clean()