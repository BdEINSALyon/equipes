from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from o365.microsoft import Microsoft


class TeamsView(LoginRequiredMixin, TemplateView):
    template_name = 'import/templates/o365/teams/teams.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['teams'] = Microsoft(self.request.user).list_teams()
        return data


class RegisterUsers(LoginRequiredMixin, TemplateView):
    template_name = 'import/register_user.html'
    http_method_names = ['get', 'post']

    def post(self, request, *args, **kwargs):
        m = Microsoft(self.request.user)
        users = [u.split(';') for u in request.POST['data'].split('\n')]
        for user in users:
            try:
                m.create_user(user[0], user[1])
            except IndexError:
                pass
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cdp'] = Microsoft(self.request.user).get_cdp_group_id()
        data['users'] = Microsoft(self.request.user).get_users()
        return data


class TeamView(LoginRequiredMixin, TemplateView):
    template_name = 'o365/teams/team.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['team'] = Microsoft(self.request.user).get_team(kwargs['gid'])
        data['members'] = Microsoft(self.request.user).get_members_of_team(kwargs['gid'])
        for i in range(0, len(data['members'])):
            odata_type = data['members'][i]['@odata.type']
            if odata_type == '#microsoft.graph.group':
                data['members'][i]['type'] = 'group'
            elif odata_type == '#microsoft.graph.user':
                data['members'][i]['type'] = 'user'
        return data
