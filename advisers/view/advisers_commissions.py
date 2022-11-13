from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from advisers.forms import AdvisersCommissionsForm, PeriodCommissionsForm
from advisers.models import AdvisersCommissions, PeriodCommissions
from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.util_functions import util_null_to_decimal
from security.functions import addUserData


def validate_commissions_max(period_commissions, request):
    if util_null_to_decimal(request.POST.get('advisers_percentage_period_1')) > period_commissions.advisers_percentage_max_period_1:
        raise NameError(f"Excedió valor maximo de la comision del periodo: {period_commissions.advisers_percentage_max_period_1}")
    if util_null_to_decimal(request.POST.get('advisers_percentage_period_2')) > period_commissions.advisers_percentage_max_period_2:
        raise NameError(f"Excedió valor maximo de la comision del periodo: {period_commissions.advisers_percentage_max_period_2}")
    if util_null_to_decimal(request.POST.get('advisers_percentage_period_3')) > period_commissions.advisers_percentage_max_period_3:
        raise NameError(f"Excedió valor maximo de la comision del periodo: {period_commissions.advisers_percentage_max_period_3}")


def advisers_commissions_save(request, *args, **kwargs):
    period_commissions = PeriodCommissions.objects.filter(deleted=False).last()
    list_id_specific = request.POST.getlist('advisers_specific')
    is_specific = True if list_id_specific else False

    query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
    query_AND_1.children.append(("deleted", False))

    dict_update = {
        'commissions_period_1': request.POST.get('advisers_percentage_period_1'),
        'commissions_period_2': request.POST.get('advisers_percentage_period_2'),
        'commissions_period_3': request.POST.get('advisers_percentage_period_3'),
        'is_exclude': False
    }

    if is_specific:
        query_AND_1.children.append(("adviser_id__in", list_id_specific))
        dict_update['is_exclude'] = True
    else:
        period_commissions.advisers_percentage_period_1 = request.POST.get('advisers_percentage_period_1')
        period_commissions.advisers_percentage_period_2 = request.POST.get('advisers_percentage_period_2')
        period_commissions.advisers_percentage_period_3 = request.POST.get('advisers_percentage_period_3')
        period_commissions.save()

    validate_commissions_max(period_commissions, request)

    AdvisersCommissions.objects.filter(
        query_AND_1
    ).update(
        **dict_update
    )


class AdvisersCommissionsListView(LoginRequiredMixin, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/advisers_commissions/list.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        return context

    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search', '')
        return AdvisersCommissions.objects.filter(
            Q(adviser__last_name__icontains=search) | Q(adviser__first_name__icontains=search) | Q(adviser__code__icontains=search)
        ).select_related(
            'adviser'
        ).order_by(
            '-created_at'
        )


class AdvisersCommissionsCreateView(CreateView):
    model = AdvisersCommissions
    template_name = 'advisers/advisers_commissions/create.html'
    form_class = AdvisersCommissionsForm
    success_url = reverse_lazy('advisers:advisers_commissions_list')
    permission_required = 'add_institutions'

    def post(self, request, *args, **kwargs):
        period_commissions = PeriodCommissions.objects.filter(deleted=False).last()
        try:
            advisers_commissions_save(request, *args, **kwargs)
            return redirect(self.success_url)
        except Exception as ex:
            messages.add_message(request, messages.ERROR, str(ex))

        form = AdvisersCommissionsForm()
        form_2 = PeriodCommissionsForm(
            request.POST,
            instance=period_commissions,
        )
        return render(request, self.template_name, {'form': form, 'form_2': form_2})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = reverse_lazy('advisers:advisers_commissions_list')
        period_commissions = PeriodCommissions.objects.filter(deleted=False).last()
        context['form_2'] = PeriodCommissionsForm(
            instance=period_commissions,
            initial={
                'advisers_percentage_period_1': period_commissions.advisers_percentage_max_period_1,
                'advisers_percentage_period_2': period_commissions.advisers_percentage_max_period_2,
                'advisers_percentage_period_3': period_commissions.advisers_percentage_max_period_3,
            }
        )
        context['form_action'] = 'Crear'
        return context


class AdvisersCommissionsUpdateView(UpdateView):
    model = AdvisersCommissions
    template_name = 'advisers/advisers_commissions/create.html'
    form_class = AdvisersCommissionsForm
    success_url = reverse_lazy('advisers:advisers_commissions_list')
    permission_required = 'change_institutions'

    def post(self, request, *args, **kwargs):
        period_commissions = PeriodCommissions.objects.filter(deleted=False).last()
        try:
            advisers_commissions_save(request, *args, **kwargs)
            return redirect(self.success_url)
        except Exception as ex:
            messages.add_message(request, messages.ERROR, str(ex))

        form = AdvisersCommissionsForm()
        form_2 = PeriodCommissionsForm(
            request.POST,
            instance=period_commissions,
        )
        return render(request, self.template_name, {'form': form, 'form_2': form_2})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = reverse_lazy('advisers:advisers_commissions_list')
        advisers_commissions = self.get_object()
        context['form_2'] = PeriodCommissionsForm(
            instance=PeriodCommissions.objects.filter(deleted=False).last(),
            initial={
                'advisers_specific': [advisers_commissions.adviser_id],
                'advisers_percentage_period_1': advisers_commissions.commissions_period_1,
                'advisers_percentage_period_2': advisers_commissions.commissions_period_2,
                'advisers_percentage_period_3': advisers_commissions.commissions_period_3,
            }
        )
        context['form_action'] = 'Actualizar'
        return context
