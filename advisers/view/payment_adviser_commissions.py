import datetime
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from advisers.forms import PaymentAdviserCommissionsForm
from advisers.models import PaymentAdviserCommissions, Advisers, PaymentAdviserCommissionsDetails, Managers
from core.util_functions import util_null_to_decimal
from security.functions import addUserData
from transactions.models import OrderInstitutionQuotas


class PaymentAdviserCommissionsListView(LoginRequiredMixin, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/payment_adviser_commissions/list.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        return context

    @staticmethod
    def get_detail_adviser_payment(payment_to, object_id, year, month):
        order_institution_quotas_list = []

        adviser = None
        manager = None

        query_AND_1 = Q()
        query_AND_1.connector = 'AND'
        query_AND_1.children.append(("deleted", False))
        query_AND_1.children.append(("date_issue__year", year))
        query_AND_1.children.append(("date_issue__month", month))

        if payment_to == PaymentAdviserCommissions.TYPE_FUNCTIONARY[0][0]:
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

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        status = 500
        data['message'] = 'Internal error in code'
        try:
            action = request.POST.get('action', '')

            if action == 'view_detail':
                pass
                # id = request.POST.get('id')
                # payment_to = int(request.POST.get('payment_to', ''))
                # payment_adviser_commissions_details = PaymentAdviserCommissionsDetails.objects.get(id=id)
                # payment_adviser_commissions = payment_adviser_commissions_details.payment_adviser_commissions
                #
                # data.update(
                #     PaymentAdviserCommissionsListView.get_detail_adviser_payment(
                #         payment_adviser_commissions_details.adviser_id,
                #         payment_adviser_commissions.year,
                #         payment_adviser_commissions.month,
                #     )
                # )
                # status = 200
                # data['message'] = ''

        except Exception as e:
            status = 500
            data['code'] = 'failed'
            data['message'] = 'Internal error in code'
            data['errors'].append(str(e))

        return JsonResponse(data, status=status)

    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search', '')
        return PaymentAdviserCommissions.objects.filter(
            deleted=False,
        ).order_by('-created_at')


class PaymentAdviserCommissionsCreateView(CreateView):
    model = PaymentAdviserCommissions
    template_name = 'advisers/payment_adviser_commissions/create.html'
    form_class = PaymentAdviserCommissionsForm
    success_url = reverse_lazy('advisers:payment_adviser_commissions_list')
    permission_required = 'add_institutions'

    def get_calculate_payment_commissions(self, payment_to, year, month):
        value_commission_sum = Decimal(0)

        query_AND_1 = Q()
        query_AND_1.connector = 'AND'
        query_AND_1.children.append(("deleted", False))
        query_AND_1.children.append(("date_issue__year", year))
        query_AND_1.children.append(("date_issue__month", month))

        if payment_to == PaymentAdviserCommissions.TYPE_FUNCTIONARY[0][0]:
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
                value_commission_adviser = order_adviser.subtotal * (order_adviser.commissions_advisers_percentage / 100)
                value_commission_manager = value_commission_adviser * (order_adviser.commissions_managers_percentage / 100)

                if payment_to == PaymentAdviserCommissions.TYPE_FUNCTIONARY[0][0]:
                    value_commission += value_commission_adviser - value_commission_manager
                else:
                    value_commission += value_commission_manager

            if value_commission == Decimal(0):
                continue

            value_commission_sum += value_commission

            payment_commissions_details_list.append(
                {
                    "payment_to": payment_to,
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

    def delete_payment(self, payment_to, year, month):
        payment_adviser_commissions_list = PaymentAdviserCommissions.objects.filter(
            type_functionary=payment_to,
            year=year,
            month=month,
            pay_period=False
        )

        if payment_adviser_commissions_list:
            for payment_adviser_commissions in payment_adviser_commissions_list:
                PaymentAdviserCommissionsDetails.objects.filter(
                    payment_adviser_commissions_id=payment_adviser_commissions.id
                ).delete()

            payment_adviser_commissions_list.delete()

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        status = 500

        action = request.POST.get('action', '')
        if action == 'add':
            try:
                status = 200
                payment_to = int(request.POST.get('payment_to', ''))
                year = request.POST.get('year', '')
                month = request.POST.get('month', '')
                date_payment = datetime.datetime.now()

                data['calculate_payment_commissions'] = self.get_calculate_payment_commissions(
                    payment_to,
                    year,
                    month
                )

                self.delete_payment(payment_to, year, month)

                payment_adviser_commissions = PaymentAdviserCommissions.objects.create(
                    type_functionary=payment_to,
                    date_payment=date_payment,
                    year=year,
                    month=month,
                    pay_period=False
                )

                create_detail_list = []

                for adviser in Advisers.objects.filter(deleted=False):

                    for payment_commissions_details in data['calculate_payment_commissions']['payment_commissions_details_list']:

                        if payment_commissions_details['adviser']['id'] != adviser.id:
                            continue

                        value_commission = payment_commissions_details['value_commission']

                        if value_commission == Decimal(0):
                            continue

                        create_detail_list.append(
                            PaymentAdviserCommissionsDetails(
                                payment_adviser_commissions_id=payment_adviser_commissions.id,
                                value_commission=value_commission,
                                adviser_id=payment_commissions_details['adviser']['id'],
                                pay=False
                            )
                        )

                PaymentAdviserCommissionsDetails.objects.bulk_create(create_detail_list)
                payment_adviser_commissions.calculate()

            except Exception as e:
                status = 500
                data['code'] = 'failed'
                data['message'] = 'Internal error in code'
                data['errors'].append(str(e))

        elif action == 'calculate':
            try:
                status = 200
                payment_to = int(request.POST.get('payment_to', ''))
                year = request.POST.get('year', '')
                month = request.POST.get('month', '')

                data['calculate_payment_commissions'] = self.get_calculate_payment_commissions(
                    payment_to,
                    year,
                    month
                )
            except Exception as e:
                status = 500
                data['code'] = 'failed'
                data['message'] = 'Internal error in code'
                data['errors'].append(str(e))

        elif action == 'view_detail':
            payment_to = int(request.POST.get('payment_to', ''))
            object_id = int(request.POST.get('object_id', ''))
            year = request.POST.get('year', '')
            month = request.POST.get('month', '')

            data.update(
                PaymentAdviserCommissionsListView.get_detail_adviser_payment(
                    payment_to,
                    object_id,
                    year,
                    month,
                )
            )

            status = 200
            data['message'] = ''

        return JsonResponse(data, status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = reverse_lazy('advisers:payment_adviser_commissions_list')
        context['form_action'] = 'Crear'
        return context
