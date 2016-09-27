from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lifestyle$', views.lifestyle, name='lifestyle'),
    url(r'^quickweight$', views.quickweight, name='quickweight')
]