import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum
from django.http import JsonResponse
from django.forms import model_to_dict

from advisers.manager.payment_adviser_commissions_manager import PaymentAdviserCommissionsManager
from advisers.models import Advisers, PaymentAdviserCommissionsDetails, PaymentAdviserCommissions
from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.common.filter_query.filter_query_common import FilterQueryCommon
from core.constants import MESES
from core.util_functions import util_null_to_decimal
from institutions.models import Institutions
from security.functions import addUserData
from transactions.models import OrderInstitutionQuotas


class DashboardAdvisorView(LoginRequiredMixin, TemplateView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/dashboard_advisor/view.html'
    permission_required = 'dashboard_advisers'

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        status = 500

        action = request.POST.get('action', '')

        if action == 'view_detail_institution':
            advisers = Advisers.objects.get(user_id=self.request.user.pkid)
            institution_id = request.POST.get('institution_id')
            option_view = request.POST.get('option_view')

            if option_view == 'paid':
                data.update(
                    PaymentAdviserCommissionsManager.get_detail_adviser_payment(
                        PaymentAdviserCommissions.TYPE_FUNCTIONARY[1][0],
                        advisers.id,
                        institution_id=institution_id,
                        pay_adviser=True
                    )
                )

            elif option_view == 'xcobrar':
                data.update(
                    PaymentAdviserCommissionsManager.get_detail_adviser_payment(
                        PaymentAdviserCommissions.TYPE_FUNCTIONARY[1][0],
                        advisers.id,
                        institution_id=institution_id,
                        pay_adviser=False
                    )
                )

            status = 200
            data['message'] = ''

        elif action == 'commission_paid':
            year_selected = FilterQueryCommon.get_param_validate(request.POST.get('year', None))
            advisers = Advisers.objects.get(user_id=self.request.user.pkid)
            payment_paid_list = []
            status = 200
            is_per_year = True if year_selected else False

            query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
            query_AND_1.children.append(('deleted', False))
            query_AND_1.children.append(('adviser_id', advisers.id))
            query_AND_1.children.append(('pay_adviser', True))

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
                                sum=Sum('commissions_advisers_value')
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

            data['payment_paid_list'] = payment_paid_list

        elif action == 'commission_x_cobrar':
            year_selected = FilterQueryCommon.get_param_validate(request.POST.get('year', None))
            advisers = Advisers.objects.get(user_id=self.request.user.pkid)
            payment_paid_list = []
            status = 200
            is_per_year = True if year_selected else False

            query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
            query_AND_1.children.append(('deleted', False))
            query_AND_1.children.append(('adviser_id', advisers.id))
            query_AND_1.children.append(('pay_adviser', False))

            range_year_to_search_list = self.get_range_year_to_search_list(is_per_year, year_selected)

            for year in range_year_to_search_list:
                value_presenter_list = []

                if is_per_year:

                    for mes in MESES:
                        value_commission = util_null_to_decimal(
                            OrderInstitutionQuotas.objects.filter(
                                query_AND_1,
                                date_issue__year=year_selected,
                                date_issue__month=mes[0],
                            ).aggregate(
                                sum=Sum('commissions_advisers_value')
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
                            sum=Sum('commissions_advisers_value')
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

            data['payment_paid_list'] = payment_paid_list

        elif action == 'commission_totals':
            year_selected = FilterQueryCommon.get_param_validate(request.POST.get('year', None))
            advisers = Advisers.objects.get(user_id=self.request.user.pkid)
            payment_paid_list = []
            status = 200
            is_per_year = True if year_selected else False

            query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
            query_AND_1.children.append(('deleted', False))
            query_AND_1.children.append(('adviser_id', advisers.id))

            range_year_to_search_list = self.get_range_year_to_search_list(is_per_year, year_selected)

            for year in range_year_to_search_list:
                value_presenter_list = []

                if is_per_year:

                    for mes in MESES:
                        value_commission = util_null_to_decimal(
                            OrderInstitutionQuotas.objects.filter(
                                query_AND_1,
                                date_issue__year=year_selected,
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

            data['payment_paid_list'] = payment_paid_list

        return JsonResponse(data, status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['advisers'] = advisers = Advisers.objects.get(user_id=self.request.user.pkid)
        context['year_list'] = self.get_range_year_list()

        context['institutions_active_count'] = Institutions.objects.filter(adviser_id=advisers.id, deleted=False, status=True).count()
        context['institutions_disabled_count'] = Institutions.objects.filter(adviser_id=advisers.id, deleted=False, status=False).count()
        context['value_commission_payment'] = util_null_to_decimal(
            PaymentAdviserCommissionsDetails.objects.filter(
                adviser_id=advisers.id,
                pay=True,
                deleted=False,
            ).aggregate(sum=Sum('value_commission'))['sum']
        )

        context['order_subtotal'] = util_null_to_decimal(
            OrderInstitutionQuotas.objects.filter(
                adviser_id=advisers.id,
                deleted=False,
            ).aggregate(sum=Sum('subtotal'))['sum']
        )

        order_institution_quotas_subtotal = PaymentAdviserCommissionsManager.get_detail_adviser_payment_acummulate(
            PaymentAdviserCommissions.TYPE_FUNCTIONARY[1][0],
            advisers.id
        )
        context['value_commission_x_cobrar'] = order_institution_quotas_subtotal['commission_adviser']
        context['institutions_list'] = Institutions.objects.filter(adviser_id=advisers.id)

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
