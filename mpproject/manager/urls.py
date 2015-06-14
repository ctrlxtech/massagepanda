from django.conf.urls import url
from manager import views
urlpatterns = [
    url(r'^$', views.index, name='manager'),
    url(r'^send$', views.send, name='sendSMS'),
    url(r'^logs$', views.logs, name='logs'),
    url(r'^getInLogs$', views.getInLogs, name='getInLogs'),
    url(r'^getOutLogs$', views.getOutLogs, name='getOutLogs'),
    url(r'^getUserInLogs$', views.getUserInLogs, name='getUserInLogs'),
    url(r'^getUserOutLogs$', views.getUserOutLogs, name='getUserOutLogs'),
    url(r'^getUserLogsByNum$', views.getUserLogsByNum, name='getUserLogsByNum'),
    url(r'^configurations$', views.configurations, name='configurations'),
    url(r'^applyConfig$', views.applyConfig, name='applyConfig'),
    url(r'^sendWithNum', views.sendWithNum, name='sendWithNum'),
    url(r'^receiveSMS', views.receiveSMS, name='receiveSMS'),
    url(r'^getContactList', views.getContactList, name='getContactList'),
    
    url(r'^payment', views.payment, name='mpayment'),
    url(r'^charge', views.mcharge, name='mcharge'),
    url(r'^orders$', views.orders, name='orders'),
    url(r'^getOrders$', views.getOrders, name='getOrders'),
    url(r'^placeOrder$', views.placeOrder, name='placeOrder'),
    url(r'^placeOrderFromForm$', views.placeOrderFromForm, name='placeOrderFromForm'),
    url(r'^login$', views.login_view, name='loginView'),
    url(r'^welcome$', views.welcome, name='welcome'),
    url(r'^profile$', views.customerProfile, name='customerProfile'),
    url(r'^logout$', views.logout_view, name='logoutView'),
    url(r'^register$', views.register_view, name='registerView'),
    url(r'^tregister$', views.tregister_view, name='tregister'),
    url(r'^create_customer$', views.createCustomer, name='createCustomer'),
    url(r'^createTherapist$', views.createTherapist, name='createTherapist'),
    url(r'^test$', views.test, name='test'),
    url(r'^logtest$', views.logtest, name='logtest'),
    url(r'^terms$', views.terms, name='terms'),
    url(r'^privacy$', views.privacy, name='privacy'),
]
