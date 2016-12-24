from django.conf.urls import url
from . import views

'''

The routes used in this app are simple and easily acccessible. None require an argument of any sort

'''

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout')
]
 