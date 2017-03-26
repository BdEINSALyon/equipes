import json
import random

import requests
from django.db import Error

from account.models import OAuthToken, OAuthService
import unicodedata


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def generate_password(length=8):
    return ''.join(
        random.SystemRandom().choice("ABCEFGHJKMNPRSTUVabcdefghjkmnprstuv0123456789:=?/%") for _ in range(length))


class Microsoft(object):
    def __init__(self):

        service = OAuthService.objects.filter(name='microsoft').first()
        if service is None:
            raise Error('No Microsoft app to manage AD')

        self.token = service.provider.retrieve_app_token()
        if self.token is None:
            raise AttributeError('Should ba a user with O365 token')

    def get_cdp_group_id(self):
        r = requests.get('https://graph.microsoft.com/v1.0/groups?$filter=startswith(displayName,\'Equipe CdP\')',
                         headers={'Authorization': 'Bearer {}'.format(self.token['access_token'])})
        return r.json()['value'][0]['id']

    def create_user(self, first_name, last_name):
        """
        Create a new user into Directory
        :type first_name: str
        :type last_name: str
        """
        name = "{} {}".format(first_name.capitalize(), last_name.capitalize())
        identifier = "{}.{}".format(strip_accents(first_name.lower()), strip_accents(last_name.lower()))
        upn = "{}@bde-insa-lyon.fr".format(identifier)
        password = generate_password(10)
        r = requests.post('https://graph.microsoft.com/v1.0/users',
                          headers={
                              'Authorization': 'Bearer {}'.format(self.token['access_token']),
                              'Content-Type': 'application/json'
                          },
                          data=json.dumps({
                              'accountEnabled': True,
                              'displayName': name,
                              'userPrincipalName': upn,
                              'mailNickname': identifier,
                              'givenName': first_name,
                              'surname': last_name,
                              "passwordProfile": {
                                  "forceChangePasswordNextSignIn": True,
                                  "password": password
                              }
                          }))
        result = r.json()
        return result, password

    def list_teams(self):
        r = requests.get(
            'https://graph.microsoft.com/v1.0/groups?$filter=' +
            'startswith(displayName,\'Equipe \') and securityEnabled eq true',
            headers={'Authorization': 'Bearer {}'.format(self.token['access_token'])})
        result = r.json()
        return result['value']

    def get_users(self):
        r = requests.get('https://graph.microsoft.com/v1.0/users',
                         headers={'Authorization': 'Bearer {}'.format(self.token['access_token'])})
        return r.json()['value']

    def get_team(self, gid):
        r = requests.get('https://graph.microsoft.com/v1.0/groups/{}'.format(gid),
                         headers={'Authorization': 'Bearer {}'.format(self.token['access_token'])})
        data = r.json()
        return data

    def get_members_of_team(self, gid):
        r = requests.get('https://graph.microsoft.com/v1.0/groups/{}/members'.format(gid),
                         headers={'Authorization': 'Bearer {}'.format(self.token['access_token'])})
        data = r.json()
        return data['value']

    def remove_member_from_team(self, member, team):
        r = requests.delete(
            'https://graph.microsoft.com/v1.0/groups/{}/members/{}/$ref'.format(team['id'], member['id']),
            headers={'Authorization': 'Bearer {}'.format(self.token['access_token'])})
        return r.status_code < 300
