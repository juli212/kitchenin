from django.conf.urls import url
from . import views

app_name = 'lists'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<list_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<list_id>[0-9]+)/add_item/$', views.add_item, name='add_item'),
	url(r'^create/$', views.create, name='create'),
	url(r'^(?P<list_id>[0-9]+)/members/$', views.members, name='members'),
	url(r'^(?P<list_id>[0-9]+)/find_member/$', views.find_member, name='find_member'),
	url(r'^(?P<list_id>[0-9]+)/add_member/$', views.add_member, name='add_member'),
	url(r'^(?P<list_id>[0-9]+)/remove_member/$', views.remove_member, name='remove_member'),
	url(r'^(?P<list_id>[0-9]+)/leave_list/$', views.leave_list, name='leave_list'),
]