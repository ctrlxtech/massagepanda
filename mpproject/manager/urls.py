from django.conf.urls import url
from manager import views
urlpatterns = [
    url(r'^$', views.index, name='manager'),
    url(r'^send$', views.send, name='sendSMS'),
    url(r'^logs$', views.logs, name='logs'),
    url(r'^getInLogs$', views.getInLogs, name='getInLogs'),
    url(r'^getOutLogs$', views.getOutLogs, name='getOutLogs'),
    url(r'^getUserInLogs$', views.getUserInLogs, name='getUserInLogs'),
    url(r'^getUserOutLogs$', views.getUserOutLogs, name='getUserOutLogs'),
    url(r'^getUserLogsByNum$', views.getUserLogsByNum, name='getUserLogsByNum'),
    url(r'^configurations$', views.configurations, name='configurations'),
    url(r'^applyConfig$', views.applyConfig, name='applyConfig'),
    url(r'^sendWithNum', views.sendWithNum, name='sendWithNum'),
    url(r'^receiveSMS', views.receiveSMS, name='receiveSMS'),
]
