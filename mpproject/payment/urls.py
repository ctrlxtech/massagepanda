from django.conf.urls import url
from payment import views
urlpatterns = [
    url(r'^$', views.index, name='payment'),
    url(r'^charge', views.charge, name='charge'),
]
