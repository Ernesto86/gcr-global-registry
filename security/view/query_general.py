from django.views.generic.base import TemplateView

from institutions.models import InsTypeRegistries
from students.models import StudentRegisters, Students
from system.constants import LOGO_SISTEMA, SISTEMA_PAGINA_WEB, NOMBRE_SISTEMA
from system.models import SysCountries, SysNationality


class QueryGeneralView(TemplateView):
    template_name = 'security/query_general/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['autor'] = ''
        context['sistema_logo'] = LOGO_SISTEMA
        context['sistema_web'] = SISTEMA_PAGINA_WEB
        context['sistema_nombre'] = NOMBRE_SISTEMA
        context['sys_nationality_list'] = SysNationality.objects.all()

        nationality = self.request.GET.get("nationality", None)
        context['nationality'] = int(nationality) if nationality else nationality

        dni = self.request.GET.get("identification", "")
        context['identification'] = dni
        context['character'] = self.request.GET.get("character", "")

        context['student_registers_list'] = []
        context['student'] = None

        if nationality is not None and dni != "":

            try:
                student = Students.objects.select_related(
                    "nationality"
                ).get(
                    dni=dni, nationality_id=nationality
                )
            except Exception as ex:
                student = None

            if student:
                context['student'] = student

                student_registers_list = StudentRegisters.objects.select_related(
                    "institution",
                    "type_register",
                    "certificate",
                    "country"
                ).filter(
                    student_id=student.id
                ).order_by(
                    "-date_issue"
                )

                context[f'type_registries_list'] = []

                for ins_type_registries in InsTypeRegistries.objects.all():

                    student_registers_level_list = student_registers_list.filter(
                        type_register_id=ins_type_registries.id
                    )

                    if student_registers_level_list.count():
                        context['type_registries_list'].append(
                            {
                                "name": ins_type_registries.name,
                                "color": ins_type_registries.color,
                                "student_registers_list": student_registers_level_list,
                            }
                        )

        return context
