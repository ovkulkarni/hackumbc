from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index_view, name="index"),
    url(r'^test/$', views.test_view, name="test"),
]
