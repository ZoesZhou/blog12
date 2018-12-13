from django.conf.urls import url
from .views import pub
from .views import get
from .views import getall


# post
# 不能区分方法，到某方法内部再判断它访问那些路径才能分得开
# 要到view里面再判断
# url(r'^$', pub),
# url(r'^$', get),
urlpatterns = [
    url(r'^pub$', pub),
    url(r'^(\d+)$', get),
    url(r'^$', getall)
]

