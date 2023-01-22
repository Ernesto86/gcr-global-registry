import datetime

from django.db.models import Sum
from django.forms import model_to_dict
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from core.common.form.form_common import FormCommon
from security.functions import addUserData
from security.manager.organizador_registros_manager import OrganizadorRegistrosManager
from security.mixins import PermissionMixin
from students.forms import StudentRegistersSearchForm, StudentRegistersForm
from students.models import Students, StudentRegisters
from system.models import SysParameters
from transactions.manager.shopping_cart_manager import ShoppingCartManager
from transactions.models import InstitutionQuotesTypeRegister


class StudentRegistersView(PermissionMixin, TemplateView):
    template_name = 'students/student_registers/view.html'
    permission_required = 'add_studentregisters'

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ''}
        status = 500

        action = request.POST.get('action', None)

        if action == 'type_registries_list':

            organizador_registros_manager = OrganizadorRegistrosManager(self.request.user)
            data['type_registries_list'] = organizador_registros_manager.get_type_registries_list()
            status = 200

        elif action == 'type_registries_count_available_list':

            organizador_registros_manager = OrganizadorRegistrosManager(self.request.user)
            type_registries_count_available_list = organizador_registros_manager.get_type_registries_count_available_list()
            data['type_registries_count_available_list'] = type_registries_count_available_list
            status = 200

        return JsonResponse(data, status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['title_label'] = 'INGRESO INTERNACIONAL DE REGISTROS INSTITUCIONAL'
        institution_quotes_type_register_sum = InstitutionQuotesTypeRegister.objects.filter(
            institution_id=context['user'].institution_id,
            deleted=False,
        ).aggregate(
            quotas=Sum('quotas'),
            quotas_balance=Sum('quotas_balance'),
        )

        context['institution_quotes_type_register_sum'] = institution_quotes_type_register_sum
        context['register_into_quotas'] = StudentRegisters.objects.filter(
            institution_id=context['user'].institution_id,
            deleted=False
        ).count()
        return context


class StudentRegistersSearchView(PermissionMixin, TemplateView):
    template_name = 'students/student_registers/search.html'
    permission_required = ('add_studentregisters',)

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': "No ha enviado ninguna opcion"}
        status = 500

        action = request.POST.get('action', '')

        if action == 'search':
            identification = request.POST.get('identification')
            country = request.POST.get('country')

            try:
                student = Students.objects.get(dni=identification, country=country)
                data['student'] = model_to_dict(student)
                return JsonResponse(data, status=200)

            except Students.DoesNotExist:
                data['message'] = 'No existe el estudiante con el dni buscado'
                return JsonResponse(data, status=404)
            except Exception as ex:
                data['message'] = 'Error inesperado'
                return JsonResponse(data, status=500)

        return JsonResponse(data, status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['form'] = StudentRegistersSearchForm()
        context['title_label'] = "INGRESO INTERNACIONAL DE REGISTROS INSTITUCIONAL"
        return context


class StudentRegistersCreateView(PermissionMixin, CreateView):
    permission_required = ('add_studentregisters',)
    model = StudentRegisters
    template_name = 'students/student_registers/create.html'
    form_class = StudentRegistersForm
    success_url = reverse_lazy('students:students_registers_search')

    def get_initial(self):
        super(StudentRegistersCreateView, self).get_initial()

        student_id = self.request.GET.get('student_id') if self.request.method == 'GET' else self.request.POST.get(
            'student_id')

        self.initial = {
            'student': student_id,
            'certificate': self.request.session.get('name_certificate_register_copy', ''),
        }
        return self.initial

    def get_form(self, *args, **kwargs):
        form = super(StudentRegistersCreateView, self).get_form(*args, **kwargs)

        student_id = self.request.GET.get('student_id') if self.request.method == 'GET' else self.request.POST.get(
            'student_id')
        institution = self.request.user.institution

        form.fields['student'].empty_label = None
        form.fields['student'].queryset = Students.objects.filter(id=student_id, deleted=False)
        form.fields['type_register'].queryset = institution.get_type_register_enabled_list()
        return form

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': "No ha enviado ninguna opcion"}
        status = 500

        action = request.POST['action']

        if action == 'add':
            form = self.get_form()

            if form.is_valid():
                status = 200

                quota_balance = ShoppingCartManager.get_quota_balance(
                    form.instance.type_register_id,
                    self.request.user.institution_id
                )

                if quota_balance <= 0:
                    status = 400
                    data['message'] = 'No tiene cupos disponibles, obtenga mas en el modulo OBTEN MAS REGISTRO.'
                    return JsonResponse(data, status=status)

                form.instance.institution_id = self.request.user.institution_id
                form.instance.date_expiry = form.instance.date_issue + datetime.timedelta(days=SysParameters.get_parameter_fer_value())
                form.save()

                institution_quotes_type_register = InstitutionQuotesTypeRegister.objects.get(
                    institution_id=self.request.user.institution_id,
                    type_register_id=form.instance.type_register_id
                )

                institution_quotes_type_register.quotas_balance -= 1
                institution_quotes_type_register.save()

                request.session['name_certificate_register_copy'] = form.cleaned_data['certificate']

                return JsonResponse(data, status=status)

            data['message'] = 'Error de validacion de formulario.'
            data['errors'] = [FormCommon.get_errors_dict(form)]
            return JsonResponse(data, status=status)

        return JsonResponse(data, status=status)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['form_action'] = 'Crear'
        context['student_id'] = self.request.GET.get('student_id')
        context['success_url'] = self.success_url
        context['back_url'] = self.success_url
        context['title_label'] = "Crear registro de estudiante"
        return context
