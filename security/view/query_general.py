import json
import os
import requests

from django.shortcuts import render
from django.views.generic.base import View
from rest_framework import status

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
