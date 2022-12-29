import datetime
from urllib.parse import urlencode

from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView

from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.util_functions import ListViewFilter
from institutions.models import InsTypeRegistries
from security.functions import addUserData
from students.models import StudentRegisters, StudentRegistersRenovationHistory
from system.models import SysParameters
from transactions.manager.shopping_cart_manager import ShoppingCartManager
from transactions.models import InstitutionQuotesTypeRegister


class OrganizadorRegistroListView(ListViewFilter, LoginRequiredMixin, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'security/organizador_registros/listado.html'
    context_object_name = 'StudentRegisters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        ins_type_registries = InsTypeRegistries.objects.get(id=self.kwargs.get("typeregisterid"))
        context['title_label'] = f'Registros de {ins_type_registries.name} - {ins_type_registries.detail}'.upper()
        context['clear_url'] = reverse_lazy('organizador_detalle', kwargs={'typeregisterid': ins_type_registries.id})

        get_params = FilterOrmCommon.get_url_params(self.request.GET)
        context.update(get_params)
        context['url_params'] = urlencode(get_params)
        return context

    def get_queryset(self, **kwargs):
        self.query_AND_1, self.query_OR_1 = FilterOrmCommon.get_query_connector_tuple()
        search = self.request.GET.get('search', '')
        type_register_id = self.kwargs.get("typeregisterid")

        self.query_AND_1.children.append(("type_register_id", type_register_id))
        self.query_AND_1.children.append(("institution_id", self.request.user.institution_id))

        if search:
            self.query_OR_1.children.append(("student__last_name__icontains", search))
            self.query_OR_1.children.append(("student__first_name__icontains", search))
            self.query_OR_1.children.append(("student__email__icontains", search))
            self.query_OR_1.children.append(("student__dni__icontains", search))

        FilterOrmCommon.get_filter_date_range(self.request.GET, 'date_issue', self.query_AND_1)

        return StudentRegisters.objects.select_related(
            "institution",
            "student",
            "type_register",
            "certificate",
            "country"
        ).filter(
            self.query_AND_1,
            self.query_OR_1
        ).order_by(
            "-date_issue"
        )

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': "No ha enviado ninguna opcion"}
        action = request.POST['action']

        if action == 'renovate_register':
            student_register_id = request.POST.get('student_register_id')
            student_register = StudentRegisters.objects.get(id=student_register_id)

            quota_balance = ShoppingCartManager.get_quota_balance(
                student_register.type_register_id,
                student_register.institution_id
            )

            if quota_balance <= 0:
                status = 400
                data['message'] = 'No tiene cupos disponibles, obtenga mas en el modulo OBTEN MAS REGISTRO.'
                return JsonResponse(data, status=status)

            date_issue_old = student_register.date_issue
            date_expiry_old = student_register.date_expiry

            student_register.date_issue = datetime.datetime.now()
            student_register.date_expiry += datetime.timedelta(days=SysParameters.get_parameter_fer_value())
            student_register.save()

            institution_quotes_type_register = InstitutionQuotesTypeRegister.objects.get(
                institution_id=student_register.institution_id,
                type_register_id=student_register.type_register_id
            )
            institution_quotes_type_register.quotas_balance -= 1
            institution_quotes_type_register.save()

            StudentRegistersRenovationHistory.objects.create(
                student_registers_id=student_register.id,
                date_issue_old=date_issue_old,
                date_expiry_old=date_expiry_old,
            )

            return JsonResponse(data, status=200)