from django.views.generic import TemplateView

from security.functions import addUserData
from security.manager.organizador_registros_manager import OrganizadorRegistrosManager
from security.mixins import PermissionMixin


class OrganizadorRegistrosView(PermissionMixin, TemplateView):
    template_name = 'security/organizador_registros/view.html'
    permission_required = 'view_studentregisters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['type_registries_list'] = OrganizadorRegistrosManager(context['user']).get_type_registries_list()
        return context
