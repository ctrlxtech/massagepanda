from django.conf.urls import url
from services import views
from services.views import DetailsView
from django.views.generic import TemplateView
from services.models import Service

urlpatterns = [
    url(r'^$', views.services, name='services'),
    url(r'^details$', views.details, name='serviceDetails'),
    url(r'^gift$',  TemplateView.as_view(template_name='services/gift.html'), name='giveGift'),
    url(r'^checkout$', views.checkout, name='serviceCheckout'),
    url(r'^applyCoupon$', views.applyCoupon, name='applyCoupon'),
    url(r'^deleteCoupon$', views.deleteCoupon, name='deleteCoupon'),
    url(r'^placeOrder$', views.placeOrderFromJson, name='placeOrderFromJson'),
    url(r'^placeOrderFromPost$', views.placeOrderFromPost, name='placeOrderFromPost'),

]
