from django.conf.urls import url
from customers import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.index, name='customer'),
    url(r'^login$', TemplateView.as_view(template_name='customers/login.html'), name='customerLogin'),
    url(r'^register$', TemplateView.as_view(template_name='customers/register.html'), name='customerRegister'),
    url(r'^refer$', views.referPage, name='refer'),
    url(r'^history$', views.historyPage, name='history'),
    url(r'^payment$', views.paymentPage, name='customerPayment'),
]
