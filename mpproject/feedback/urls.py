from django.conf.urls import url
from feedback import views
urlpatterns = [
    url(r'^email$', views.feedbackEmail, name='feedbackEmail'),
    url(r'^survey$', views.feedbackSurvey, name='feedbackSurvey'),
]
