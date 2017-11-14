from django.conf.urls import url, include

from ..urls import views

urlpatterns = [
    url(r'', include(views)),

]