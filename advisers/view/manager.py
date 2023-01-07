from urllib.parse import urlencode
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.http import JsonResponse
from rest_framework import status

from advisers.forms import ManagerForm, ManagerChangeForm
from advisers.models import Managers, Managers, ManagersCommissions, Advisers
from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.common.form.form_common import FormCommon
from security.functions import addUserData
from core.util_functions import ListViewFilter
from security.mixins import *
from security.models import User
from system.models import SysCountries


class ManagerListView(PermissionMixin, ListViewFilter, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/manager/list.html'
    context_object_name = 'advisers'
    permission_required = 'view_managers'

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        status = 500

        action = request.POST.get('action', '')

        if action == 'adviser_list':
            manager_id = self.request.POST.get("manager_id")

            manager = Managers.objects.get(id=manager_id)

            data['adviser_list'] = [
                {
                    "code": x.code,
                    "names": x.names,
                    "dni": x.dni,
                    "cell_phone": x.cell_phone,
                    "email": x.email
                }
                for x in Advisers.objects.filter(manager_id=manager.id)
            ]

            status = 200
            data['message'] = ''

        return JsonResponse(data, status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['create_url'] = reverse_lazy('advisers:manager_create')
        context['title_label'] = "Listado de gerentes"
        context['clear_url'] = reverse_lazy('advisers:manager_list')
        context['change_form'] = ManagerChangeForm()

        get_params = FilterOrmCommon.get_url_params(self.request.GET)
        context.update(get_params)
        context['url_params'] = urlencode(get_params)
        context['countries'] = SysCountries.objects.filter(deleted=False)
        try:
            context['country_id'] = int(context['country_id']) if context['country_id'] else ''
        except:
            pass
        return context

    def get_queryset(self, **kwargs):
        self.query_AND_1, self.query_OR_1 = FilterOrmCommon.get_query_connector_tuple()
        search = self.request.GET.get('search', '')
        country_id = self.request.GET.get('country_id', '')
        self.query_AND_1.children.append(("deleted", False))

        if search:
            self.query_OR_1.children.append(("last_name__icontains", search))
            self.query_OR_1.children.append(("first_name__icontains", search))
            self.query_OR_1.children.append(("code__icontains", search))
            self.query_OR_1.children.append(("dni__icontains", search))

        if country_id:
            self.query_OR_1.children.append(("country_residence_id", country_id))

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
    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            
            manager_new_id = request.POST.get('manager', None)
            manager = Managers.objects.get(pk=id)
            manager_new = None

            if manager_new_id == '':
                
                if Advisers.objects.filter(
                    manager_id=manager.id,
                    deleted=False
                ).exists():
                    return JsonResponse(
                        {"message": "Error al eliminar", "errors": ["El gerente actual tiene asesores, tiene que escoger un gerente de reemplazo."]},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            else:
                manager_new = Managers.objects.get(pk=manager_new_id)
            
                if manager.id == manager_new.id:
                    return JsonResponse(
                        {"message": "Error al eliminar", "errors": ["No puede escoger el mismo gerente"]},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            manager.user.is_active = False
            manager.deleted = True
            
            if manager_new is not None:
                advisers = Advisers.objects.filter(
                    manager_id=manager.id,
                    deleted=False
                )
                advisers.update(manager_id=manager_new.id)

            manager_commissions = ManagersCommissions.objects.get(manager_id=manager.id)
            manager_commissions.deleted = True
            manager_commissions.save()

            manager.save()
        except Exception as ex:
            return JsonResponse(
                {"message": "Error al eliminar", "errors": [str(ex)]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return JsonResponse({}, status=status.HTTP_200_OK)
