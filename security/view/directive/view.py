from urllib.parse import urlencode
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth.models import Group

from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.common.form.form_common import FormCommon
from core.constants import GROUP_NAME_ADVISER, GROUP_NAME_DIRECTIVO
from security.forms import CustomUserCreationForm, CustomUserChangeForm
from security.functions import addUserData
from core.util_functions import ListViewFilter
from security.mixins import *
from security.models import User


class UserListView(PermissionMixin, ListViewFilter, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'security/directive/list.html'
    context_object_name = 'advisers'
    permission_required = 'view_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['create_url'] = reverse_lazy('user_create')
        context['title_label'] = "Listado de usuarios administradores"
        context['clear_url'] = reverse_lazy('user_list')

        get_params = FilterOrmCommon.get_url_params(self.request.GET)
        context.update(get_params)
        context['url_params'] = urlencode(get_params)
        return context

    def get_queryset(self, **kwargs):
        self.query_AND_1, self.query_OR_1 = FilterOrmCommon.get_query_connector_tuple()
        self.query_AND_1.children.append(("is_staff", True))
        self.query_AND_1.children.append(("is_superuser", False))
        search = self.request.GET.get('search', '')

        if search:
            self.query_OR_1.children.append(("username__icontains", search))
            self.query_OR_1.children.append(("email__icontains", search))
            self.query_OR_1.children.append(("last_name__icontains", search))
            self.query_OR_1.children.append(("first_name__icontains", search))

        return User.objects.filter(
            self.query_AND_1,
            self.query_OR_1
        ).order_by(
            "-id"
        )


class UserCreateView(PermissionMixin, CreateView):
    model = User
    template_name = 'security/directive/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user_list')
    permission_required = 'add_user'

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ""}
        action = request.POST['action']

        if action == 'add':

            form = self.get_form()

            if form.is_valid():

                if User.objects.filter(email=form.cleaned_data['email']).exists():
                    data['message'] = 'Ya existe un usuario con el email principal.'
                    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

                user = User.objects.create_administrativo(
                    username=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1']
                )

                directivo_group = Group.objects.get(name=GROUP_NAME_DIRECTIVO)
                user.groups.add(directivo_group)

                return JsonResponse(data, status=status.HTTP_200_OK)

            data['message'] = 'Error de validacion de formulario.'
            data['errors'] = [FormCommon.get_errors_dict(form)]
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = self.success_url
        context['title_label'] = "Crear directivo"
        context['action'] = 'add'
        return context


class UserUpdateView(PermissionMixin, UpdateView):
    model = User
    template_name = 'security/directive/create.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('user_list')
    permission_required = 'change_user'

    def get_form(self, *args, **kwargs):
        form = super(UserUpdateView, self).get_form(*args, **kwargs)
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
                return JsonResponse(data, status=status.HTTP_200_OK)

            data['message'] = 'Error de validacion de formulario.'
            data['errors'] = [FormCommon.get_errors_dict(form)]
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = self.success_url
        context['title_label'] = 'Actualizar directivo'
        context['action'] = 'edit'
        return context


class UserDeleteView(PermissionMixin, View):
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            user = User.objects.get(pk=id)
            user.is_active = False
            user.save()
        except Exception as ex:
            return JsonResponse(
                {"message": "Error al eliminar", "errors": []},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return JsonResponse({}, status=status.HTTP_200_OK)
