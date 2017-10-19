from django.conf.urls import url

from post.views import post_list, post_add, post_detail, comment_add, post_delete, comment_delete

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'^add/$', post_add, name='post_add'),
    url(r'^(?P<pk>\d+)/$', post_detail, name='post_detail'),
    url(r'^(?P<pk>\d+)/delete/', post_delete, name='post_delete'),
    url(r'^(?P<pk>\d+)/comment/create/', comment_add, name='comment_add'),
    url(r'^(?P<pk>\d+)/comment/delete/', comment_delete, name='comment_delete')
]