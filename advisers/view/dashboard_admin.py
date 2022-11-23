import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum
from django.http import JsonResponse
from django.forms import model_to_dict

from advisers.manager.payment_adviser_commissions_manager import PaymentAdviserCommissionsManager
from advisers.models import Advisers, PaymentAdviserCommissionsDetails, PaymentAdviserCommissions, Managers
from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.common.filter_query.filter_query_common import FilterQueryCommon
from core.constants import MESES
from core.util_functions import util_null_to_decimal
from institutions.models import Institutions
from security.functions import addUserData
from system.models import SysCountries
from transactions.models import OrderInstitutionQuotas


class DashboardAdminView(LoginRequiredMixin, TemplateView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/dashboard_admin/view.html'

    # permission_required = ('add_institutions','change_institutions')

    def get_range_year_list(self):
        year = datetime.datetime.now().date().year
        year_list = [year]

        for index in range(0, 4):
            year -= 1
            year_list.append(year)
        return year_list

    def get_payment_adviser_commissions_list(self, year, year_list, year_selected):
        query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()

        for index in range(0, 4):
            year -= 1
            year_list.append(year)

        if year_selected:
            query_AND_1.children.append(('year', year_selected))
        else:
            query_AND_1.children.append(('year__in', year_list))

        payment_adviser_commissions_list = PaymentAdviserCommissions.objects.filter(
            query_AND_1,
            deleted=False,
        )

        return payment_adviser_commissions_list

    def get_filter_orm(self, query_AND_1, country_id, manager_id, adviser_id):

        if country_id:
            query_AND_1.children.append(('institution__country_id', country_id))

            if manager_id:
                query_AND_1.children.append(('manager_id', manager_id))

                if adviser_id:
                    query_AND_1.children.append(('adviser_id', adviser_id))

        return query_AND_1

    def get_commission_paid(self, country_id, manager_id, adviser_id, year, year_list, year_selected):
        payment_paid_list = []

        payment_adviser_commissions_list = self.get_payment_adviser_commissions_list(
            year, year_list, year_selected
        )

        query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
        query_AND_1.children.append(('deleted', False))
        query_AND_1.children.append(('pay_manager', True))

        self.get_filter_orm(
            query_AND_1, country_id, manager_id, adviser_id
        )

        for payment_adviser_commissions in payment_adviser_commissions_list:
            value_presenter_list = []

            if year_selected:

                for mes in MESES:
                    value_commission = util_null_to_decimal(
                        OrderInstitutionQuotas.objects.filter(
                            query_AND_1,
                            date_issue__year=year_selected,
                            date_issue__month=mes[0],
                        ).aggregate(
                            sum=Sum('commissions_managers_value')
                        )['sum']
                    )

                    value_presenter_list.append(
                        {
                            'payment_adviser_commissions': model_to_dict(payment_adviser_commissions),
                            'label': mes[1],
                            'value': value_commission
                        }
                    )
            else:
                value_commission = util_null_to_decimal(
                    OrderInstitutionQuotas.objects.filter(
                        query_AND_1
                    ).aggregate(
                        sum=Sum('commissions_managers_value')
                    )['sum']
                )

                value_presenter_list.append(
                    {
                        'label': payment_adviser_commissions.year,
                        'value': value_commission
                    }
                )

            payment_paid_list.append(
                {
                    'payment_adviser_commissions': model_to_dict(payment_adviser_commissions),
                    'value_presenter_list': value_presenter_list
                }
            )

        return payment_paid_list

    def get_commission_x_cobrar(self, country_id, manager_id, adviser_id, year, year_list, year_selected):
        payment_paid_list = []

        payment_adviser_commissions_list = self.get_payment_adviser_commissions_list(
            year, year_list, year_selected
        )

        query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
        query_AND_1.children.append(('deleted', False))
        query_AND_1.children.append(('pay_manager', False))

        self.get_filter_orm(
            query_AND_1, country_id, manager_id, adviser_id
        )

        for payment_adviser_commissions in payment_adviser_commissions_list:
            value_presenter_list = []

            if year_selected:

                for mes in MESES:
                    value_commission = util_null_to_decimal(
                        OrderInstitutionQuotas.objects.filter(
                            query_AND_1,
                            date_issue__year=year_selected,
                            date_issue__month=mes[0],
                        ).aggregate(
                            sum=Sum('commissions_managers_value')
                        )['sum']
                    )

                    value_presenter_list.append(
                        {
                            'payment_adviser_commissions': model_to_dict(payment_adviser_commissions),
                            'label': mes[1],
                            'value': value_commission
                        }
                    )
            else:
                value_commission = util_null_to_decimal(
                    OrderInstitutionQuotas.objects.filter(
                        query_AND_1,
                    ).aggregate(
                        sum=Sum('commissions_managers_value')
                    )['sum']
                )

                value_presenter_list.append(
                    {
                        'label': payment_adviser_commissions.year,
                        'value': value_commission
                    }
                )

            payment_paid_list.append(
                {
                    'payment_adviser_commissions': model_to_dict(payment_adviser_commissions),
                    'value_presenter_list': value_presenter_list
                }
            )

        return payment_paid_list

    def get_commission_totals(self, country_id, manager_id, adviser_id, year, year_list, year_selected):
        payment_paid_list = []

        payment_adviser_commissions_list = self.get_payment_adviser_commissions_list(
            year, year_list, year_selected
        )

        query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
        query_AND_1.children.append(('deleted', False))

        self.get_filter_orm(
            query_AND_1, country_id, manager_id, adviser_id
        )

        for payment_adviser_commissions in payment_adviser_commissions_list:
            value_presenter_list = []

            if year_selected:

                for mes in MESES:
                    value_commission = util_null_to_decimal(
                        OrderInstitutionQuotas.objects.filter(
                            query_AND_1,
                            date_issue__year=year_selected,
                            date_issue__month=mes[0]
                        ).aggregate(
                            sum=Sum('subtotal')
                        )['sum']
                    )

                    value_presenter_list.append(
                        {
                            'payment_adviser_commissions': model_to_dict(payment_adviser_commissions),
                            'label': mes[1],
                            'value': value_commission
                        }
                    )
            else:
                value_commission = util_null_to_decimal(
                    OrderInstitutionQuotas.objects.filter(
                        query_AND_1
                    ).aggregate(
                        sum=Sum('subtotal')
                    )['sum']
                )

                value_presenter_list.append(
                    {
                        'label': payment_adviser_commissions.year,
                        'value': value_commission
                    }
                )

            payment_paid_list.append(
                {
                    'payment_adviser_commissions': model_to_dict(payment_adviser_commissions),
                    'value_presenter_list': value_presenter_list
                }
            )
        return payment_paid_list

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        status = 500

        action = request.POST.get('action', None)

        if action == 'view_detail_institution':
            institution_id = request.POST.get('institution_id')
            option_view = request.POST.get('option_view')

            if option_view == 'paid':
                data.update(
                    PaymentAdviserCommissionsManager.get_detail_adviser_payment(
                        PaymentAdviserCommissions.TYPE_FUNCTIONARY[1][0],
                        institution_id=institution_id,
                        pay_manager=True
                    )
                )

            elif option_view == 'xcobrar':
                data.update(
                    PaymentAdviserCommissionsManager.get_detail_adviser_payment(
                        PaymentAdviserCommissions.TYPE_FUNCTIONARY[1][0],
                        institution_id=institution_id,
                        pay_manager=False
                    )
                )

            status = 200
            data['message'] = ''

        elif action == 'get_manager':
            status = 200
            country_id = FilterQueryCommon.get_param_validate(request.POST.get('country_id', None))
            data['manager_list'] = [
                {'id': x.id, 'value': x.__str__()} for x in Managers.objects.filter(deleted=False, country_residence_id=country_id)
            ]

        elif action == 'get_adviser':
            status = 200
            manager_id = FilterQueryCommon.get_param_validate(request.POST.get('manager_id', None))
            data['adviser_list'] = [
                {'id': x.id, 'value': x.__str__()} for x in Advisers.objects.filter(deleted=False, manager_id=manager_id)
            ]

        elif action == 'commission_manager':
            year_selected = FilterQueryCommon.get_param_validate(request.POST.get('year', None))
            country_id = FilterQueryCommon.get_param_validate(request.POST.get('country_id', None))
            manager_id = FilterQueryCommon.get_param_validate(request.POST.get('manager_id', None))
            adviser_id = FilterQueryCommon.get_param_validate(request.POST.get('adviser_id', None))
            year = datetime.datetime.now().date().year
            year_list = [year]
            status = 200

            query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
            query_AND_1.children.append(('deleted', False))

            value_commission_query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
            value_commission_query_AND_1.children.append(('deleted', False))

            if year_selected:
                query_AND_1.children.append(('date_approval__year', year_selected))
                value_commission_query_AND_1.children.append(('date_issue__year', year_selected))

            if country_id:
                query_AND_1.children.append(('country_id', country_id))
                value_commission_query_AND_1.children.append(('institution__country_id', country_id))

                if manager_id:
                    query_AND_1.children.append(('adviser__manager_id', manager_id))
                    value_commission_query_AND_1.children.append(('manager_id', manager_id))

                    if adviser_id:
                        query_AND_1.children.append(('adviser_id', adviser_id))
                        value_commission_query_AND_1.children.append(('adviser_id', adviser_id))

            data['institutions_active_count'] = Institutions.objects.filter(query_AND_1, status=True).count()
            data['institutions_disabled_count'] = Institutions.objects.filter(query_AND_1, status=False).count()

            data['value_commission_paid'] = util_null_to_decimal(
                OrderInstitutionQuotas.objects.filter(
                    value_commission_query_AND_1,
                    pay_manager=True,
                ).aggregate(
                    sum=Sum('commissions_managers_value')
                )['sum']
            )
            data['value_commission_x_cobrar'] = util_null_to_decimal(
                OrderInstitutionQuotas.objects.filter(
                    value_commission_query_AND_1,
                    pay_manager=False,
                ).aggregate(
                    sum=Sum('commissions_managers_value')
                )['sum']
            )
            data['value_commission_totals'] = util_null_to_decimal(
                OrderInstitutionQuotas.objects.filter(
                    value_commission_query_AND_1,
                ).aggregate(
                    sum=Sum('subtotal')
                )['sum']
            )

            data['payment_paid_list'] = self.get_commission_paid(
                country_id,
                manager_id,
                adviser_id,
                year,
                year_list,
                year_selected
            )
            data['payment_x_cobrar_list'] = self.get_commission_x_cobrar(
                country_id,
                manager_id,
                adviser_id,
                year,
                year_list,
                year_selected
            )
            data['payment_totals_list'] = self.get_commission_totals(
                country_id,
                manager_id,
                adviser_id,
                year,
                year_list,
                year_selected
            )

            data['institutions_list'] = [
                x
                for x in Institutions.objects.filter(
                    query_AND_1
                ).values(
                    'id',
                    'name',
                    'alias',
                    'type_registration',
                    'representative',
                    'identification',
                    'country',
                    'address',
                    'telephone',
                    'email',
                )
            ]

        return JsonResponse(data, status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['year_list'] = self.get_range_year_list()
        context['country_list'] = SysCountries.objects.filter(deleted=False)
        return context
