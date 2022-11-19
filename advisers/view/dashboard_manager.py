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
from transactions.models import OrderInstitutionQuotas


class DashboardManagerView(LoginRequiredMixin, TemplateView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/dashboard_manager/view.html'

    # permission_required = ('add_institutions','change_institutions')

    def get_payment_adviser_commissions_list(self, year, year_list, is_per_year, year_selected):
        query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()

        for index in range(0, 4):
            year -= 1
            year_list.append(year)

        if is_per_year:
            query_AND_1.children.append(('year', year_selected))
        else:
            query_AND_1.children.append(('year__in', year_list))

        payment_adviser_commissions_list = PaymentAdviserCommissions.objects.filter(
            query_AND_1,
            deleted=False,
        )

        return payment_adviser_commissions_list

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
                        PaymentAdviserCommissions.TYPE_FUNCTIONARY[1][0],
                        manager.id,
                        institution_id=institution_id,
                        pay_manager=True
                    )
                )

            elif option_view == 'xcobrar':
                data.update(
                    PaymentAdviserCommissionsManager.get_detail_adviser_payment(
                        PaymentAdviserCommissions.TYPE_FUNCTIONARY[1][0],
                        manager.id,
                        institution_id=institution_id,
                        pay_manager=False
                    )
                )

            status = 200
            data['message'] = ''

        elif action == 'commission_paid':
            year_selected = FilterQueryCommon.get_param_validate(request.POST.get('year', None))
            adviser_id = FilterQueryCommon.get_param_validate(request.POST.get('adviser_id', None))
            manager = Managers.objects.get(user_id=self.request.user.pkid)
            year = datetime.datetime.now().date().year
            year_list = [year]
            payment_paid_list = []
            status = 200
            is_per_year = True if year_selected else False

            query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
            if adviser_id:
                query_AND_1.children.append(('adviser_id', adviser_id))

            payment_adviser_commissions_list = self.get_payment_adviser_commissions_list(
                year, year_list, is_per_year, year_selected
            )

            for payment_adviser_commissions in payment_adviser_commissions_list:
                value_presenter_list = []

                if is_per_year:

                    for mes in MESES:
                        value_commission = util_null_to_decimal(
                            OrderInstitutionQuotas.objects.filter(
                                query_AND_1,
                                manager_id=manager.id,
                                date_issue__year=year_selected,
                                date_issue__month=mes[0],
                                pay_manager=True,
                                deleted=False
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
                            manager_id=manager.id,
                            pay_manager=True,
                            deleted=False
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

            data['payment_paid_list'] = payment_paid_list

        elif action == 'commission_x_cobrar':
            year_selected = FilterQueryCommon.get_param_validate(request.POST.get('year', None))
            adviser_id = FilterQueryCommon.get_param_validate(request.POST.get('adviser_id', None))
            manager = Managers.objects.get(user_id=self.request.user.pkid)
            year = datetime.datetime.now().date().year
            year_list = [year]
            payment_paid_list = []
            status = 200
            is_per_year = True if year_selected else False

            print("adviser_id: ", adviser_id)

            query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
            if adviser_id:
                query_AND_1.children.append(('adviser_id', adviser_id))

            payment_adviser_commissions_list = self.get_payment_adviser_commissions_list(
                year, year_list, is_per_year, year_selected
            )

            for payment_adviser_commissions in payment_adviser_commissions_list:
                value_presenter_list = []

                if is_per_year:

                    for mes in MESES:
                        value_commission = util_null_to_decimal(
                            OrderInstitutionQuotas.objects.filter(
                                query_AND_1,
                                manager_id=manager.id,
                                date_issue__year=year_selected,
                                date_issue__month=mes[0],
                                pay_manager=False,
                                deleted=False
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
                            manager_id=manager.id,
                            pay_manager=False,
                            deleted=False
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

            data['payment_paid_list'] = payment_paid_list

        elif action == 'commission_totals':
            year_selected = FilterQueryCommon.get_param_validate(request.POST.get('year', None))
            adviser_id = FilterQueryCommon.get_param_validate(request.POST.get('adviser_id', None))
            manager = Managers.objects.get(user_id=self.request.user.pkid)
            year = datetime.datetime.now().date().year
            year_list = [year]
            payment_paid_list = []
            status = 200
            is_per_year = True if year_selected else False

            query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
            if adviser_id:
                query_AND_1.children.append(('adviser_id', adviser_id))

            payment_adviser_commissions_list = self.get_payment_adviser_commissions_list(
                year, year_list, is_per_year, year_selected
            )

            for payment_adviser_commissions in payment_adviser_commissions_list:
                value_presenter_list = []

                if is_per_year:

                    for mes in MESES:
                        value_commission = util_null_to_decimal(
                            OrderInstitutionQuotas.objects.filter(
                                query_AND_1,
                                manager_id=manager.id,
                                date_issue__year=year_selected,
                                date_issue__month=mes[0],
                                deleted=False
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
                            query_AND_1,
                            manager_id=manager.id,
                            deleted=False
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

            data['payment_paid_list'] = payment_paid_list

        return JsonResponse(data, status=status)

    def get_range_year_list(self):
        year = datetime.datetime.now().date().year
        year_list = [year]

        for index in range(0, 4):
            year -= 1
            year_list.append(year)
        return year_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['managers'] = manager = Managers.objects.get(user_id=self.request.user.pkid)
        context['advisers_list'] = advisers_list = Advisers.objects.filter(manager_id=manager.id)
        advisers_id_list = list(advisers_list.values_list('id', flat=True))

        context['year_list'] = self.get_range_year_list()

        context['institutions_active_count'] = Institutions.objects.filter(adviser_id__in=advisers_id_list, deleted=False, status=True).count()
        context['institutions_disabled_count'] = Institutions.objects.filter(adviser_id__in=advisers_id_list, deleted=False, status=False).count()
        context['value_commission_payment'] = util_null_to_decimal(
            PaymentAdviserCommissionsDetails.objects.filter(
                manager_id=manager.id,
                pay=True,
                deleted=False,
            ).aggregate(sum=Sum('value_commission'))['sum']
        )
        context['order_subtotal'] = util_null_to_decimal(
            OrderInstitutionQuotas.objects.filter(
                manager_id=manager.id,
                deleted=False,
            ).aggregate(sum=Sum('subtotal'))['sum']
        )
        order_institution_quotas_subtotal = PaymentAdviserCommissionsManager.get_detail_adviser_payment_acummulate(
            PaymentAdviserCommissions.TYPE_FUNCTIONARY[1][0],
            manager.id
        )
        context['value_commission_x_cobrar'] = order_institution_quotas_subtotal['commission_manager']
        context['institutions_list'] = Institutions.objects.filter(adviser_id__in=advisers_id_list)

        return context
