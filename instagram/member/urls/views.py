from django.conf.urls import url

from member.views import auth, auth_facebook, profile, relations

urlpatterns = [
    url(r'^signup/$', auth.signup, name='signup'),
    url(r'^login/$', auth.login, name='login'),
    url(r'^logout/$', auth.logout, name='logout'),
    url('^(?P<pk>\d+)/profile/$', profile, name='profile'),
    url('^facebook-login/$', auth_facebook.facebook_login, name='facebook_login'),
]

