from datetime import *
from decimal import Decimal
from typing import List

from django.db.models import Subquery, OuterRef, Func
from django.db.models import Sum, Q
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
        self.__adviser = adviser
        self.__number_of_year_max = number_of_year_max
        self.__query_AND_1 = Q()
        self.__query_AND_1.connector = 'AND'

    def get_institution_order_totals_per_range_year(self):
        institution_dict = {}
        labels = []

        for year in self.get_range_last_year():
            labels.append(year)

            query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
            query_AND_1.children.append(('deleted', False))
            query_AND_1.children.append(('adviser_id', self.__adviser.id))
            query_AND_1.children.append(('date_issue__year', year))

            subquery = self.__get_subquery_order_institution_quotas(query_AND_1)

            institutions = self.__get_institutions_to_order_totals(subquery)

            self.__fill_institution_dict(institution_dict, institutions)

        series = self.__get_series_to_order_totals(institution_dict)

        return {
            'series': series,
            'labels': labels
        }

    def get_institution_order_totals_per_year(self, year):
        institution_dict = {}
        labels = []

        for mes in MESES:
            labels.append(mes)

            query_AND_1, _ = FilterOrmCommon.get_query_connector_tuple()
            query_AND_1.children.append(('date_issue__month', mes[0]))
            query_AND_1.children.append(('date_issue__year',year))
            query_AND_1.children.append(('adviser_id', self.__adviser.id))

            subquery = self.__get_subquery_order_institution_quotas(query_AND_1)

            institutions = self.__get_institutions_to_order_totals(subquery)

            self.__fill_institution_dict(institution_dict, institutions)

        series = self.__get_series_to_order_totals(institution_dict)

        return {
            'series': series,
            'labels': labels
        }

    def __get_subquery_order_institution_quotas(self, query_and):
        return Subquery(
            OrderInstitutionQuotas.objects.filter(
                query_and,
                institution=OuterRef('id'),
                deleted=False,
            ).annotate(
                sum=Func('subtotal', function='SUM')
            ).values('sum').order_by()
        )

    def __get_institutions_to_order_totals(self, subquery):
        return Institutions.objects.select_related(
            'type_registration'
        ).filter(
            deleted=False,
            adviser_id=self.__adviser.id
        ).annotate(
            subtotal=subquery
        )

    def __fill_institution_dict(self, institution_dict, institutions):
        for institution in institutions:
            value = institution.subtotal if institution.subtotal else "0.00"

            if institution_dict.get(str(institution.id)):

                institution_dict[str(institution.id)]['data'].append(value)

            else:

                institution_dict[str(institution.id)] = {
                    'data': [value],
                    'name': institution.name
                }

    def __get_series_to_order_totals(self, institution_dict):
        series = []
        for k, v in institution_dict.items():
            series.append(v)
        return series

    def get_commission_collected_per_range_year(self):
        payment_paid_list = []
        self.__set_query_to_commission_collected()

        for year in self.get_range_last_year():
            value_commission = self.__get_value_commission_to_year(year, 'commissions_advisers_value')
            payment_paid_list.append(self.__get_format_send(year, year, value_commission))

        return payment_paid_list

    def get_commission_collected_per_year(self, year):
        payment_paid_list = []
        self.__set_query_to_commission_collected()

        for mes in MESES:
            value_commission = self.__get_value_commission_to_year_and_month(year, mes[0], 'commissions_advisers_value')
            payment_paid_list.append(self.__get_format_send(year, mes[1], value_commission))

        return payment_paid_list

    def get_commission_collected(self):
        self.__set_query_to_commission_collected()

        return util_null_to_decimal(
            OrderInstitutionQuotas.objects.filter(
                self.__query_AND_1
            ).aggregate(
                sum=Sum('commissions_advisers_value')
            )['sum']
        )

    def get_commission_by_collect_per_range_year(self):
        payment_paid_list = []
        self.__set_query_to_commission_by_collect()

        for year in self.get_range_last_year():
            value_commission = self.__get_value_commission_to_year(year, 'commissions_advisers_value')
            payment_paid_list.append(self.__get_format_send(year, year, value_commission))

        return payment_paid_list

    def get_commission_by_collect_per_year(self, year):
        payment_paid_list = []
        self.__set_query_to_commission_by_collect()

        for mes in MESES:
            value_commission = self.__get_value_commission_to_year_and_month(year, mes[0], 'commissions_advisers_value')
            payment_paid_list.append(self.__get_format_send(year, mes[1], value_commission))

        return payment_paid_list

    def get_commission_by_collect(self):
        self.__set_query_to_commission_by_collect()

        return util_null_to_decimal(
            OrderInstitutionQuotas.objects.filter(
                self.__query_AND_1
            ).aggregate(
                sum=Sum('commissions_advisers_value')
            )['sum']
        )

    def get_totals_sales_per_range_year(self):
        payment_paid_list = []
        self.__set_query_to_totals_sales()

        for year in self.get_range_last_year():
            value_commission = self.__get_value_commission_to_year(year, 'subtotal')
            payment_paid_list.append(self.__get_format_send(year, year, value_commission))

        return payment_paid_list

    def get_totals_sales_per_year(self, year):
        payment_paid_list = []
        self.__set_query_to_totals_sales()

        for mes in MESES:
            value_commission = self.__get_value_commission_to_year_and_month(year, mes[0], 'subtotal')
            payment_paid_list.append(self.__get_format_send(year, mes[1], value_commission))

        return payment_paid_list

    def get_totals_sales(self):
        self.__set_query_to_totals_sales()

        return util_null_to_decimal(
            OrderInstitutionQuotas.objects.filter(
                self.__query_AND_1
            ).aggregate(sum=Sum('subtotal'))['sum']
        )

    def get_institutions_active_count(self):
        return Institutions.objects.filter(
            adviser_id=self.__adviser.id,
            deleted=False,
            registration_status=RegistrationStatus.APROBADO
        ).count()

    def get_institutions_disabled_count(self):
        return Institutions.objects.filter(
            adviser_id=self.__adviser.id,
            deleted=False,
            registration_status=RegistrationStatus.PENDIENTE
        ).count()

    def get_range_last_year(self) -> List[int]:
        """
            rango desde año actual hasta un año anterior
        """
        year = datetime.now().date().year
        year_list = [year]

        for index in range(0, self.__number_of_year_max):
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

    def get_detail_sales_collected_per_range_year_and_institution(self, institution_id):
        self.__set_query_to_commission_collected()
        self.__query_AND_1.children.append(('institution_id', institution_id))

        order_list = OrderInstitutionQuotas.objects.select_related(
            'institution'
        ).filter(
            self.__query_AND_1
        ).order_by('-date_issue')

        detail_order_sales_per_institution = self.__get_detail_order_sales(order_list)

        return {
            **detail_order_sales_per_institution,
            'adviser': model_to_dict(self.__adviser),
        }

    def get_detail_sales_by_collect_per_range_year_and_institution(self, institution_id):
        self.__set_query_to_commission_by_collect()
        self.__query_AND_1.children.append(('institution_id', institution_id))

        order_list = OrderInstitutionQuotas.objects.select_related(
            'institution'
        ).filter(
            self.__query_AND_1
        ).order_by('-date_issue')

        detail_order_sales_per_institution = self.__get_detail_order_sales(order_list)

        return {
            **detail_order_sales_per_institution,
            'adviser': model_to_dict(self.__adviser),
        }

    def __get_detail_order_sales(self, order_list):
        order_institution_quotas_list = []

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
            commission_adviser_real = (detail.commissions_advisers_value / detail.subtotal) * 100

            order_institution_quotas_list.append(
                {
                    **model_to_dict(detail),
                    'date_issue': detail.date_issue.date(),
                    'number': detail.number,
                    'commission_adviser_clean': commission_clean,
                    'commission_manager': detail.commissions_managers_value,
                    'commission_adviser': detail.commissions_advisers_value,
                    'commission_adviser_real': commission_adviser_real,
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
        }

    def __set_clear_query_and_1(self):
        self.__query_AND_1 = Q()
        self.__query_AND_1.connector = 'AND'

    def __set_query_to_totals_sales(self):
        self.__set_clear_query_and_1()
        self.__query_AND_1.children.append(('deleted', False))
        self.__query_AND_1.children.append(('adviser_id', self.__adviser.id))

    def __set_query_to_commission_by_collect(self):
        self.__set_clear_query_and_1()
        self.__query_AND_1.children.append(('deleted', False))
        self.__query_AND_1.children.append(('adviser_id', self.__adviser.id))
        self.__query_AND_1.children.append(('pay_adviser', False))

    def __set_query_to_commission_collected(self):
        self.__set_clear_query_and_1()
        self.__query_AND_1.children.append(('deleted', False))
        self.__query_AND_1.children.append(('adviser_id', self.__adviser.id))
        self.__query_AND_1.children.append(('pay_adviser', True))

    def __get_value_commission_to_year(self, year, name_field_aggregate):
        return util_null_to_decimal(
            OrderInstitutionQuotas.objects.filter(
                self.__query_AND_1,
                date_issue__year=year,
            ).aggregate(
                sum=Sum(name_field_aggregate)
            )['sum']
        )

    def __get_value_commission_to_year_and_month(self, year, month, name_field_aggregate):
        return util_null_to_decimal(
            OrderInstitutionQuotas.objects.filter(
                self.__query_AND_1,
                date_issue__year=year,
                date_issue__month=month,
            ).aggregate(
                sum=Sum(name_field_aggregate)
            )['sum']
        )
