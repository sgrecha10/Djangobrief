from django import forms
import datetime
from . import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.core.validators import validate_email


class UploadFileModel(forms.ModelForm):
    class Meta:
        model = models.Upload
        fields = ['name', 'upfile']


class UploadFile(forms.Form):
    name = forms.CharField(max_length=100)
    upfile = forms.FileField(label='FileField')


# создаем свое поле, принимающее несколько значений емейл разделенных запятой
class MultiEmailField(forms.Field):

    widget = forms.Textarea(attrs={'rows': 3, 'cols': 55})

    def to_python(self, value):
        # raise ValidationError('to_python!')
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        # raise ValidationError('validate!')
        super().validate(value)
        for item in value:
            # print(item.strip())
            validate_email(item.strip())


class ContactForm(forms.Form):
    multiemail = MultiEmailField(help_text='Принимает несколько emeil через запятую')
    name = forms.CharField(required=False)
    datetimefield = forms.DateTimeField(label="DateTimeField",
                                        widget=forms.TextInput(attrs={
                                            'class': 'special',
                                            'type': 'datetime-local'
                                        }),
                                        initial=datetime.datetime.now(),
                                        help_text='datetime-local Bootstrap 4'
                                        )

    def clean_multiemail(self):
        data = self.cleaned_data['multiemail']
        for i in data:
            if i == 'grecha@list.ru':
                raise ValidationError(
                    _('Invalid value: %(value)s'),
                    code='invalid',
                    params={'value': '43'},
            )
        return data

    """def clean(self):
        super().clean()
        data = self.cleaned_data.get('multiemail')
        # raise ValidationError(data)
        # self.add_error('multiemail', data)
        """




class AuthorForm(forms.ModelForm):
    prefix = 'author'

    # собственная проверка поля name
    """def clean_name(self):
        # print('aaaaa')
        name = self.cleaned_data['name']
        if name == '123':
            raise ValidationError("Имя не может быть 123!")
        return name

    def clean_name(self):  # здесь делаем проверку, для одного поля (здесь - name)
        raise ValidationError(
                    _('Invalid value: %(value)s'),
                    code='invalid',
                    params={'value': '42'},
            )

    def clean(self):  # в этом методе делаем проверку если она учитывает значения из нескольких полей
        raise ValidationError("clean!")"""

    class Meta:
        model = models.Author
        fields = ['name', 'title', 'birth_date']
        # exclude = ['name']
        widgets = {
            'name': forms.Textarea(attrs={'cols': 25, 'rows': 2})
        }


"""можно наследовать форму и переопределить проверку в ней. но зачем - не понятно
ибо работает и при переопределении в исходной форме"""
"""class AuthorFormMore(AuthorForm):
    # собственная проверку поля name
    def clean_name(self):
        print('aaaaa')
        name = self.cleaned_data['name']
        if name == '123':
            raise ValidationError("Имя не может быть 123!")

        return name"""


class BookForm(forms.ModelForm):
    prefix = 'book'
    class Meta:
        model = models.Book
        fields = ['name', 'authors']



class UsualForm(forms.Form):
    """по умолчанию эти две настройки (почти) нормально работают только в .as_table()
    но если форму вывожу в шаблон поэлементно - то в нужном месте можно вставить
    item.css_classes и тогда в этом месте будут классы в соответсвии с этими настройками"""
    error_css_class = "error123"  # работает в контейнере
    required_css_class = "field123"  # работает в элементе

    booleanfield = forms.BooleanField(required=False, label="BooleanField")
    charfield = forms.CharField(max_length=5, label="CharField", required=True,
                                widget=forms.TextInput(attrs={'class': 'anna'}))

    YEAR_IN_SCHOOL_CHOICES = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    ]
    choicefield = forms.ChoiceField(choices=YEAR_IN_SCHOOL_CHOICES, label="ChoiceField")

    typedchoicefield = forms.TypedChoiceField(choices=YEAR_IN_SCHOOL_CHOICES, coerce=str, label="TypedChoiceField")
    datefield = forms.DateField(initial=datetime.datetime.now(), label="DateField")
    datetimefield = forms.DateTimeField(initial=datetime.datetime.now(), label="DateTimeField")
    decimalfield = forms.DecimalField(required=True, max_digits=4, decimal_places=2, label='DecimalField',
                                      error_messages={'max_digits': 'Слишком много цифр!'})
    durationfield = forms.DurationField(required=False, label="")
    emailfield = forms.EmailField(required=False, label="DurationField")
    # filefield = forms.FileField(label="FileField")
    # filepathfield = forms.FilePathField(label="FilePathField")
    floatfield = forms.FloatField(required=False, label="FloatField")
    # imagefield = forms.ImageField(label="ImageField")
    integerfield = forms.IntegerField(required=False, label="IntegerField")
    genericipaddresfield = forms.GenericIPAddressField(required=False, label="GenericIPAddressField")
    multiplechoicefield = forms.MultipleChoiceField(choices=YEAR_IN_SCHOOL_CHOICES, required=False,
                                                    label="MultipleChoiceField")
    typedmultiplechoicefield = forms.TypedMultipleChoiceField(choices=YEAR_IN_SCHOOL_CHOICES,
                                                              required=False, coerce=str,
                                                              label="TypedMultipleChoiceField")
    nullbooleanfield = forms.NullBooleanField(label="NullBooleanField")
    # regexfield = forms.RegexField(label="RegexField")
    slugfield = forms.SlugField(required=False, allow_unicode=True, label="SlugField")
    timefield = forms.TimeField(initial=datetime.datetime.now(), label="TimeField")
    urlfield = forms.URLField(required=False, label="URLField")
    uuidfield = forms.UUIDField(required=False, label="UUIDField")

    # Достаточно сложные встроенные классы Field
    combofield = forms.ComboField(help_text='валидируется по нескольким полям', required=False, label="ComboField",
                                  fields=[forms.CharField(max_length=10), forms.EmailField()])
    # multivaluefield = forms.MultiValueField(label="MultiValueField")

    splitdatetimefield = forms.SplitDateTimeField(initial=datetime.datetime.now(), label="SplitDateTimeField")

    # Поля для обработки связей
    # modelchoicefield = forms.ModelChoiceField(label="ModelChoiceField")
    # modelmultiplechoicefield = forms.ModelMultipleChoiceField(label="ModelMultipleChoiceField")

    # Создание собственных полей в customforms

