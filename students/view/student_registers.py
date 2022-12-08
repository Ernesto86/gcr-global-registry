from django.db.models import Sum
from django.forms import model_to_dict
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from security.functions import addUserData
from security.mixins import PermissionMixin
from students.forms import StudentRegistersSearchForm, StudentRegistersForm
from students.models import Students, StudentRegisters
from system.models import SysParameters
from transactions.models import InstitutionQuotesTypeRegister


class StudentRegistersView(PermissionMixin, TemplateView):
    template_name = 'students/student_registers/view.html'
    permission_required = 'add_studentregisters'

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

            try:
                student = Students.objects.get(dni=identification)

                data['message'] = 'No existe el estudiante ingresado'
                data['student'] = model_to_dict(student)
                return JsonResponse(data, status=200)

            except Students.DoesNotExist:
                data['message'] = 'No existe el estudiante ingresado'
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

        student_id = self.request.GET.get('student_id') if self.request.method == 'GET' else self.request.POST.get('student_id')

        self.initial = {
            'student': student_id,
            'code_international_register': SysParameters.get_value_formate_next()['format']
        }
        return self.initial

    def get_form(self, *args, **kwargs):
        form = super(StudentRegistersCreateView, self).get_form(*args, **kwargs)

        student_id = self.request.GET.get('student_id') if self.request.method == 'GET' else self.request.POST.get('student_id')
        institution = self.request.user.institution

        form.fields['student'].queryset = Students.objects.filter(id=student_id)
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
                value_new = SysParameters.get_value_formate_next()
                form.instance.institution_id = self.request.user.institution_id
                form.instance.code_international_register = value_new['format']
                form.save()

                institution_quotes_type_register = InstitutionQuotesTypeRegister.objects.get(
                    institution_id=self.request.user.institution_id,
                    type_register_id=form.instance.type_register_id
                )

                institution_quotes_type_register.quotas_balance -= 1
                institution_quotes_type_register.save()

                SysParameters.update_value(value_new['next_value'])

                return JsonResponse(data, status=status)

            data['code'] = 'failed'
            data['message'] = 'Error'
            data['errors'] = form.errors
            return JsonResponse(data, status=status)

        data['code'] = 'failed'
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

# class InstitutionconfigurationView(TemplateView):
#     template_name = 'students/student_registers/create.html'
#     success_url = reverse_lazy('students_registers_search')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         addUserData(self.request, context)
#         context['form'] = InstitutionForm(instance=self.request.user.institution)
#         return context
#
#     def post(self, request, *args, **kwargs):
#         institution = self.request.user.institution
#         form = InstitutionForm(request.POST, request.FILES, instance=institution)
#         if form.is_valid():
#             form.save()
#             if institution is None:
#                 user = self.request.user
#                 user.institution = form.instance
#                 user.save()
#             messages.add_message(request, messages.SUCCESS, "Registro actualizado correctamente..")
#             return redirect(self.success_url)
#         else:
#             return render(request, self.template_name, {'form': form})
