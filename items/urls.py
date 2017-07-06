from django.conf.urls import url
from . import views

app_name='items'
urlpatterns = [
	url(r'^(?P<item_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<item_id>[0-9]+)/move/$', views.move, name='move'),
]