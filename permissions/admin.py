from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from permissions import models
from permissions.forms import AzureGroupForm


@admin.register(models.AzureGroup)
class AzureGroupAdmin(admin.ModelAdmin):
    form = AzureGroupForm


@admin.register(models.User)
class UserAdmin(UserAdmin):
    list_filter = ('_is_staff', '_is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', '_is_staff', '_is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
