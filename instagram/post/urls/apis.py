
from django.conf.urls import url

import utils
from .. import apis


urlpatterns = [
    url(r'^$', apis.PostList.as_view(), name='api-post'),
    url(r'^(?P<post_pk>\d+)/like_toggle/$', apis.PostLikeToggle.as_view(), name='api-like-toggle'),
    url(r'^send-message/$', utils.sms.apis.SendSMS.as_view()),
]
