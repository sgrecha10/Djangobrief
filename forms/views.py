from django.shortcuts import render, redirect
from . import forms
from django.http import HttpResponse
from . import models
from django.forms import modelform_factory, formset_factory, modelformset_factory, inlineformset_factory
from django.core.files.storage import FileSystemStorage, get_storage_class


# Create your views here.
def uploadfilesmodel(request):
    if request.method == 'POST':
        form = forms.UploadFileModel(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('forms:uploadfilesmodel')
    else:
        form = forms.UploadFileModel()

    uploadfiles = models.Upload.objects.all()
    context = {'form': form, 'uploadfiles': uploadfiles}

    """Для удаления загруженного файла
    a = Upload.objects.get(pk=2)
    a.upfile.delete()
    a.delete()
    """

    """Для отображения media files внести изменения в urls.py"""

    return render(request, 'forms/uploadfilesmodel.html', context)



def uploadfiles(request):
    class Item:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            return self.name

    if request.method == 'POST':
        form = forms.UploadFile(request.POST, request.FILES)
        form.is_valid()
        upfile = form.cleaned_data['upfile']
        cdata = []
        for x in dir(upfile):
            if not (x.startswith("_") or x == 'close' or x =='encoding' or x == 'fileno' or x == 'newlines'):
                i = Item(x)
                i.value = getattr(upfile, x, None)
                cdata.append(i)

        fs = FileSystemStorage()
        filename = fs.save(upfile.name, upfile)
        uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)
        i = Item('uploaded_file_url')
        i.value = uploaded_file_url
        cdata.append(i)
    else:
        form = forms.UploadFile()
        cdata = None


    context = {'form': form, 'cdata': cdata}

    return render(request, 'forms/uploadfiles.html', context)

def inlineformset(request):
    BookFormSet = inlineformset_factory(models.Author, models.BookForInline, fields='__all__', extra=1)
    author = models.Author.objects.get(pk=1)

    if request.method == 'POST':
        formset = BookFormSet(request.POST, instance=author)
        if formset.is_valid():
            formset.save()
            return redirect('forms:inlineformset')
    else:
        formset = BookFormSet(instance=author)

    context = {'formset': formset}
    return render(request, 'forms/inlineformset.html', context)


def setmodelforms(request):
    AuthorFormSet = modelformset_factory(models.Author, fields='__all__', extra=1)

    class ThinAuthorFormSet(AuthorFormSet):
        def __init__(self, *args, **kwargs):
            super().__init__( *args, **kwargs)
            self.queryset = models.Author.objects.filter(name__startswith='С')


    # formset =AuthorFormSet(queryset=models.Author.objects.filter(name__startswith='С'))
    formset = ThinAuthorFormSet()
    context = {'formset': formset}
    return render(request, 'forms/setmodelform.html', context)


def setforms(request):
    """Создаем setform. Создается одной функцией"""
    ContactFormSet = formset_factory(forms.ContactForm, extra=2)
    if request.method == 'POST':
        formset = ContactFormSet(request.POST)
        if formset.is_valid():
            cleaned_data = formset.cleaned_data
            print(formset.cleaned_data)
        else:
            cleaned_data = None
    else:
        formset = ContactFormSet()
        cleaned_data = None

    context = {'formset': formset, 'cleaned_data': cleaned_data}
    return render(request, 'forms/setform.html', context)


def customforms(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
    else:
        form = forms.ContactForm()

    context = {'form': form}
    return render(request, 'forms/customform.html', context)


def modelformsauthor(request, author_id):
    i = models.Author.objects.get(pk=author_id)
    if request.method == 'POST':
        authorform = forms.AuthorForm(request.POST, instance=i)
        if authorform.is_valid():
            authorform.save()
            return redirect('forms:modelforms')
    else:
        authorform = forms.AuthorForm(instance=i)

    context = {'form': authorform, 'author_id': author_id}
    return render(request, 'forms/modelformauthor.html', context)


def modelformbook(request, book_id):
    i = models.Book.objects.get(pk=book_id)
    if request.method == 'POST':
        bookform = forms.BookForm(request.POST, instance=i)
        if bookform.is_valid():
            bookform.save()
            return redirect('forms:modelforms')
    else:
        # bookform = forms.BookForm(instance=i)
        """А можно и создать форму функцией modelform_factory:
        сначала создаем класс формы, а потом экземпляр.
        так можно делать и в forms.py"""
        BookFormFromFunc = modelform_factory(models.Book, fields='__all__')
        bookform = BookFormFromFunc(instance=i)

    context = {'form': bookform, 'book_id': book_id}
    return render(request, 'forms/modelformbook.html', context)


def modelforms(request):

    if request.method == 'POST':
        if any([x.startswith('author-') for x in request.POST.keys()]):
            authorform = forms.AuthorForm(request.POST)

            """хоть save() и проверяет данные в момент сохранения, но при ошибке вызывает ValueError что вызывает 500
            перед сохранением проверять is_valid() что бы вызывалось ValidationError оно штатно обрабатывается"""
            if authorform.is_valid():
                # print(authorform.cleaned_data)
                # i = authorform.save(commit=False)
                # i.name = 'Валера'
                # print(authorform.cleaned_data)
                # i.save()
                # authorform.save_m2m()
                authorform.save()
                return redirect('forms:modelforms')

        else:
            authorform = forms.AuthorForm()

        if any([x.startswith('book-') for x in request.POST.keys()]):
            bookform = forms.BookForm(request.POST)
            if bookform.is_valid():
                bookform.save()
                return redirect('forms:modelforms')
        else:
            bookform = forms.BookForm()



    else:
        authorform = forms.AuthorForm()
        bookform = forms.BookForm()

    authors = models.Author.objects.all()
    books = models.Book.objects.all()

    context = {'authorform': authorform, 'bookform': bookform, 'authors': authors, 'books': books}
    return render(request, 'forms/modelform.html', context)




def usualforms(request):
    context = {}
    if request.method == 'POST':
        form = forms.UsualForm(request.POST)
        form.is_valid()
        for k in form.cleaned_data:
            form[k].myattr = form.cleaned_data[k]
    else:
        form = forms.UsualForm()

    context.update({'form': form})
    # print(context)
    return render(request, 'forms/usualform.html', context)


