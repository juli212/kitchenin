from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name='home'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register/', views.register, name='register'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
]