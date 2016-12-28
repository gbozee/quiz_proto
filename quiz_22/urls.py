from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^que/(?P<quiz_id>\d+)$', views.quiz_detail, name='quiz_detail'),
    url(r'^que/$', views.quiz_detail, name='check_answered_question'),
    url(r'^create/$', views.create_quiz, name='create_quiz'),
    url(r'^create/(?P<quiz_id>\w+)/(?P<que_type>mc|tf)/$', views.create_question, name='create_question'),
]
