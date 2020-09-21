from django.db import models

TITLE_CHOICES = [
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
]


# Create your models here.
class Upload(models.Model):
    name = models.CharField(max_length=100)
    upfile = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.name


class BookForInline(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
