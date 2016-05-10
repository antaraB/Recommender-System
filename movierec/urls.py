from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^index$', views.index, name='index2'),
	url(r'^login', views.login, name='login'),
	url(r'^register', views.register, name='register'),
	url(r'^newuser', views.newuser, name='newuser'),
	url(r'^rate$', views.rate, name='rate'),
	url(r'^rated', views.rated, name='rated'),
	url(r'^list', views.list, name='list'),

]