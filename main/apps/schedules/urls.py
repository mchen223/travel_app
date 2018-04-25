from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', home, name = "home"),
    url(r'^add$', add, name='add'),
    url(r'^add_trip$', add_trip, name='add_trip'),
    url(r'^join/(?P<id>\d+)$', join, name='join'),
    url(r'^destination/(?P<id>\d+)$', destination, name='destination'),
    url(r'^leave_trip/(?P<id>\d+)$', leave_trip, name='leave_trip'),
    url(r'^delete_trip/(?P<id>\d+)$', delete_trip, name='delete_trip'),
]
