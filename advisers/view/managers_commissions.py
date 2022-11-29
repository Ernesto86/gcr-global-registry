from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from advisers.forms import ManagersCommissionsForm, PeriodCommissionsForm, PeriodCommissionsManagerForm
from advisers.models import ManagersCommissions, PeriodCommissions
from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.util_functions import util_null_to_decimal
from security.functions import addUserData


def validate_commissions_max(period_commissions, request):
    if util_null_to_decimal(request.POST.get('manager_percentage')) > period_commissions.manager_percentage_max:
        raise NameError(f"Excedió valor maximo de la comision del periodo: {period_commissions.manager_percentage_max}")


def managers_commissions_save(request, *args, **kwargs):
    list_id_specific = request.POST.getlist('managers_specific')
    is_specific = True if list_id_specific else False
    period_commissions = PeriodCommissions.objects.filter(deleted=False).last()

    query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
    query_AND_1.children.append(("deleted", False))

    dict_update = {
        'value': request.POST.get('manager_percentage'),
        'is_exclude': False
    }

    validate_commissions_max(period_commissions, request)

    if is_specific:
        query_AND_1.children.append(("manager_id__in", list_id_specific))
        dict_update['is_exclude'] = True
    else:
        period_commissions.manager_percentage = request.POST.get('manager_percentage')
        period_commissions.save()

    ManagersCommissions.objects.filter(
        query_AND_1
    ).update(
        **dict_update
    )


class ManagersCommissionsListView(LoginRequiredMixin, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/managers_commissions/list.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['create_url'] = reverse_lazy("advisers:managers_commissions_create")
        context['title_label'] = 'Listado de comisiones de gerentes'
        return context

    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search', '')
        return ManagersCommissions.objects.filter(
            Q(manager__last_name__icontains=search) | Q(manager__first_name__icontains=search) | Q(manager__code__icontains=search)
        ).select_related(
            'manager'
        ).order_by(
            '-created_at'
        )


class ManagersCommissionsCreateView(CreateView):
    model = ManagersCommissions
    template_name = 'advisers/managers_commissions/create.html'
    form_class = ManagersCommissionsForm
    success_url = reverse_lazy('advisers:managers_commissions_list')
    permission_required = 'add_managerscommissions'

    def post(self, request, *args, **kwargs):
        period_commissions = PeriodCommissions.objects.filter(deleted=False).last()
        try:
            managers_commissions_save(request, *args, **kwargs)
            return redirect(self.success_url)
        except Exception as ex:
            messages.add_message(request, messages.ERROR, str(ex))

        form = ManagersCommissionsForm()
        form_2 = PeriodCommissionsManagerForm(
            request.POST,
            instance=period_commissions,
        )
        return render(request, self.template_name, {'form': form, 'form_2': form_2})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = reverse_lazy('advisers:managers_commissions_list')
        context['title_label'] = "Actualizacion masiva"
        period_commissions = PeriodCommissions.objects.filter(deleted=False).last()
        context['form_2'] = PeriodCommissionsManagerForm(
            instance=period_commissions,
        )
        context['form_action'] = 'Crear'
        return context


class ManagersCommissionsUpdateView(UpdateView):
    model = ManagersCommissions
    template_name = 'advisers/managers_commissions/create.html'
    form_class = ManagersCommissionsForm
    success_url = reverse_lazy('advisers:managers_commissions_list')
    permission_required = 'change_institutions'

    def post(self, request, *args, **kwargs):
        period_commissions = PeriodCommissions.objects.filter(deleted=False).last()
        try:
            managers_commissions_save(request, *args, **kwargs)
            return redirect(self.success_url)
        except Exception as ex:
            messages.add_message(request, messages.ERROR, str(ex))

        form = ManagersCommissionsForm()
        form_2 = PeriodCommissionsManagerForm(
            request.POST,
            instance=period_commissions,
        )
        return render(request, self.template_name, {'form': form, 'form_2': form_2})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = reverse_lazy('advisers:managers_commissions_list')
        context['title_label'] = "Actualizacion masiva"
        managers_commissions = self.get_object()
        context['form_2'] = PeriodCommissionsManagerForm(
            instance=PeriodCommissions.objects.filter(deleted=False).last(),
            initial={
                'managers_specific': [managers_commissions.manager_id],
                'manager_percentage': managers_commissions.value,
            }
        )
        context['form_action'] = 'Actualizar'
        return context
