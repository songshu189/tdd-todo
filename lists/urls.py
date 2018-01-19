from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^new$', views.new_list, name='new_list'),
    url(r'^(?P<list_id>[0-9]+)/$', views.view_list, name='view_list'),
]
