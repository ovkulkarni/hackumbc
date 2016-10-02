from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^new/$', views.create_new_receipt_view, name="new_receipt"),
    url(r'^edit/(?P<receipt_id>\d+)/$', views.edit_receipt_view, name="edit_receipt"),
    url(r'^view/(?P<receipt_id>\d+)/$', views.receipt_info_view, name="receipt_info"),
]
