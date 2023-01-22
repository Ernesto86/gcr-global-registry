from urllib.parse import urlencode
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView

from core.command.validation_upload_file_institution.validation_upload_file_institution import \
    ValidationUploadFileInstitution
from core.common.form.form_common import FormCommon
from institutions.forms import InstitutionDiscountForm, InstitutionForm
from institutions.models import Institutions
from security.functions import addUserData
from core.util_functions import ListViewFilter
from security.mixins import *
from advisers.models import Advisers, Managers
from core.constants import RegistrationStatus, SYSTEM_NAME, REGISTER_DEFAULT_GRUP_USER, REGISTER_INSTITUTIONS_GRUP_USER, \
    CODE_ADVISER_DEFAULT
from core.send_email import render_to_email_send
from system.models import SysCountries, SysParameters
import datetime

class InstitutionsListView(PermissionMixin, ListViewFilter, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'institutions/list.html'
    context_object_name = 'institutions'
    permission_required = 'view_institutions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        get_params = {k: v[0] for k, v in dict(self.request.GET).items()}
        context.update(get_params)
        try:
            get_params.pop('page')
        except:
            pass
        context['url_params'] = urlencode(get_params)
        return context


    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search', '')
        self.filter_date('fecha')
        return Institutions.objects.filter(
            Q(name__icontains=search),
            *self.queries()
        ).order_by(
            '-created_at'
        )

class InstitutionCreateView(PermissionMixin, CreateView):
    model = Institutions
    template_name = 'institutions/create.html'
    form_class = InstitutionForm
    success_url = reverse_lazy('institution_list')
    permission_required = 'add_institutions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = reverse_lazy('institution_list')
        context['form_action'] = 'Crear'
        return context

class InstitutionUpdateView(PermissionMixin, UpdateView):
    model = Institutions
    template_name = 'institutions/create.html'
    form_class = InstitutionForm
    success_url = reverse_lazy('institution_list')
    permission_required = 'change_institutions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = reverse_lazy('institution_list')
        context['form_action'] = 'Actualizar'
        return context

class InstitutionDelete(PermissionMixin, View):
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        Institutions.objects.get(pk=id).delete()
        return JsonResponse({}, status=200)

class InstitutionconfigurationView(PermissionMixin, TemplateView):
    template_name = 'institutions/configuration.html'
    success_url = reverse_lazy('institution_configuration')
    permission_required = ('add_institutions','change_institutions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['form'] = InstitutionForm(instance = self.request.user.institution)
        context['institution'] = self.request.user.institution
        context['title_label'] = "Configurar datos de Institución"
        return context

    def post(self, request, *args, **kwargs):

        institution = self.request.user.institution
        adviser_code = request.POST.get('adviser', None)

        if adviser_code:
            adviser = Advisers.objects.filter(code=adviser_code, deleted=False).first()
        else:
            adviser = Advisers.objects.filter(code=CODE_ADVISER_DEFAULT, deleted=False).first()

        if adviser is None:
            messages.add_message(request, messages.ERROR, "No se encontro codigo de Asesor")
            return redirect(self.success_url)

        form = InstitutionForm(request.POST.copy(), request.FILES, instance = institution)
        form.data['adviser'] = adviser.id

        if form.is_valid():

            if Institutions.has_complete_files(form.instance):
                form.instance.last_data_upload_complete_files = datetime.datetime.now().date()

            form.save()
            user = self.request.user

            if institution is None:
                user.institution = form.instance
                user.save()

            try:
                reseptores = [institution.email, user.email, adviser.manager.email]
                parameter = SysParameters.objects.filter(status=True, code='EMAIL-ADMIN').first()
                if parameter is not None:
                    reseptores.append(parameter.value)

                render_to_email_send(
                    subject= f"Verificación de información ingresada, {SYSTEM_NAME}",
                    body={
                        'institution': institution,
                        'system_name': SYSTEM_NAME
                    },
                    receiver=reseptores,
                    template='email/template_institution_configuration.html'
                )
            except:
                pass

            messages.add_message(request, messages.SUCCESS, "Registro actualizado correctamente..")
            return redirect(self.success_url)
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form })


class InstitutionRegisterStatus(PermissionMixin, ListViewFilter, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'institutions/register_status.html'
    context_object_name = 'institutions'
    group_permissions = ['Gerentes']
    permission_required = 'view_institutions'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        get_params = {k: v[0] for k, v in dict(self.request.GET).items()}
        context.update(get_params)
        try:
            get_params.pop('page')
        except:
            pass
        context['discount_form'] = InstitutionDiscountForm()
        context['url_params'] = urlencode(get_params)
        context['status'] = RegistrationStatus.choices
        context['countries'] = SysCountries.objects.filter(deleted=False)
        try:
            context['country_id'] = int(context['country_id']) if context['country_id'] else ''
        except:
            pass

        ValidationUploadFileInstitution().run()

        return context

    def get_queryset(self, **kwargs):
        user = self.request.user
        search = self.request.GET.get('search', '')
        self.query_filter = {
            'registration_status': self.request.GET.get('status_id', ''),
            'country_id': self.request.GET.get('country_id', '')
        }

        group = user.get_group_session()
        if group.name in self.group_permissions:
            manager = Managers.objects.filter(user_id=user.pk).first()
            if manager is not None:
                self.query_filter['adviser__manager_id'] = manager.id
            else:
                messages.add_message(request, messages.ERROR, "No tiene permisos para ingresar al modulo.")
                return redirect('/')

        return Institutions.objects.select_related(
            'type_registration',
            'adviser',
            'adviser__manager'
        ).filter(
            Q(deleted=False),
            Q(code__icontains=search)|
            Q(name__icontains=search),
            *self.queries()
        ).order_by(
            '-created_at',
            'name'
        )

    def post(self, request, *args, **kwargs):
        data = {'errors': []}

        action = request.POST.get('action', '')

        if action == 'change_discount':
            institution_id = self.request.POST.get("institution_id")

            institution = Institutions.objects.get(id=institution_id)

            form = InstitutionDiscountForm(request.POST, instance=institution)

            if form.is_valid():
                form.save()

                return JsonResponse(data, status=200)
            else:
                data['message'] = 'Error de validacion de formulario.'
                data['errors'] = [FormCommon.get_errors_dict(form)]

        return JsonResponse(data, status=400)

class InstitutionViewByPk(PermissionMixin, View):

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        try:
            pk = kwargs.get('pk')
            institution = Institutions.objects.filter(deleted=False, pk=pk).first()
            if institution is not None:
                status_id = self.request.POST.get('status_id')
                with_mail = self.request.POST.get('with_mail')
                observation = self.request.POST.get('observation', '')

                institution.registration_status = status_id
                institution.date_approval = datetime.datetime.now()
                institution.details = observation
                institution.save()

                try:
                    institution_user = institution.user_set.get()
                    institution_user.groups.clear()
                    user_group = REGISTER_INSTITUTIONS_GRUP_USER if status_id == '2' else REGISTER_DEFAULT_GRUP_USER
                    institution_user.set_grup_to_user_add(user_group)

                except:
                    pass

                try:
                    if with_mail:
                        user = request.user
                        reseptores = [institution.email, user.email]
                        parameter = SysParameters.objects.filter(status=True, code='EMAIL-ADMIN').first()
                        if parameter is not None:
                            reseptores.append(parameter.value)

                        render_to_email_send(
                            subject= f"Aprobacion de estado de registro en {SYSTEM_NAME}",
                            body={
                                'institution': institution,
                                'message': observation,
                                'system_name': SYSTEM_NAME
                            },
                            receiver=reseptores,
                            template='email/template_register_status.html'
                        )
                except:
                    pass

                status = 200
                data['code'] = 'successful'
                data['message'] = 'Registro actualizado correctamente'

            else:
                status = 400
                data['code'] = 'failed'
                data['message'] = 'No se encontro institucion'

        except Exception as e:
            status = 500
            data['code'] = 'failed'
            data['message'] = 'Internal error in code'
            data['errors'].append(str(e))

        return JsonResponse(data, status=status)

    def get(self, request, *args, **kwargs):
        data = {'errors': []}
        status = 200
        try:
            pk = kwargs.get('pk')
            institution = Institutions.objects.filter(deleted=False, pk=pk).first()
            if institution is not None:
                data = {
                    "id": institution.id,
                    "code": institution.code,
                    "name": institution.name,
                    "adviser": institution.adviser.names if institution.adviser else '',
                    "type_registration": institution.type_registration.name if institution.type_registration else '',
                    "country": institution.country.name if institution.country else '',
                    "registration_status": institution.get_registration_status_display().upper(),
                    "status_bg": institution.get_bg_status(),
                    "representative": institution.representative,
                    # "representative_academic_level": institution.representative_academic_level.name if institution.representative_academic_level else '',
                    "representative_academic_level": "-",
                    "email": institution.email,
                    "observation": institution.detail if institution.detail else '',
                }
            else:
                status = 200
                data['code'] = 'failed'
                data['message'] = 'No se encontro institucion'

        except Exception as e:
            status = 500
            data['code'] = 'failed'
            data['message'] = 'Internal error in code'
            data['errors'].append(str(e))

        return JsonResponse(data, status=status)
