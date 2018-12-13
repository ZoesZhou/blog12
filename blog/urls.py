"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import loader
from django.template.backends.django import Template
from django.shortcuts import render
import datetime
from user.views import reg


class School:
    def __init__(self):
        self.name = 'zoes'


# def foo():
#     for i in range(1, 10):
#         for j in range(1, 10):
#             print('{}x{}={}'.format(i, j, i * j), end=' ')
#         print()


def index(request: HttpRequest):
    context = {
        'school': School(),
        'name': 'Zoes',
        'testlist': list(range(10, 20)),
        'testdict': {'a': 100, 'b': 200, 'c': School(), 'd': list(range(1, 8)), 'e': None},
        'my_dict': {
            'a': 100, 'b': 0, 'c': list(range(10, 20)),
            'd': 'abd', 'date': datetime.datetime.now()
        },
        'new_list': list(range(1, 10)),
        'jj': 'foo'

    }
    return render(request, 'index.html', context, status=201)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'index$', index),
    url(r'^$', index),
    # url(r'user/reg$', reg)
    url(r'^user/', include('user.urls')),
    url(r'^post/', include('post.urls')),
]
