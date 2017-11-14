from django.conf.urls import url, include


urlpatterns = [
    url(r'^members/$', include('member.urls.apis', namespace='members')),
    url(r'^posts/$', include('post.urls.apis', namespace='posts')),

]
