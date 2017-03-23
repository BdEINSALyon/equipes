from django.contrib import admin

from account import models


@admin.register(models.OAuthService)
class OAuthServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OAuthToken)
class OAuthTokenAdmin(admin.ModelAdmin):
    pass
