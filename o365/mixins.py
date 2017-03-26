from django.views.generic.base import ContextMixin

from o365.microsoft import Microsoft


class MicrosoftMixin:

    api = Microsoft()


class MicrosoftTeamMixin(MicrosoftMixin, ContextMixin):

    def get_team(self, gid):
        return self.api.get_team(gid)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['team'] = self.get_team(kwargs['gid'])
        return data
