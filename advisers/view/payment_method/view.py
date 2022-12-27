from urllib.parse import urlencode
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.http import JsonResponse
from rest_framework import status

from advisers.forms import PaymentMethodForm
from advisers.models import PaymentMethod, Managers
from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.common.form.form_common import FormCommon
from security.functions import addUserData
from core.util_functions import ListViewFilter
from security.mixins import *
from security.models import User


class PaymentMethodListView(PermissionMixin, ListViewFilter, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/payment_method/list.html'
    permission_required = 'view_paymentmethod'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['create_url'] = reverse_lazy('advisers:payment_method_create')
        context['title_label'] = "Listado de tarjetas"
        context['clear_url'] = reverse_lazy('advisers:payment_method_list')

        get_params = FilterOrmCommon.get_url_params(self.request.GET)
        context.update(get_params)
        context['url_params'] = urlencode(get_params)
        return context

    def get_queryset(self, **kwargs):
        self.query_AND_1, self.query_OR_1 = FilterOrmCommon.get_query_connector_tuple()
        self.query_AND_1.children.append(("user_id", self.request.user.pkid))
        self.query_AND_1.children.append(("deleted", False))

        return PaymentMethod.objects.filter(
            self.query_AND_1,
            self.query_OR_1
        ).order_by(
            '-created_at'
        )


class PaymentMethodCreateView(PermissionMixin, CreateView):
    model = PaymentMethod
    template_name = 'advisers/payment_method/create.html'
    form_class = PaymentMethodForm
    success_url = reverse_lazy('advisers:payment_method_list')
    permission_required = 'add_paymentmethod'

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ""}
        action = request.POST['action']

        if action == 'add':
            form = self.get_form()

            if form.is_valid():

                if form.cleaned_data['is_default']:
                    if PaymentMethod.objects.filter(
                            user_id=self.request.user.pkid,
                            is_default=True,
                            deleted=False
                    ).exists():
                        data['message'] = 'Ya existe una tarjeta predeterminada.'
                        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

                form.instance.user_id = self.request.user.pkid
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
        context['title_label'] = "Crear tarjeta"
        context['action'] = 'add'
        return context


class PaymentMethodUpdateView(PermissionMixin, UpdateView):
    model = PaymentMethod
    template_name = 'advisers/payment_method/create.html'
    form_class = PaymentMethodForm
    success_url = reverse_lazy('advisers:payment_method_list')
    permission_required = 'change_paymentmethod'

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ""}
        action = request.POST['action']

        if action == 'edit':
            instance = self.get_object()
            form = self.form_class(data=self.request.POST, instance=instance)

            payment_method = self.get_object()

            if form.is_valid():
                if PaymentMethod.objects.filter(
                        user_id=self.request.user.pkid,
                        is_default=True,
                        deleted=False
                ).exclude(
                    id=payment_method.id
                ).exists():
                    data['message'] = 'Ya existe una tarjeta predeterminada.'
                    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

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
        context['title_label'] = 'Actualizar tarjeta'
        context['action'] = 'edit'
        return context


class PaymentMethodDeleteView(PermissionMixin, View):
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        payment_method = PaymentMethod.objects.get(pk=id)
        payment_method.deleted = True
        payment_method.save()
        return JsonResponse({}, status=status.HTTP_200_OK)
