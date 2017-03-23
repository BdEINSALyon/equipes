from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


# Create your models here.
from account import providers


class OAuthToken(models.Model):

    class Meta:
        verbose_name = _('Jeton OAuth')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tokens', verbose_name=_('utilisateur'))
    service = models.ForeignKey('OAuthService', related_name='tokens', verbose_name=_('service'))
    auth_token = models.TextField()
    uuid = models.CharField(max_length=250, default='', blank=True)
    auth_token_expiration = models.DateTimeField(null=True, blank=True)
    renew_token = models.CharField(max_length=250, null=True, blank=True)
    renew_token_expiration = models.DateTimeField(null=True, blank=True)


class OAuthService(models.Model):

    class Meta:
        verbose_name = _('Service OAuth')

    PROVIDERS = {
        'microsoft': providers.MicrosoftOAuthProvider
    }
    PROVIDERS_CHOICES = (
        ('microsoft', _('Microsoft')),
    )

    display_name = models.CharField(max_length=250, verbose_name=_('nom'))
    name = models.CharField(max_length=250, verbose_name=_('identifiant'),
                            choices=PROVIDERS_CHOICES, null=False, blank=False)
    application_id = models.CharField(max_length=250, verbose_name=_('application id'))
    application_secret = models.CharField(max_length=250, verbose_name=_('application secret'))
    enabled = models.BooleanField(verbose_name=_('actif'))
    __provider = None

    @property
    def provider(self):
        if self.__provider is None:
            self.__provider = self.PROVIDERS[self.name](self.application_id, self.application_secret)
        return self.__provider

    def __str__(self):
        return self.display_name
