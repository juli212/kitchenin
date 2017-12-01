from django.conf.urls import url
from . import views

app_name = 'profiles'
urlpatterns = [
	url(r'^(?P<profile_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<profile_id>[0-9]+)/edit$', views.edit, name='edit'),
]