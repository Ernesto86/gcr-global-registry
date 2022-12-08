from django.views.generic import CreateView, TemplateView
from security.mixins import PermissionMixin
from institutions.models import InsTypeRegistries
from security.functions import addUserData
from students.models import StudentRegisters


class OrganizadorRegistrosView(PermissionMixin, TemplateView):
    template_name = 'security/organizador_registros/view.html'
    permission_required = 'view_studentregisters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['type_registries_list'] = []

        for ins_type_registries in InsTypeRegistries.objects.all():
            registers_level = StudentRegisters.objects.filter(
                type_register_id=ins_type_registries.id,
                institution_id=context['user'].institution_id
            ).count()

            if registers_level:
                context['type_registries_list'].append(
                    {
                        "id": ins_type_registries.id,
                        "name": ins_type_registries.name,
                        "detail": ins_type_registries.detail,
                        "color": ins_type_registries.color,
                        "registers_level_count": registers_level,
                    }
                )
        return context
