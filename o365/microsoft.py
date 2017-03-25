import json

import requests

from account.models import OAuthToken
import unicodedata


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


class Microsoft(object):
    def __init__(self, user):
        self.token = OAuthToken.objects.filter(user=user).last()
        if self.token is None:
            raise AttributeError('Should ba a user with O365 token')

    def get_cdp_group_id(self):
        r = requests.get('https://graph.microsoft.com/v1.0/groups?$filter=startswith(displayName,\'Equipe CdP\')',
                         headers={'Authorization': 'Bearer {}'.format(self.token.auth_token)})
        return r.json()['value'][0]['id']

    def create_user(self, first_name, last_name):
        r = requests.post('https://graph.microsoft.com/v1.0/users',
                          headers={
                              'Authorization': 'Bearer {}'.format(self.token.auth_token),
                              'Content-Type': 'application/json'
                          },
                          data=json.dumps({
                              'accountEnabled': False,
                              'displayName': "{} {}".format(first_name, last_name),
                              'userPrincipalName': strip_accents(
                                  "{}.{}@bde-insa-lyon.fr".format(first_name, last_name)).lower(),
                              'mailNickname': strip_accents(
                                  "{}.{}".format(first_name, last_name)).lower(),
                              'givenName': first_name,
                              'surname': last_name,
                              "passwordProfile": {
                                  "forceChangePasswordNextSignIn": True,
                                  "password": "cdp2017" + first_name
                              }
                          }))
        result = r.json()
        return result

    def list_teams(self):
        r = requests.get('https://graph.microsoft.com/v1.0/groups?$filter=startswith(displayName,\'Equipe \') and securityEnabled eq true',
                         headers={'Authorization': 'Bearer {}'.format(self.token.auth_token)})
        result = r.json()
        return result['value']

    def get_users(self):
        r = requests.get('https://graph.microsoft.com/v1.0/users',
                         headers={'Authorization': 'Bearer {}'.format(self.token.auth_token)})
        return r.json()['value']

    def get_team(self, gid):
        r = requests.get('https://graph.microsoft.com/v1.0/groups/{}'.format(gid),
                         headers={'Authorization': 'Bearer {}'.format(self.token.auth_token)})
        data = r.json()
        return data

    def get_members_of_team(self, gid):
        r = requests.get('https://graph.microsoft.com/v1.0/groups/{}/members'.format(gid),
                         headers={'Authorization': 'Bearer {}'.format(self.token.auth_token)})
        data = r.json()
        return data['value']
