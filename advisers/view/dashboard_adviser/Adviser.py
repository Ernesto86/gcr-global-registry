from datetime import *
from typing import List
from django.db.models import Sum, Q
from decimal import Decimal
from django.forms import model_to_dict

from advisers.models import Advisers
from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.constants import MESES, RegistrationStatus
from core.util_functions import util_null_to_decimal
from institutions.models import Institutions
from transactions.models import OrderInstitutionQuotas


class AdviserDashboard:
    NUMBER_OF_YEARS_DEFAULT = 4

    def __init__(self, adviser: Advisers, number_of_year_max: int = NUMBER_OF_YEARS_DEFAULT):
        self.adviser = adviser
        self.number_of_year_max = number_of_year_max

    def get_commission_collected_per_range_year(self):
        payment_paid_list = []
        query_AND_1 = self.__get_query_to_commission_collected()

        for year in self.get_range_last_year():
            value_commission = util_null_to_decimal(
                OrderInstitutionQuotas.objects.filter(
                    query_AND_1,
                    date_issue__year=year,
                ).aggregate(
                    sum=Sum('commissions_advisers_value')
                )['sum']
            )

            payment_paid_list.append(self.__get_format_send(year, year, value_commission))

        return payment_paid_list

    def get_commission_collected_per_year(self, year):
        payment_paid_list = []
        query_AND_1 = self.__get_query_to_commission_collected()

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

            payment_paid_list.append(self.__get_format_send(year, mes[1], value_commission))

        return payment_paid_list

    def get_commission_collected(self):
        query_AND_1 = self.__get_query_to_commission_collected()

        return util_null_to_decimal(
            OrderInstitutionQuotas.objects.filter(
                query_AND_1
            ).aggregate(
                sum=Sum('commissions_advisers_value')
            )['sum']
        )

    def __get_query_to_commission_collected(self):
        query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
        query_AND_1.children.append(('deleted', False))
        query_AND_1.children.append(('adviser_id', self.adviser.id))
        query_AND_1.children.append(('pay_adviser', True))
        return query_AND_1

    def get_commission_by_collect_per_range_year(self):
        payment_paid_list = []
        query_AND_1 = self.__get_query_to_commission_by_collect()

        for year in self.get_range_last_year():
            value_commission = util_null_to_decimal(
                OrderInstitutionQuotas.objects.filter(
                    query_AND_1,
                    date_issue__year=year,
                ).aggregate(
                    sum=Sum('commissions_advisers_value')
                )['sum']
            )

            payment_paid_list.append(self.__get_format_send(year, year, value_commission))

        return payment_paid_list

    def get_commission_by_collect_per_year(self, year):
        payment_paid_list = []
        query_AND_1 = self.__get_query_to_commission_by_collect()

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

            payment_paid_list.append(self.__get_format_send(year, mes[1], value_commission))

        return payment_paid_list

    def get_commission_by_collect(self):
        query_AND_1 = self.__get_query_to_commission_by_collect()

        return util_null_to_decimal(
            OrderInstitutionQuotas.objects.filter(
                query_AND_1
            ).aggregate(
                sum=Sum('commissions_advisers_value')
            )['sum']
        )

    def __get_query_to_commission_by_collect(self):
        query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
        query_AND_1.children.append(('deleted', False))
        query_AND_1.children.append(('adviser_id', self.adviser.id))
        query_AND_1.children.append(('pay_adviser', False))
        return query_AND_1

    def get_totals_sales_per_range_year(self):
        payment_paid_list = []
        query_AND_1 = self.__get_query_to_totals_sales()

        for year in self.get_range_last_year():
            value_commission = util_null_to_decimal(
                OrderInstitutionQuotas.objects.filter(
                    query_AND_1,
                    date_issue__year=year,
                ).aggregate(
                    sum=Sum('subtotal')
                )['sum']
            )

            payment_paid_list.append(self.__get_format_send(year, year, value_commission))

        return payment_paid_list

    def get_totals_sales_per_year(self, year):
        payment_paid_list = []
        query_AND_1 = self.__get_query_to_totals_sales()

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

            payment_paid_list.append(self.__get_format_send(year, mes[1], value_commission))

        return payment_paid_list

    def get_totals_sales(self):
        query_AND_1 = self.__get_query_to_totals_sales()

        return util_null_to_decimal(
            OrderInstitutionQuotas.objects.filter(
                query_AND_1
            ).aggregate(sum=Sum('subtotal'))['sum']
        )

    def __get_query_to_totals_sales(self):
        query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
        query_AND_1.children.append(('deleted', False))
        query_AND_1.children.append(('adviser_id', self.adviser.id))
        return query_AND_1

    def get_institutions_active_count(self):
        return Institutions.objects.filter(
            adviser_id=self.adviser.id,
            deleted=False,
            registration_status=RegistrationStatus.APROBADO
        ).count()

    def get_institutions_disabled_count(self):
        return Institutions.objects.filter(
            adviser_id=self.adviser.id,
            deleted=False,
            registration_status=RegistrationStatus.PENDIENTE
        ).count()

    def get_range_last_year(self) -> List[int]:
        """
            rango desde año actual hasta un año anterior
        """
        year = datetime.now().date().year
        year_list = [year]

        for index in range(0, self.number_of_year_max):
            year -= 1
            year_list.append(year)

        return year_list

    def __get_format_send(self, year, label, value_commission):
        return {
            'year': year,
            'value_presenter_list': [
                {
                    'label': label,
                    'value': value_commission
                }
            ]
        }

    def get_detail_sales_collected_per_range_year(self):
        order_institution_quotas_list = []
        query_AND_1 = self.__get_query_to_commission_collected()

        order_list = OrderInstitutionQuotas.objects.select_related(
            'institution'
        ).filter(
            query_AND_1
        ).order_by('-date_issue')

        commission_sum = Decimal(0)
        commission_adviser_sum = Decimal(0)
        commission_manager_sum = Decimal(0)
        subtotal_sum = Decimal(0)

        for detail in order_list:
            commission_clean = detail.get_commission_adviser_clear()
            commission_sum += commission_clean
            commission_adviser_sum += detail.commissions_advisers_value
            commission_manager_sum += detail.commissions_managers_value
            subtotal_sum += detail.subtotal

            order_institution_quotas_list.append(
                {
                    **model_to_dict(detail),
                    'date_issue': detail.date_issue.date(),
                    'number': detail.number,
                    'commission_adviser_clean': commission_clean,
                    'commission_manager': detail.commissions_managers_value,
                    'commission_adviser': detail.commissions_advisers_value,
                    'institution': {
                        'name': detail.institution.name
                    }
                }
            )

        return {
            'order_institution_quotas_list': order_institution_quotas_list,
            'commission_adviser': commission_adviser_sum,
            'commission_manager': commission_manager_sum,
            'commission': commission_sum,
            'subtotal': subtotal_sum,
            'adviser': model_to_dict(self.adviser),
        }

    def get_detail_sales_by_collect_per_range_year(self):
        order_institution_quotas_list = []
        query_AND_1 = self.__get_query_to_commission_by_collect()

        order_list = OrderInstitutionQuotas.objects.select_related(
            'institution'
        ).filter(
            query_AND_1
        ).order_by('-date_issue')

        commission_sum = Decimal(0)
        commission_adviser_sum = Decimal(0)
        commission_manager_sum = Decimal(0)
        subtotal_sum = Decimal(0)

        for detail in order_list:
            commission_clean = detail.get_commission_adviser_clear()
            commission_sum += commission_clean
            commission_adviser_sum += detail.commissions_advisers_value
            commission_manager_sum += detail.commissions_managers_value
            subtotal_sum += detail.subtotal

            order_institution_quotas_list.append(
                {
                    **model_to_dict(detail),
                    'date_issue': detail.date_issue.date(),
                    'number': detail.number,
                    'commission_adviser_clean': commission_clean,
                    'commission_manager': detail.commissions_managers_value,
                    'commission_adviser': detail.commissions_advisers_value,
                    'institution': {
                        'name': detail.institution.name
                    }
                }
            )

        return {
            'order_institution_quotas_list': order_institution_quotas_list,
            'commission_adviser': commission_adviser_sum,
            'commission_manager': commission_manager_sum,
            'commission': commission_sum,
            'subtotal': subtotal_sum,
            'adviser': model_to_dict(self.adviser),
        }
