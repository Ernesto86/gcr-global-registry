from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic.base import View
from weasyprint import HTML

from api import settings
from core.common.filter_query.filter_query_common import FilterQueryCommon
from core.services.recaptcha.recaptcha_service import RecaptchaService
from institutions.models import InsTypeRegistries
from security.functions import addUserData
from students.models import StudentRegisters, Students
from system.models import SysCountries


class QueryGeneralView(View):
    template_name = 'security/query_general/view.html'

    def context_common(self):
        context = {}
        addUserData(self.request, context)
        context['sys_country_list'] = SysCountries.objects.filter(deleted=False)
        context['recaptcha_site_key'] = RecaptchaService.get_recaptcha_site_key()
        return context

    def get(self, request):
        context = self.context_common()
        return render(request, self.template_name, context)

    def post(self, request):
        context = self.context_common()
        country = self.request.POST.get("country", None)
        recaptcha = FilterQueryCommon.get_param_validate(self.request.POST.get("g-recaptcha-response", None))
        context['country'] = int(country) if country else country

        dni = self.request.POST.get("identification", "")
        context['identification'] = dni

        validate_recaptcha = RecaptchaService(recaptcha).validate_facade()
        if not validate_recaptcha[0]:
            context['errors'] = [validate_recaptcha[1]]
            return render(request, self.template_name, context)

        context['student_registers_list'] = []
        context['student'] = None

        if country is not None and dni != "":

            try:
                student = Students.objects.select_related(
                    'country'
                ).get(
                    dni=dni,
                    country_id=country
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
                                "detail": ins_type_registries.detail,
                                "color": ins_type_registries.color,
                                "student_registers_list": student_registers_level_list,
                            }
                        )

        return render(request, self.template_name, context)


class CertificateStudentRegisterView(View):
    template_name = 'security/query_general/certificate_student_register.html'

    def get(self, request):
        try:
            student_registers = StudentRegisters.objects.select_related(
                "student",
                "certificate",
                "institution",
                "country",
            ).get(
                id=request.GET.get('student_register_id')
            )
            student = student_registers.student
            certificate = student_registers.certificate
            institution = student_registers.institution
            country = student_registers.country
            type_register = student_registers.type_register

            context = {
                'title': "Certificados",
                'number': student_registers.code_international_register,
                'student': {
                    "names": student.names,
                    'dni': student.dni,
                },
                'institution': {
                    'name': institution.name
                },
                'type_register': {
                    "name": type_register.name
                },
                'certificate': {
                    "name": certificate.name
                },
                'country': {
                    "name": country.name
                },
                'date_issue': student_registers.date_issue_display(),
                'name_specific': "título" if student_registers.is_degree() else "curso",
                'logo': "{}{}".format(settings.MEDIA_URL, 'img/logo/logo-acta100.png'),
            }

            # html_string = render_to_string(self.template_name, context)
            # html_string = render_to_string(self.template_name, context, request=request)
            # html = HTML(string=html_string, base_url=request.build_absolute_uri())

            template = get_template(self.template_name)
            html_template = template.render(context).encode(encoding="UTF-8")
            # base_url = os.path.dirname(os.path.realpath(__file__))

            html = HTML(
                string=html_template,
                # string=html_string,
                base_url=request.build_absolute_uri(),
                # base_url=request.build_absolute_uri("/"),
                # base_url=settings.BASE_DIR,
                # base_url=base_url
            )
            pdf = html.write_pdf(
                stylesheets=[
                    # CSS(os.path.join(settings.BASE_DIR, f'static/v2/css/hope-ui.min.css')),
                    # CSS(os.path.join(settings.BASE_DIR, f'static/v2/css/pro.min.css')),
                ]
            )

            return HttpResponse(pdf, content_type='application/pdf')
        except Exception as ex:
            print(ex)
            print(settings.BASE_DIR)
            pass
        return redirect('home')
