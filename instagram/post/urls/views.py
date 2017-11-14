from django.conf.urls import url

from post.views import post, comment

urlpatterns = [
    url(r'^$', post.post_list, name='post_list'),
    url(r'^add/$', post.post_add, name='post_add'),
    url(r'^(?P<pk>\d+)/$', post.post_detail, name='post_detail'),
    url(r'^(?P<pk>\d+)/delete/', post.post_delete, name='post_delete'),
    url(r'^(?P<pk>\d+)/comment/create/', comment.comment_add, name='comment_add'),
    url(r'^(?P<pk>\d+)/comment/delete/', comment.comment_delete, name='comment_delete'),
    url(r'^(?P<pk>\d+)/like-toggle/$', post.post_like_toggle, name='post_like_toggle'),
]

