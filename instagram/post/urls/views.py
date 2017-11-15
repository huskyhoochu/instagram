from django.conf.urls import url

from .. import views

urlpatterns = [
    # post
    url(r'^$', views.post.post_list, name='post_list'),
    url(r'^add/$', views.post.post_add, name='post_add'),
    url(r'^(?P<pk>\d+)/$', views.post.post_detail, name='post_detail'),
    url(r'^(?P<pk>\d+)/delete/', views.post.post_delete, name='post_delete'),
    url(r'^(?P<pk>\d+)/like-toggle/$', views.post.post_like_toggle, name='post_like_toggle'),

    # comment
    url(r'^(?P<pk>\d+)/comment/create/', views.comment.comment_add, name='comment_add'),
    url(r'^(?P<pk>\d+)/comment/delete/', views.comment.comment_delete, name='comment_delete'),
]

