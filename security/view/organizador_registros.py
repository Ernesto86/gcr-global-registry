from django.shortcuts import render
from django.views.generic.base import View

from institutions.models import InsTypeRegistries, Institutions
from security.functions import addUserData
from students.models import StudentRegisters, Students
from system.constants import LOGO_SISTEMA, SISTEMA_PAGINA_WEB, NOMBRE_SISTEMA

class OrganizadorRegistrosView(View):
    template_name = 'security/organizador_registros/view.html'

    def context_common(self):
        context = {}
        context['autor'] = ''
        context['sistema_logo'] = LOGO_SISTEMA
        context['sistema_web'] = SISTEMA_PAGINA_WEB
        context['sistema_nombre'] = NOMBRE_SISTEMA
        return context

    def get(self, request):
        context = {}
        addUserData(self.request, context)
        context['type_registries_list'] = []

        for ins_type_registries in InsTypeRegistries.objects.all():
            registers_level = StudentRegisters.objects.filter(
                type_register_id=ins_type_registries.id,
                institution__created_by=context['usuario'].username
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
        return render(request, self.template_name, context)

    