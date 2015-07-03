from django.conf.urls import url
from referral import views
urlpatterns = [
    url(r'^$', views.index, name='referral'),
    url(r'^code$', views.referralCode, name='referralCode'),
]
