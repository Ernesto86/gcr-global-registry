from urllib.parse import urlencode
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from institutions.forms import InstitutionForm
from institutions.models import Institutions
from security.functions import addUserData
from core.util_functions import ListViewFilter
from security.mixins import *
from advisers.models import Advisers
from core.constants import RegistrationStatus
from system.models import SysCountries
import datetime

class InstitutionsListView(PermissionMixin, ListViewFilter, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'institutions/list.html'
    context_object_name = 'institutions'
    permission_required = 'view_institutions'
    paginate_by = 2

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
        return context

    def post(self, request, *args, **kwargs):

        institution = self.request.user.institution
        adviser_code = request.POST.get('adviser', None)

        if adviser_code:
            adviser = Advisers.objects.filter(code=adviser_code, deleted=False).first()
        else:
            adviser = Advisers.objects.filter(code='ASESOR-DEFAULT', deleted=False).first()

        if adviser is None:
            messages.add_message(request, messages.ERROR, "No se encontro codigo de Asesor")
            return redirect(self.success_url)

        form = InstitutionForm(request.POST.copy(), request.FILES, instance = institution)
        form.data['adviser'] = adviser.id

        if form.is_valid():
            form.save()
            if institution is None:
                user = self.request.user
                user.institution = form.instance
                user.save()
            messages.add_message(request, messages.SUCCESS, "Registro actualizado correctamente..")
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form })


class InstitutionRegisterStatus(ListViewFilter, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'institutions/register_status.html'
    context_object_name = 'institutions'
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
        context['url_params'] = urlencode(get_params)
        context['status'] = RegistrationStatus.choices
        context['countries'] = SysCountries.objects.filter(deleted=False)
        try:
            context['country_id'] = int(context['country_id']) if context['country_id'] else ''
        except:
            pass
        return context

    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search', '')
        self.query_filter = {
            'registration_status': self.request.GET.get('status_id', ''),
            'country_id': self.request.GET.get('country_id', ''),
        }
        return Institutions.objects.filter(
            Q(deleted=False),
            Q(code__icontains=search)|
            Q(name__icontains=search),
            *self.queries()
        ).order_by(
            '-created_at',
            'name'
        )

class InstitutionViewByPk(PermissionMixin, View):

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        status = 200
        try:
            pk = kwargs.get('pk')
            institution = Institutions.objects.filter(deleted=False, pk=pk).first()
            if institution is not None:
                status_id = self.request.POST.get('status_id')
                institution.registration_status = status_id
                institution.date_approval = datetime.datetime.now()
                institution.save()
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
                    "representative_academic_level": institution.representative_academic_level.name if institution.representative_academic_level else '',
                    "email": institution.email,
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
