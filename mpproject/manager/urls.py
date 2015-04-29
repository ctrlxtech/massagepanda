from django.conf.urls import url
from manager import views
urlpatterns = [
    url(r'^$', views.index, name='manager'),
    url(r'^send', views.send, name='sendSMS'),
]
