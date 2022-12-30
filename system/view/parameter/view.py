from urllib.parse import urlencode

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from rest_framework import status

from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.common.form.form_common import FormCommon
from core.util_functions import ListViewFilter
from security.functions import addUserData
from security.mixins import *
from system.forms import SysParameterForm
from system.models import SysParameters


class SysParameterListView(PermissionMixin, ListViewFilter, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'system/parameter/list.html'
    permission_required = 'view_sysparameters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['create_url'] = reverse_lazy('system:sys_parameter_create')
        context['title_label'] = "Listado de parametros"
        context['clear_url'] = reverse_lazy('system:sys_parameter_list')

        get_params = FilterOrmCommon.get_url_params(self.request.GET)
        context.update(get_params)
        context['url_params'] = urlencode(get_params)
        return context

    def get_queryset(self, **kwargs):
        self.query_AND_1, self.query_OR_1 = FilterOrmCommon.get_query_connector_tuple()
        self.query_AND_1.children.append(("deleted", False))

        return SysParameters.objects.filter(
            self.query_AND_1,
            self.query_OR_1
        ).order_by(
            '-created_at'
        )


class SysParameterCreateView(PermissionMixin, CreateView):
    model = SysParameters
    template_name = 'system/parameter/create.html'
    form_class = SysParameterForm
    success_url = reverse_lazy('system:sys_parameter_list')
    permission_required = 'add_sysparameters'

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
        context['title_label'] = "Crear parametros"
        context['action'] = 'add'
        return context


class SysParameterUpdateView(PermissionMixin, UpdateView):
    model = SysParameters
    template_name = 'system/parameter/create.html'
    form_class = SysParameterForm
    success_url = reverse_lazy('system:sys_parameter_list')
    permission_required = 'change_sysparameters'

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
        context['title_label'] = 'Actualizar parametros'
        context['action'] = 'edit'
        return context


class SysParameterDeleteView(PermissionMixin, View):
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            parameter = SysParameters.objects.get(pk=id)
            parameter.deleted = True
            parameter.save()
        except Exception as ex:
            return JsonResponse(
                {"message": "Error al eliminar", "errors": []},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return JsonResponse({}, status=status.HTTP_200_OK)
