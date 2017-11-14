from django.conf.urls import url

from post.apis import PostList

urlpatterns = [
    url(r'^api/posts/$', PostList.as_view(), name='api-posts'),
]