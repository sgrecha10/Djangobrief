"""djangobrief URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


# для media files
from django.conf.urls.static import static
from django.conf import settings
# для media files конец

from django.http import HttpResponse

handler403 = 'template.views.response_error_handler'
handler404 = lambda request, exception: HttpResponse('привет')

urlpatterns = [
    path('request/', include('request.urls')),
    path('forms/', include('forms.urls')),
    path('models/', include('models.urls')),
    path('template/', include('template.urls')),
    path('views/', include('views.urls')),
    path('myauth/', include('myauth.urls')),
    path('admin/', admin.site.urls),
]
# для отображения media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns