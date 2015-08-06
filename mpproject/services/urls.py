from django.conf.urls import url
from services import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.services, name='services'),
    url(r'^details$', views.details, name='serviceDetails'),
    url(r'^gift$',  TemplateView.as_view(template_name='services/gift.html'), name='giveGift'),
    url(r'^checkout$', views.checkout, name='serviceCheckout'),
]
