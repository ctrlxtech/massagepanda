from django.conf.urls import url
from payment import views
urlpatterns = [
    url(r'^$', views.index, name='payment'),
    url(r'^charge', views.charge, name='charge'),
    url(r'^buy', views.buy, name='buy'),
    url(r'^test', views.test, name='test'),
    url(r'^processOrder', views.processOrder, name='processOrder'),
]
