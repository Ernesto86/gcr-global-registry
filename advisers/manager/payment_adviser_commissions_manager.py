import datetime
from decimal import Decimal

from django.db.models import Q
from django.forms import model_to_dict

from advisers.models import PaymentAdviserCommissions, Advisers, Managers, PaymentAdviserCommissionsDetails
from core.util_functions import util_null_to_decimal
from transactions.models import OrderInstitutionQuotas


class PaymentAdviserCommissionsManager:

    @staticmethod
    def get_calculate_payment_commissions(type_functionary, year, month):
        value_commission_sum = Decimal(0)

        query_AND_1 = Q()
        query_AND_1.connector = 'AND'
        query_AND_1.children.append(("deleted", False))
        query_AND_1.children.append(("date_issue__year", year))
        query_AND_1.children.append(("date_issue__month", month))

        if type_functionary == PaymentAdviserCommissions.TYPE_FUNCTIONARY[0][0]:
            query_AND_1.children.append(("pay_adviser", False))
        else:
            query_AND_1.children.append(("pay_manager", False))

        order_list = OrderInstitutionQuotas.objects.filter(query_AND_1)

        payment_commissions_details_list = []

        for adviser in Advisers.objects.select_related(
                'manager'
        ).filter(
            deleted=False
        ):
            order_adviser_list = order_list.filter(adviser_id=adviser.id)

            value_commission = Decimal(0)

            for order_adviser in order_adviser_list:
                # value_commission_adviser = order_adviser.get_commission_adviser()
                value_commission_adviser = order_adviser.subtotal * (order_adviser.commissions_advisers_percentage / 100)
                # value_commission_manager = order_adviser.get_commission_manager()
                value_commission_manager = value_commission_adviser * (order_adviser.commissions_managers_percentage / 100)

                if type_functionary == PaymentAdviserCommissions.TYPE_FUNCTIONARY[0][0]:
                    value_commission += value_commission_adviser - value_commission_manager
                else:
                    value_commission += value_commission_manager

            if value_commission == Decimal(0):
                continue

            value_commission_sum += value_commission

            payment_commissions_details_list.append(
                {
                    "type_functionary": type_functionary,
                    "value_commission": util_null_to_decimal(value_commission),
                    'adviser': model_to_dict(adviser),
                    'manager': model_to_dict(adviser.manager),
                    'pay': False
                }
            )

        return {
            "payment_commissions_details_list": payment_commissions_details_list,
            'value_commission': value_commission_sum
        }

    @staticmethod
    def get_detail_adviser_payment(type_functionary, object_id, year, month):
        order_institution_quotas_list = []

        adviser = None
        manager = None

        query_AND_1 = Q()
        query_AND_1.connector = 'AND'
        query_AND_1.children.append(("deleted", False))
        query_AND_1.children.append(("date_issue__year", year))
        query_AND_1.children.append(("date_issue__month", month))

        if type_functionary == PaymentAdviserCommissions.TYPE_FUNCTIONARY[0][0]:
            adviser = Advisers.objects.get(id=object_id)
            query_AND_1.children.append(("adviser_id", object_id))
        else:
            manager = Managers.objects.get(id=object_id)
            query_AND_1.children.append(("manager_id", object_id))

        order_list = OrderInstitutionQuotas.objects.select_related(
            'institution'
        ).filter(
            query_AND_1
        )

        commission_adviser_sum = Decimal(0)
        commission_manager_sum = Decimal(0)

        for detail in order_list:
            commission_adviser = detail.get_commission_adviser()
            commission_manager = detail.get_commission_manager()
            commission_adviser_sum += commission_adviser
            commission_manager_sum += commission_manager

            order_institution_quotas_list.append(
                {
                    **model_to_dict(detail),
                    'date_issue': detail.date_issue.date(),
                    'number': detail.number,
                    'commission_adviser_clean': detail.get_commission_adviser_clear(),
                    'commission_manager': detail.get_commission_manager(),
                    'commission_adviser': commission_adviser,
                    'institution': {
                        'name': detail.institution.name
                    }
                }
            )

        return {
            'order_institution_quotas_list': order_institution_quotas_list,
            'commission_adviser': commission_adviser_sum,
            'commission_manager': commission_manager_sum,
            'adviser': model_to_dict(adviser) if adviser else None,
            'manager': model_to_dict(manager) if manager else None,
        }

    @staticmethod
    def create_details_payment(payment_adviser_commissions_id, payment_commissions_details_list):
        create_detail_list = []

        for adviser in Advisers.objects.filter(deleted=False):

            for payment_commissions_details in payment_commissions_details_list:

                if payment_commissions_details['adviser']['id'] != adviser.id:
                    continue

                value_commission = payment_commissions_details['value_commission']

                if value_commission == Decimal(0):
                    continue

                create_detail_list.append(
                    PaymentAdviserCommissionsDetails(
                        payment_adviser_commissions_id=payment_adviser_commissions_id,
                        value_commission=value_commission,
                        adviser_id=payment_commissions_details['adviser']['id'],
                        pay=False
                    )
                )

        PaymentAdviserCommissionsDetails.objects.bulk_create(create_detail_list)
