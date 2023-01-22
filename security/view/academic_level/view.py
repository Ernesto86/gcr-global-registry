from urllib.parse import urlencode

from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from rest_framework import status

from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.common.form.form_common import FormCommon
from core.constants import GROUP_NAME_DIRECTIVO
from core.util_functions import ListViewFilter
from security.forms import CustomUserCreationForm, CustomUserChangeForm, AcademicLevelForm
from security.functions import addUserData
from security.mixins import *
from security.models import User
from system.models import AcademicLevel


class AcademicLevelListView(PermissionMixin, ListViewFilter, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'security/academic_level/list.html'
    permission_required = 'view_academiclevel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['create_url'] = reverse_lazy('academic_level_create')
        context['title_label'] = "Listado de niveles academicos"
        context['clear_url'] = reverse_lazy('academic_level_list')

        get_params = FilterOrmCommon.get_url_params(self.request.GET)
        context.update(get_params)
        context['url_params'] = urlencode(get_params)
        return context

    def get_queryset(self, **kwargs):
        self.query_AND_1, self.query_OR_1 = FilterOrmCommon.get_query_connector_tuple()
        search = self.request.GET.get('search', '')

        if search:
            self.query_OR_1.children.append(("code__icontains", search))
            self.query_OR_1.children.append(("name__icontains", search))
            self.query_OR_1.children.append(("name_short__icontains", search))

        return AcademicLevel.objects.filter(
            self.query_AND_1,
            self.query_OR_1
        ).order_by(
            "-id"
        )


class AcademicLevelCreateView(PermissionMixin, CreateView):
    model = AcademicLevel
    template_name = 'security/academic_level/create.html'
    form_class = AcademicLevelForm
    success_url = reverse_lazy('academic_level_list')
    permission_required = 'add_academiclevel'

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ""}
        action = request.POST['action']

        if action == 'add':

            form = self.get_form()

            if form.is_valid():
                form.save()
                return JsonResponse(data, status=status.HTTP_200_OK)

            data['message'] = 'Error de validacion de formulario.'
            data['errors'] = [FormCommon.get_errors_dict(form)]
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = self.success_url
        context['title_label'] = "Crear nivel academico"
        context['action'] = 'add'
        return context


class AcademicLevelUpdateView(PermissionMixin, UpdateView):
    model = AcademicLevel
    template_name = 'security/academic_level/create.html'
    form_class = AcademicLevelForm
    success_url = reverse_lazy('academic_level_list')
    permission_required = 'change_academiclevel'

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ""}
        action = request.POST['action']

        if action == 'edit':
            instance = self.get_object()
            form = self.form_class(data=self.request.POST, instance=instance)

            if form.is_valid():
                form.save()
                return JsonResponse(data, status=status.HTTP_200_OK)

            data['message'] = 'Error de validacion de formulario.'
            data['errors'] = [FormCommon.get_errors_dict(form)]
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = self.success_url
        context['title_label'] = 'Actualizar nivel academico'
        context['action'] = 'edit'
        return context


class AcademicLevelDeleteView(PermissionMixin, View):
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            AcademicLevel.objects.get(pk=id).delete()
        except Exception as ex:
            return JsonResponse(
                {"message": "Error al eliminar", "errors": []},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return JsonResponse({}, status=status.HTTP_200_OK)
