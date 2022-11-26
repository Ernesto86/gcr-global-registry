import json
import os

import requests
from django.shortcuts import render
from django.views.generic.base import View

from core.common.filter_query.filter_query_common import FilterQueryCommon
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
        context['recaptcha_site_key'] = os.environ.get('RECAPTCHA_SITE_KEY', '')
        return context

    def get(self, request):
        context = self.context_common()
        return render(request, self.template_name, context)

    def post(self, request):
        context = self.context_common()
        country = self.request.POST.get("country", None)
        recaptcha = FilterQueryCommon.get_param_validate(self.request.POST.get("g-recaptcha-response", None))
        recaptcha_secret_key = os.environ.get('RECAPTCHA_SECRET_KEY', '')
        context['country'] = int(country) if country else country

        dni = self.request.POST.get("identification", "")
        context['identification'] = dni

        recaptcha_data = {
            "secret": recaptcha_secret_key,
            "response": recaptcha
        }

        try:
            response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify?secret={}&response={}'.format(
                    recaptcha_secret_key,
                    recaptcha
                ),
                data=json.dumps(recaptcha_data)
            )
        except Exception as e:
            context['errors'] = ["Error de captcha"]
            return render(request, self.template_name, context)

        if response.status_code != 200:
            context['errors'] = ["Error de captcha"]
            return render(request, self.template_name, context)

        response_json = response.json()

        if not response_json['success']:
            context['errors'] = ["Error de captcha"]
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
