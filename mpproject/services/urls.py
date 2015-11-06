from django.conf.urls import url
from django.conf import settings
from services import views
from services.views import DetailsView
from django.views.generic import TemplateView
from services.models import Service

urlpatterns = [
    url(r'^$', views.services, name='services'),
    url(r'^details$', views.details, name='serviceDetails'),
    url(r'^gift$',  TemplateView.as_view(template_name='services/gift.html'), {'prod': not settings.DEBUG}, name='giveGift'),
    url(r'^checkout$', views.checkout, name='serviceCheckout'),
    url(r'^applyCoupon$', views.applyCoupon, name='applyCoupon'),
    url(r'^deleteCoupon$', views.deleteCoupon, name='deleteCoupon'),
    url(r'^orderSuccess$', views.orderSuccess, name='orderSuccess'),
    url(r'^uncaptureCharge$', views.uncaptureCharge, name='uncaptureCharge'),
    url(r'^placeOrderFromJson$', views.placeOrderFromJson, name='placeOrderFromJson'),
    url(r'^placeOrder$', views.placeOrderFromPost, name='placeOrderFromPost'),

    url(r'^In-Home_Swedish_Massage_for_1_Hour$', DetailsView.as_view(context={'service': Service.objects.get(service_type="Swedish Massage", service_time=1), 'prod': not settings.DEBUG}), name='swedishOneHourDetail'),
    url(r'^In-Home_Swedish_Massage_for_1.5_Hours$', DetailsView.as_view(context={'service': Service.objects.get(service_type="Swedish Massage", service_time=1.5), 'prod': not settings.DEBUG})),
    url(r'^In-Home_Deep_Tissue_Massage_for_1_Hour$', DetailsView.as_view(context={'service': Service.objects.get(service_type="Deep Tissue Massage", service_time=1), 'prod': not settings.DEBUG}), name='deepTissueOneHourDetail'),
    url(r'^In-Home_Deep_Tissue_Massage_for_1.5_Hours$', DetailsView.as_view(context={'service': Service.objects.get(service_type="Deep Tissue Massage", service_time=1.5), 'prod': not settings.DEBUG})),
    url(r'^In-Home_Couples_Massage_for_1_Hour$', DetailsView.as_view(context={'service': Service.objects.get(service_type="Couples Massage", service_time=1), 'couple': True, 'prod': not settings.DEBUG})),
    url(r'^In-Home_Couples_Massage_for_1.5_Hours$', DetailsView.as_view(context={'service': Service.objects.get(service_type="Couples Massage", service_time=1.5), 'couple': True, 'prod': not settings.DEBUG})),
    url(r'^In-Home_Sports_Massage_for_1_Hour$', DetailsView.as_view(context={'service': Service.objects.get(service_type="Sports Massage", service_time=1), 'prod': not settings.DEBUG})),
    url(r'^In-Home_Sports_Massage_for_1.5_Hours$', DetailsView.as_view(context={'service': Service.objects.get(service_type="Sports Massage", service_time=1.5), 'prod': not settings.DEBUG})),
    url(r'^In-Home_Shiatsu_Massage_for_1_Hour$', DetailsView.as_view(context={'service': Service.objects.get(service_type="Shiatsu Massage", service_time=1), 'prod': not settings.DEBUG})),
]
