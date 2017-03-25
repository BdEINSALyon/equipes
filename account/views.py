import json

from django import shortcuts


# Create your views here.
from django.conf import settings
from django.contrib.auth import backends
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from account import models


class OAuthLogin(View):
    http_method_names = ['get']

    # noinspection PyMethodMayBeStatic
    def get(self, request, provider):
        service = shortcuts.get_object_or_404(models.OAuthService, name=provider)
        return shortcuts.redirect(
            service.provider.get_authorization_url(
                redirect_uri=request.build_absolute_uri(
                    reverse('oauth_callback', kwargs={"provider": provider})
                )
            ))


class OAuthCallback(View):
    http_method_names = ['get']

    # noinspection PyMethodMayBeStatic
    def get(self, request, provider):
        oauth_service = shortcuts.get_object_or_404(models.OAuthService, name=provider)
        service = oauth_service.provider
        code = request.GET.get('code', None)
        if code is None:
            return shortcuts.redirect('/')
        token = service.retrieve_token(code, request.build_absolute_uri(
                    reverse('oauth_callback', kwargs={"provider": provider})
                ))
        user = service.login_with_token(token['access_token'], oauth_service)
        if user is not None:
            login(request, user)
        return shortcuts.redirect('/')


class HomeLoginView(TemplateView):
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return shortcuts.redirect(shortcuts.reverse('logged_home'))
        else:
            return super(HomeLoginView, self).get(request, *args, **kwargs)


class LoggedHomeView(LoginRequiredMixin, TemplateView):
    login_url = 'home'
    template_name = 'account/logged.html'

    def get(self, request, *args, **kwargs):
        return shortcuts.redirect(shortcuts.reverse('o365:teams'))
