from django.conf.urls import url
from .views import reg
from .views import show
from .views import login

urlpatterns = [
    url(r'^reg$', reg),
    url(r'^login$', login),
    url(r'^show$', show)
]

