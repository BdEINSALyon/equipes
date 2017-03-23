import requests
from django.shortcuts import render

# Create your views here.
from django.template.response import TemplateResponse

from account.models import OAuthToken


def list_azure_groups(request):
    token = OAuthToken.objects.filter(user=request.user).last()
    if token is None:
        return ''
    r = requests.get('https://graph.microsoft.com/v1.0/groups',
                     headers={'Authorization': 'Bearer {}'.format(token.auth_token)})
    return TemplateResponse(request, 'permissions/azure.html', context={'groups': r.json()['value']})
