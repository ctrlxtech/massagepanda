from django.conf.urls import url, include
from customers import views
from django.views.generic import TemplateView

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='customer'),
    url(r'^createCustomerFromJson$', views.createCustomerFromJson, name='createCustomerFromJson'),
    url(r'^createCustomerFromForm$', views.createCustomerFromForm, name='createCustomerFromForm'),
    url(r'^login$', TemplateView.as_view(template_name='customers/login.html'), name='customerLogin'),
    url(r'^logout$', views.logout_view, name='logoutView'),
    url(r'^userLoginFromForm$', views.loginFromForm, name='userLoginFromForm'),
    url(r'^userLogin$', views.loginFromJson, name='userLogin'),
    url(r'^register$', TemplateView.as_view(template_name='customers/register.html'), name='customerRegister'),
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
