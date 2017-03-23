from django import forms
import requests
from account.models import OAuthService


class AzureGroupForm(forms.ModelForm):
    class Meta:
        fields = ('group', 'azure_id')

    @staticmethod
    def get_groups():
        service = OAuthService.objects.filter(name='microsoft').first()
        if service is None:
            return ('', 'Please enable Office 365 for this app'),
        data = requests.get(
            service.provider.graph('/groups?$orderby=displayName'),
            headers={
                'Authorization': 'Bearer {}'.format(service.provider.retrieve_app_token()['access_token'])
            }).json()

        if data.get('error'):
            return ('', 'Error while fetching groups : {}'.format(data.get('error').get('message'))),

        groups = data.get('value', [])
        form_data = []
        for group in groups:
            form_data.append((group['id'], group['displayName']))
        return form_data

    azure_id = forms.ChoiceField(choices=(('', 'Please enable Office 365 for this app'),))

    def __init__(self, *args, **kwargs):
        # receive a tupple/list for custom choices
        super(AzureGroupForm, self).__init__(*args, **kwargs)
        self.fields['azure_id'].choices = AzureGroupForm.get_groups()
