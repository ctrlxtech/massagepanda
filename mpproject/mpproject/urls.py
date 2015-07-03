from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'mpproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('index.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^store/', include('services.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^payment/', include('payment.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^referral/', include('referral.urls')),
]
