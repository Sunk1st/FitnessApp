from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lifestyle$', views.lifestyle, name='lifestyle'),
    url(r'^analysis$', views.analysis, name='analysis'),
    url(r'^community$', views.community, name='community'),
    url(r'^quickweight$', views.quickweight, name='quickweight'),
    url(r'^addfood$', views.addfood, name='addfood'),
    url(r'^quickactivity$', views.quickactivity, name='quickactivity'),
    url(r'^quickgoal$', views.quickgoal, name='quickgoal')
]