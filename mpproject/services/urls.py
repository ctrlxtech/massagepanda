from django.conf.urls import url
from services import views
urlpatterns = [
    url(r'^$', views.services, name='services'),
]
