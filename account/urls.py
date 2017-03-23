"""accounts URL configuration
"""
from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from account import views

urlpatterns = [
    url(r'^oauth/(?P<provider>[a-z_]*)/callback', views.OAuthCallback.as_view(), name='oauth_callback'),
    url(r'^oauth/(?P<provider>[a-z_]*)/login', views.OAuthLogin.as_view(),  name='oauth_login'),
    url(r'^$', views.HomeLoginView.as_view(), name='home'),
    url(r'^home', views.LoggedHomeView.as_view(), name='logged_home'),
    url(r'^logout$', auth_views.logout, name='logout')
]
