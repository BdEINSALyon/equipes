from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from o365.microsoft import Microsoft
from o365.mixins import MicrosoftTeamMixin


class TeamsView(LoginRequiredMixin, TemplateView):
    template_name = 'o365/teams/teams.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['teams'] = Microsoft().list_teams()
        return data


class RegisterMembersTeamView(MicrosoftTeamMixin, LoginRequiredMixin, View):
    template_name = 'import/register_user.html'
    http_method_names = ['post']

    def post(self, request, gid):
        m = Microsoft()
        users = [u.split(';') for u in request.POST['data'].split('\n')]
        for user in users:
            try:
                m.create_user(user[0], user[1])
            except IndexError:
                pass
        return redirect(reverse('o365:team', args=gid))


class TeamView(LoginRequiredMixin, TemplateView):
    template_name = 'o365/teams/team.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['team'] = Microsoft().get_team(kwargs['gid'])
        data['members'] = Microsoft().get_members_of_team(kwargs['gid'])
        for i in range(0, len(data['members'])):
            odata_type = data['members'][i]['@odata.type']
            if odata_type == '#microsoft.graph.group':
                data['members'][i]['type'] = 'group'
            elif odata_type == '#microsoft.graph.user':
                data['members'][i]['type'] = 'user'
        return data


class ClearTeamView(MicrosoftTeamMixin, LoginRequiredMixin, TemplateView):
    template_name = 'o365/teams/clear_team.html'
    http_method_names = ['get', 'post']

    def post(self, _, gid):
        team = self.get_team(gid)
        members = self.api.get_members_of_team(gid)
        for member in members:
            if member['@odata.type'] == '#microsoft.graph.user':
                self.api.remove_member_from_team(member, team)
        return redirect(reverse('o365:team', kwargs={'gid': gid}))
