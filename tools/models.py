from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# Create your models here.
class TaggedItem(models.Model):
    tag = models.SlugField()

    # три обязательных поля для обобщенной связи
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id', for_concrete_model=False)

    def __str__(self):
        return self.tag


class MyUser(User):
    tags = GenericRelation(TaggedItem, for_concrete_model=False)

    class Meta:
        proxy = True
