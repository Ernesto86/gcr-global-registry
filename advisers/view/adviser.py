from urllib.parse import urlencode
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.http import JsonResponse
from rest_framework import status

from advisers.forms import AdviserForm
from advisers.models import Advisers, Managers
from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from security.functions import addUserData
from core.util_functions import ListViewFilter
from security.mixins import *
from security.models import User


class AdviserListView(PermissionMixin, ListViewFilter, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/adviser/list.html'
    context_object_name = 'advisers'
    permission_required = 'view_advisers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['create_url'] = reverse_lazy('advisers:adviser_create')
        context['title_label'] = "Listado de asesores"
        context['clear_url'] = reverse_lazy('advisers:adviser_list')

        get_params = FilterOrmCommon.get_url_params(self.request.GET)
        context.update(get_params)
        context['url_params'] = urlencode(get_params)
        return context

    def get_queryset(self, **kwargs):
        self.query_AND_1, self.query_OR_1 = FilterOrmCommon.get_query_connector_tuple()
        self.query_AND_1.children.append(("manager__user_id", self.request.user.pkid))
        search = self.request.GET.get('search', '')

        if search:
            self.query_OR_1.children.append(("last_name__icontains", search))
            self.query_OR_1.children.append(("first_name__icontains", search))
            self.query_OR_1.children.append(("code__icontains", search))
            self.query_OR_1.children.append(("dni__icontains", search))

        return Advisers.objects.filter(
            self.query_AND_1,
            self.query_OR_1
        ).order_by(
            '-created_at'
        )


class AdviserCreateView(PermissionMixin, CreateView):
    model = Advisers
    template_name = 'advisers/adviser/create.html'
    form_class = AdviserForm
    success_url = reverse_lazy('advisers:adviser_list')
    permission_required = 'add_advisers'

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ""}
        action = request.POST['action']

        if action == 'add':
            form = self.get_form()

            manager = Managers.objects.get(user_id=self.request.user.pk)

            if form.is_valid():
                user = User.objects.create_user(
                    username=form.instance.email,
                    first_name=form.instance.first_name,
                    last_name=form.instance.last_name,
                    email=form.instance.email,
                    password="admin123**",
                    is_active=False
                )
                
                form.instance.manager_id = manager.id
                form.instance.user_id = user.pk
                form.save()
                form.instance.create_commission()
                return JsonResponse(data, status=status.HTTP_200_OK)
            else:

                data['message'] = 'Error de validacion de formulario.'
                errors = {}
                for key, value in form.errors.items():
                    field = form.fields[key]
                    errors[field.label] = value
                data['errors'] = [
                    "Erro de formulario basico",
                    errors
                ]

            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = self.success_url
        context['title_label'] = "Crear asesores"
        context['title_label'] = "Crear asesores"
        context['action'] = 'add'
        return context


class AdviserUpdateView(PermissionMixin, UpdateView):
    model = Advisers
    template_name = 'advisers/adviser/create.html'
    form_class = AdviserForm
    success_url = reverse_lazy('advisers:adviser_list')
    permission_required = 'change_advisers'

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
            data['errors'] = form.errors
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = self.success_url
        context['title_label'] = 'Actualizar asesor'
        context['action'] = 'edit'
        return context


class AdviserDeleteView(PermissionMixin, View):
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            Advisers.objects.get(pk=id).delete()
        except Exception as ex:
            return JsonResponse({"message": "Error al eliminar", "errors" : ["jajaja"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse({}, status=status.HTTP_200_OK)
