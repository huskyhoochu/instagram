from django.conf.urls import url

from post.views import post_list, post_add

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'^add/$', post_add, name='post_add')
]