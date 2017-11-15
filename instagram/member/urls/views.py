from django.conf.urls import url

from .. import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url('^(?P<pk>\d+)/profile/$', views.profile, name='profile'),
    url('^facebook-login/$', views.facebook_login, name='facebook_login'),
    url(r'^front-facebook-login/$',
        views.FrontFacebookLogin.as_view(),
        name='front-facebook-login'),
]
