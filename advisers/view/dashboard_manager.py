import datetime

from django.db.models import Sum
from django.http import JsonResponse
from django.views.generic import TemplateView

from advisers.manager.payment_adviser_commissions_manager import PaymentAdviserCommissionsManager
from advisers.models import Advisers, PaymentAdviserCommissions, Managers
from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.common.filter_query.filter_query_common import FilterQueryCommon
from core.constants import MESES, RegistrationStatus
from core.util_functions import util_null_to_decimal
from institutions.models import Institutions
from security.functions import addUserData
from security.mixins import PermissionMixin
from transactions.models import OrderInstitutionQuotas


class DashboardManagerView(PermissionMixin, TemplateView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/dashboard_manager/view.html'
    permission_required = 'dashboard_managers'

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        status = 500

        action = request.POST.get('action', None)

        if action == 'view_detail_institution':
            manager = Managers.objects.get(user_id=self.request.user.pkid)
            institution_id = request.POST.get('institution_id')
            option_view = request.POST.get('option_view')

            if option_view == 'paid':
                data.update(
                    PaymentAdviserCommissionsManager.get_detail_adviser_payment(
                        PaymentAdviserCommissions.TYPE_FUNCTIONARY[2][0],
                        manager.id,
                        institution_id=institution_id,
                        pay_manager=True
                    )
                )

            elif option_view == 'xcobrar':
                data.update(
                    PaymentAdviserCommissionsManager.get_detail_adviser_payment(
                        PaymentAdviserCommissions.TYPE_FUNCTIONARY[2][0],
                        manager.id,
                        institution_id=institution_id,
                        pay_manager=False
                    )
                )

            status = 200
            data['message'] = ''

        elif action == 'commission_manager':
            year_selected = FilterQueryCommon.get_param_validate(request.POST.get('year', None))
            adviser_id = FilterQueryCommon.get_param_validate(request.POST.get('adviser_id', None))
            manager = Managers.objects.get(user_id=self.request.user.pkid)
            year = datetime.datetime.now().date().year
            status = 200
            is_per_year = True if year_selected else False

            query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
            query_AND_1.children.append(('deleted', False))

            value_commission_query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
            value_commission_query_AND_1.children.append(('deleted', False))

            if is_per_year:
                query_AND_1.children.append(('date_approval__year', year_selected))
                value_commission_query_AND_1.children.append(('date_issue__year', year_selected))

            if adviser_id:
                advisers_id_list = [adviser_id]
                query_AND_1.children.append(('adviser_id__in', advisers_id_list))
                value_commission_query_AND_1.children.append(('adviser_id', adviser_id))
            else:
                advisers_list = Advisers.objects.filter(manager_id=manager.id)
                advisers_id_list = list(advisers_list.values_list('id', flat=True))
                query_AND_1.children.append(('adviser_id__in', advisers_id_list))

            data['payment_paid_list'] = self.get_commission_paid(manager.id, adviser_id, is_per_year, year_selected)

            data['payment_x_cobrar_list'] = self.get_commission_x_cobrar(
                manager.id,
                adviser_id,
                is_per_year,
                year_selected
            )
            data['payment_totals_list'] = self.get_commission_totals(manager.id, adviser_id, is_per_year, year_selected)
            data['institutions_active_count'] = Institutions.objects.filter(
                query_AND_1,
                registration_status=RegistrationStatus.APROBADO
            ).count()
            data['institutions_disabled_count'] = Institutions.objects.filter(
                query_AND_1,
                registration_status=RegistrationStatus.PENDIENTE
            ).count()

            data['value_commission_paid'] = util_null_to_decimal(
                OrderInstitutionQuotas.objects.filter(
                    value_commission_query_AND_1,
                    manager_id=manager.id,
                    pay_manager=True,
                ).aggregate(
                    sum=Sum('commissions_managers_value')
                )['sum']
            )
            data['value_commission_x_cobrar'] = util_null_to_decimal(
                OrderInstitutionQuotas.objects.filter(
                    value_commission_query_AND_1,
                    manager_id=manager.id,
                    pay_manager=False,
                ).aggregate(
                    sum=Sum('commissions_managers_value')
                )['sum']
            )
            data['value_commission_totals'] = util_null_to_decimal(
                OrderInstitutionQuotas.objects.filter(
                    value_commission_query_AND_1,
                    manager_id=manager.id,
                ).aggregate(
                    sum=Sum('subtotal')
                )['sum']
            )
            data['institutions_list'] = [
                x
                for x in Institutions.objects.filter(
                    adviser_id__in=advisers_id_list
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
        context['managers'] = manager = Managers.objects.get(user_id=self.request.user.pkid)
        context['advisers_list'] = advisers_list = Advisers.objects.filter(manager_id=manager.id)
        context['year_list'] = self.get_range_year_list()
        return context

    def get_range_year_list(self):
        year = datetime.datetime.now().date().year
        year_list = [year]

        for index in range(0, 4):
            year -= 1
            year_list.append(year)
        return year_list

    def get_range_year_to_search_list(self, is_per_year, year_selected):

        if is_per_year:
            return [int(year_selected)]

        return self.get_range_year_list()

    def get_commission_paid(self, manager_id, adviser_id, is_per_year, year_selected):
        payment_paid_list = []

        query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
        query_AND_1.children.append(('deleted', False))
        query_AND_1.children.append(('pay_manager', True))
        query_AND_1.children.append(('manager_id', manager_id))

        if adviser_id:
            query_AND_1.children.append(('adviser_id', adviser_id))

        range_year_to_search_list = self.get_range_year_to_search_list(is_per_year, year_selected)

        for year in range_year_to_search_list:
            value_presenter_list = []

            if is_per_year:

                for mes in MESES:
                    value_commission = util_null_to_decimal(
                        OrderInstitutionQuotas.objects.filter(
                            query_AND_1,
                            date_issue__year=year,
                            date_issue__month=mes[0],
                        ).aggregate(
                            sum=Sum('commissions_managers_value')
                        )['sum']
                    )

                    value_presenter_list.append(
                        {
                            'year': year,
                            'label': mes[1],
                            'value': value_commission
                        }
                    )
            else:
                value_commission = util_null_to_decimal(
                    OrderInstitutionQuotas.objects.filter(
                        query_AND_1,
                        date_issue__year=year,
                    ).aggregate(
                        sum=Sum('commissions_managers_value')
                    )['sum']
                )

                value_presenter_list.append(
                    {
                        'label': year,
                        'value': value_commission
                    }
                )

            payment_paid_list.append(
                {
                    'year': year,
                    'value_presenter_list': value_presenter_list
                }
            )

        return payment_paid_list

    def get_commission_x_cobrar(self, manager_id, adviser_id, is_per_year, year_selected):
        payment_paid_list = []

        query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
        query_AND_1.children.append(('deleted', False))
        query_AND_1.children.append(('pay_manager', False))
        query_AND_1.children.append(('manager_id', manager_id))

        if adviser_id:
            query_AND_1.children.append(('adviser_id', adviser_id))

        range_year_to_search_list = self.get_range_year_to_search_list(is_per_year, year_selected)
        for year in range_year_to_search_list:
            value_presenter_list = []

            if is_per_year:
                for mes in MESES:
                    value_commission = util_null_to_decimal(
                        OrderInstitutionQuotas.objects.filter(
                            query_AND_1,
                            date_issue__year=year,
                            date_issue__month=mes[0],
                        ).aggregate(
                            sum=Sum('commissions_managers_value')
                        )['sum']
                    )

                    value_presenter_list.append(
                        {
                            'year': year,
                            'label': mes[1],
                            'value': value_commission
                        }
                    )
            else:
                value_commission = util_null_to_decimal(
                    OrderInstitutionQuotas.objects.filter(
                        query_AND_1,
                        date_issue__year=year,
                    ).aggregate(
                        sum=Sum('commissions_managers_value')
                    )['sum']
                )

                value_presenter_list.append(
                    {
                        'label': year,
                        'value': value_commission
                    }
                )

            payment_paid_list.append(
                {
                    'year': year,
                    'value_presenter_list': value_presenter_list
                }
            )

        return payment_paid_list

    def get_commission_totals(self, manager_id, adviser_id, is_per_year, year_selected):
        payment_paid_list = []

        query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
        query_AND_1.children.append(('deleted', False))
        query_AND_1.children.append(('manager_id', manager_id))

        if adviser_id:
            query_AND_1.children.append(('adviser_id', adviser_id))

        range_year_to_search_list = self.get_range_year_to_search_list(is_per_year, year_selected)

        for year in range_year_to_search_list:
            value_presenter_list = []

            if is_per_year:

                for mes in MESES:
                    value_commission = util_null_to_decimal(
                        OrderInstitutionQuotas.objects.filter(
                            query_AND_1,
                            date_issue__year=year,
                            date_issue__month=mes[0],
                        ).aggregate(
                            sum=Sum('subtotal')
                        )['sum']
                    )

                    value_presenter_list.append(
                        {
                            'year': year,
                            'label': mes[1],
                            'value': value_commission
                        }
                    )
            else:
                value_commission = util_null_to_decimal(
                    OrderInstitutionQuotas.objects.filter(
                        query_AND_1,
                        date_issue__year=year,
                    ).aggregate(
                        sum=Sum('subtotal')
                    )['sum']
                )

                value_presenter_list.append(
                    {
                        'label': year,
                        'value': value_commission
                    }
                )

            payment_paid_list.append(
                {
                    'year': year,
                    'value_presenter_list': value_presenter_list
                }
            )
        return payment_paid_list
