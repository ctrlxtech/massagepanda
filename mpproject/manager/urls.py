from django.conf.urls import url
from manager import views
urlpatterns = [
    url(r'^$', views.index, name='manager'),
    url(r'^send$', views.send, name='sendSMS'),
    url(r'^sendWithNum', views.sendWithNum, name='sendWithNum'),
    url(r'^receiveSMS', views.receiveSMS, name='receiveSMS'),
]
