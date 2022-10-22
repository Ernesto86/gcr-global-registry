from django.shortcuts import render
from django.views.generic.base import View

from institutions.models import InsTypeRegistries
from students.models import StudentRegisters, Students
from system.constants import LOGO_SISTEMA, SISTEMA_PAGINA_WEB, NOMBRE_SISTEMA
from system.models import SysNationality


class QueryGeneralView(View):
    template_name = 'security/query_general/view.html'

    def context_common(self):
        context = {}
        context['autor'] = ''
        context['sistema_logo'] = LOGO_SISTEMA
        context['sistema_web'] = SISTEMA_PAGINA_WEB
        context['sistema_nombre'] = NOMBRE_SISTEMA
        context['sys_nationality_list'] = SysNationality.objects.all()
        return context

    def get(self, request):
        context = self.context_common()
        return render(request, self.template_name, context)

    def post(self, request):
        context = self.context_common()
        context['autor'] = ''
        context['sistema_logo'] = LOGO_SISTEMA
        context['sistema_web'] = SISTEMA_PAGINA_WEB
        context['sistema_nombre'] = NOMBRE_SISTEMA
        context['sys_nationality_list'] = SysNationality.objects.all()

        nationality = self.request.POST.get("nationality", None)
        context['nationality'] = int(nationality) if nationality else nationality

        dni = self.request.POST.get("identification", "")
        context['identification'] = dni
        context['character'] = self.request.POST.get("character", "")

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

        return render(request, self.template_name, context)
