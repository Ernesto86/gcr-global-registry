from urllib.parse import urlencode
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.http import JsonResponse
from rest_framework import status

from advisers.forms import ManagerForm
from advisers.models import Managers, Managers, ManagersCommissions
from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.common.form.form_common import FormCommon
from security.functions import addUserData
from core.util_functions import ListViewFilter
from security.mixins import *
from security.models import User


class ManagerListView(PermissionMixin, ListViewFilter, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/manager/list.html'
    context_object_name = 'advisers'
    permission_required = 'view_managers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['create_url'] = reverse_lazy('advisers:manager_create')
        context['title_label'] = "Listado de gerentes"
        context['clear_url'] = reverse_lazy('advisers:manager_list')

        get_params = FilterOrmCommon.get_url_params(self.request.GET)
        context.update(get_params)
        context['url_params'] = urlencode(get_params)
        return context

    def get_queryset(self, **kwargs):
        self.query_AND_1, self.query_OR_1 = FilterOrmCommon.get_query_connector_tuple()
        search = self.request.GET.get('search', '')
        self.query_AND_1.children.append(("deleted", False))

        if search:
            self.query_OR_1.children.append(("last_name__icontains", search))
            self.query_OR_1.children.append(("first_name__icontains", search))
            self.query_OR_1.children.append(("code__icontains", search))
            self.query_OR_1.children.append(("dni__icontains", search))

        return Managers.objects.filter(
            self.query_AND_1,
            self.query_OR_1
        ).order_by(
            '-created_at'
        )


class ManagerCreateView(PermissionMixin, CreateView):
    model = Managers
    template_name = 'advisers/manager/create.html'
    form_class = ManagerForm
    success_url = reverse_lazy('advisers:manager_list')
    permission_required = 'add_managers'

    def get_initial(self):
        initial_dict = super(ManagerCreateView, self).get_initial()
        initial_dict['code'] = Managers.generate_code()
        return initial_dict

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ""}
        action = request.POST['action']

        if action == 'add':
            form = self.get_form()

            if form.is_valid():
                if User.objects.filter(email=form.cleaned_data['email']).exists():
                    data['message'] = 'Ya existe un usuario con el email principal.'
                    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

                user = User.objects.create_user(
                    username=form.instance.email,
                    first_name=form.instance.first_name,
                    last_name=form.instance.last_name,
                    email=form.instance.email,
                    password="admin123**",
                    is_active=False
                )

                form.instance.user_id = user.pk
                form.save()
                return JsonResponse(data, status=status.HTTP_200_OK)
            else:
                data['message'] = 'Error de validacion de formulario.'
                data['errors'] = [FormCommon.get_errors_dict(form)]

            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = self.success_url
        context['title_label'] = "Crear gerentes"
        context['action'] = 'add'
        return context


class ManagerUpdateView(PermissionMixin, UpdateView):
    model = Managers
    template_name = 'advisers/manager/create.html'
    form_class = ManagerForm
    success_url = reverse_lazy('advisers:manager_list')
    permission_required = 'change_managers'

    def get_form(self, *args, **kwargs):
        form = super(ManagerUpdateView, self).get_form(*args, **kwargs)
        FormCommon.update_readonly_field([form.fields['email']], is_list=True)
        return form

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ""}
        action = request.POST['action']

        if action == 'edit':
            instance = self.get_object()
            form = self.form_class(data=self.request.POST, instance=instance)

            if form.is_valid():
                form.save()
                form.instance.user.first_name = form.instance.first_name
                form.instance.user.last_name = form.instance.last_name
                form.instance.user.save()
                return JsonResponse(data, status=status.HTTP_200_OK)

            data['message'] = 'Error de validacion de formulario.'
            data['errors'] = [FormCommon.get_errors_dict(form)]
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = self.success_url
        context['title_label'] = 'Actualizar asesor'
        context['action'] = 'edit'
        return context


class ManagerDeleteView(PermissionMixin, View):
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            manager = Managers.objects.get(pk=id)
            manager.user.is_active = False
            manager.deleted = True
            manager_commissions = ManagersCommissions.objects.get(manager_id=manager.id)
            manager_commissions.deleted = True
            manager_commissions.save()
            manager.save()
        except Exception as ex:
            return JsonResponse(
                {"message": "Error al eliminar", "errors": ["Error al eliminar"]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return JsonResponse({}, status=status.HTTP_200_OK)