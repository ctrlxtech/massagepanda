from django.conf.urls import url
from django.contrib.auth import views as auth_views
from customers import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'template_name': 'customers/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'customers/login.html'}, name='password_reset_complete'),
    url(r'^verified/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.verifyCustomer, name='signup_validation_confirm'),
    url(r'^$', views.index, name='customer'),
    url(r'^createCustomerFromJson$', views.createCustomerFromJson, name='createCustomerFromJson'),
    url(r'^createCustomer$', views.createCustomerFromForm, name='createCustomerFromForm'),
    url(r'^login$', views.loginView, name='customerLogin'),
    url(r'^logout$', views.logoutView, name='logoutView'),
    url(r'^userLogin$', views.loginFromForm, name='userLoginFromForm'),
    url(r'^userLoginFromJson$', views.loginFromJson, name='userLogin'),
    url(r'^register$', views.registerView, name='customerRegister'),
    url(r'^changePassword$', views.changePassword, name='changePassword'),
    url(r'^resetPassword$', views.resetPassword, name='resetPassword'),
    url(r'^addNewAddress$', views.addNewAddress, name='addNewAddress'),
    url(r'^deleteAddress$', views.deleteAddress, name='deleteAddress'),
    url(r'^setDefaultAddress$', views.setDefaultAddress, name='setDefaultAddress'),
    url(r'^addNewPayment$', views.addNewPayment, name='addNewPayment'),
    url(r'^deletePayment$', views.deletePayment, name='deletePayment'),
    url(r'^refer$', views.referPage, name='refer'),
    url(r'^history$', views.historyPage, name='history'),
    url(r'^payment$', views.paymentPage, name='customerPayment'),
]
