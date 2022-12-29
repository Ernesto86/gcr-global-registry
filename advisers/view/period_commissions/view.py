from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from rest_framework import status

from advisers.forms import PeriodCommissionsAdminForm
from advisers.models import PeriodCommissions, AdvisersCommissions, ManagersCommissions
from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.common.form.form_common import FormCommon
from security.functions import addUserData
from security.mixins import *


class PeriodCommissionsUpdateView(PermissionMixin, UpdateView):
    model = PeriodCommissions
    template_name = 'advisers/period_commissions/create.html'
    form_class = PeriodCommissionsAdminForm
    success_url = reverse_lazy('home')
    permission_required = 'change_periodcommissions'

    def get_object(self):
        return PeriodCommissions.objects.all().last()

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ""}
        action = request.POST['action']

        if action == 'edit':
            instance = self.get_object()
            form = self.form_class(data=self.request.POST, instance=instance)

            if form.is_valid():
                self.update_massive_commissions(form)

                self.update_percentage_period_commissions(form)

                form.save()
                return JsonResponse(data, status=status.HTTP_200_OK)

            data['message'] = 'Error de validacion de formulario.'
            data['errors'] = [FormCommon.get_errors_dict(form)]
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_massive_commissions(self, form):
        query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
        query_AND_1.children.append(("deleted", False))

        AdvisersCommissions.objects.filter(
            query_AND_1,
            commissions_period_1__gt=form.cleaned_data['advisers_percentage_max_period_1'],
        ).update(
            commissions_period_1=form.cleaned_data['advisers_percentage_max_period_1'],
        )

        AdvisersCommissions.objects.filter(
            query_AND_1,
            commissions_period_2__gt=form.cleaned_data['advisers_percentage_max_period_2'],
        ).update(
            commissions_period_2=form.cleaned_data['advisers_percentage_max_period_2'],
        )

        AdvisersCommissions.objects.filter(
            query_AND_1,
            commissions_period_3__gt=form.cleaned_data['advisers_percentage_max_period_3'],
        ).update(
            commissions_period_3=form.cleaned_data['advisers_percentage_max_period_3'],
        )

        ManagersCommissions.objects.filter(
            query_AND_1,
            value__gt=form.cleaned_data['manager_percentage_max']
        ).update(
            value=form.cleaned_data['manager_percentage_max']
        )

    def update_percentage_period_commissions(self, form):
        if form.cleaned_data['manager_percentage'] > form.cleaned_data['manager_percentage_max']:
            form.instance.manager_percentage = form.cleaned_data['manager_percentage_max']

        if form.cleaned_data['advisers_percentage_period_1'] > form.cleaned_data['advisers_percentage_max_period_1']:
            form.instance.advisers_percentage_period_1 = form.cleaned_data['advisers_percentage_max_period_1']

        if form.cleaned_data['advisers_percentage_period_2'] > form.cleaned_data['advisers_percentage_max_period_2']:
            form.instance.advisers_percentage_period_2 = form.cleaned_data['advisers_percentage_max_period_2']

        if form.cleaned_data['advisers_percentage_period_3'] > form.cleaned_data['advisers_percentage_max_period_3']:
            form.instance.advisers_percentage_period_3 = form.cleaned_data['advisers_percentage_max_period_3']

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = self.success_url
        context['title_label'] = 'Actualizacion masiva de periodos de comision'
        context['action'] = 'edit'
        return context
