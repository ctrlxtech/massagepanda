from django.conf.urls import url
from feedback import views
urlpatterns = [
    url(r'^email$', views.feedbackEmail, name='feedbackEmail'),
    url(r'^survey/(?P<code>[0-9A-Za-z]{32})/(?P<rating>[1-5]{1})/$', views.feedbackSurvey, name='feedbackSurvey'),
    url(r'^thanks$', views.feedbackConfirm, name='feedbackConfirm'),
]
