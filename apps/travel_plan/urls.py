from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^travels$', views.user, name='user'),
    url(r'^travels/destination$', views.travel, name='travel'),
    url(r'^travels/add$', views.add, name='add'),




]
