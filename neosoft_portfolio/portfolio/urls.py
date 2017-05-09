from django.conf.urls import *
from portfolio.feed import ArticlesFeed
from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^projects/(?P<pid>[0-9]+)/$', views.ProjectDetailsView.as_view(), name='project_details'),
    # url(r'^latest/comments/', DreamrealCommentsFeed()),
    url(r'^comments/(?P<pid>[0-9]+)/$',views.comment, name = 'comment'),
    url(r'^latest/comments/a112', ArticlesFeed()),
    url(r'^feed/', views.subscribe_feed,name='feed'),
]