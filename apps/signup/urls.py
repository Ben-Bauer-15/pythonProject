from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^signup$', views.signup),
    url(r'^create$', views.create),
    url(r'^add_set$', views.add_set)
    # url(r'^send_mail$', views.send_mail)
] 