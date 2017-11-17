from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^send-message/$', apis.SendSMS.as_view()),
]
