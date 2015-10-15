from django.conf.urls import url
from manager import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.index, name='manager'),
    url(r'^send$', views.send, name='sendSMS'),
    url(r'^logs$', views.logs, name='logs'),
    url(r'^logsByNum$', views.logsByNum, name='logsByNum'),
    url(r'^forwardLogs$', views.forwardLogs, name='forwardLogs'),
    url(r'^getForwardLogs$', views.getForwardLogs, name='getForwardLogs'),
    url(r'^getOldInLogs$', views.getOldInLogs, name='getOldInLogs'),
    url(r'^getNewInLogs$', views.getNewInLogs, name='getNewInLogs'),
    url(r'^getOldOutLogs$', views.getOldOutLogs, name='getOldOutLogs'),
    url(r'^getNewOutLogs$', views.getNewOutLogs, name='getNewOutLogs'),
    url(r'^getUserInLogs$', views.getUserInLogs, name='getUserInLogs'),
    url(r'^getUserOutLogs$', views.getUserOutLogs, name='getUserOutLogs'),
    url(r'^getInLogsByNum$', views.getInLogsByNum, name='getInLogsByNum'),
    url(r'^getOutLogsByNum$', views.getOutLogsByNum, name='getOutLogsByNum'),
    url(r'^configurations$', views.configurations, name='configurations'),
    url(r'^applyConfig$', views.applyConfig, name='applyConfig'),
    url(r'^receiveSMS', views.receiveSMS, name='receiveSMS'),
    url(r'^getContactList', views.getContactList, name='getContactList'),
    url(r'^sendEmail$', views.sendEmail, name='sendEmail'),
    url(r'^sendMyEmail$', views.sendMyEmail, name='sendMyEmail'),
    url(r'^sendFeedbackEmails$', views.sendFeedbackEmails, name='sendFeedbackEmails'),
    url(r'^assignTherapist$', views.assignTherapist, name='assignTherapist'),
    
    url(r'^payment', views.payment, name='mpayment'),
    url(r'^charge', views.mcharge, name='mcharge'),
    url(r'^orders$', views.orders, name='orders'),
    url(r'^getOrders$', views.getOrders, name='getOrders'),
    url(r'^profile$', views.customerProfile, name='customerProfile'),
    url(r'^register$', views.register_view, name='registerView'),
    url(r'^tregister$', views.tregister_view, name='tregister'),
    url(r'^createTherapist$', views.createTherapist, name='createTherapist'),
    url(r'^test$', views.test, name='test'),
    url(r'^getOrderlist$', views.orderlisttest, name='orderlisttest'),
    url(r'^getSchedule$', views.getSchedule, name='schedule'),
    url(r'^referralTest$', views.referralTest, name='referralTest'),
]
