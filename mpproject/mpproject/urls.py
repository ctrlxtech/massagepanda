from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from manager import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'mpproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('index.urls')),
    url(r'^single$', TemplateView.as_view(template_name='index/single.html'), name='single'),
    url(r'^howitworks$', TemplateView.as_view(template_name='index/howItWorks.html'), name='howItWorks'),
    url(r'^faq$', TemplateView.as_view(template_name='index/faq.html'), name='faq'),
    url(r'^terms$', TemplateView.as_view(template_name='index/terms.html'), name='terms'),
    url(r'^privacy$', TemplateView.as_view(template_name='index/privacy.html'), name='privacy'),
    url(r'^about$', TemplateView.as_view(template_name='index/about.html'), name='about'),
    url(r'^contactus$', TemplateView.as_view(template_name='index/contactUs.html'), name='contactUs'),
    url(r'^locationcoverage$', TemplateView.as_view(template_name='index/locationCoverage.html'), name='locationCoverage'),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^store/', include('services.urls')),
    url(r'^payment/', include('payment.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^customer/', include('customers.urls')),
    url(r'^referral/', include('referral.urls')),
]
