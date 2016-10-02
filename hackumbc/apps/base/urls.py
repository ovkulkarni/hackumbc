from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index_view, name="index"),
    url(r'^info/$', views.info_view, name="info"),
]
