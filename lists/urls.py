from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^lists/new$', views.new_list, name='new_list'),
    url(r'^lists/(?P<list_id>[0-9]+)/$', views.view_list, name='view_list'),
    url(r'^lists/(?P<list_id>[0-9]+)/add_item$', views.add_item, name='add_item'),
]
