import datetime
from decimal import Decimal

from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView
from security.mixins import PermissionMixin

from advisers.models import PeriodCommissions, AdvisersCommissions, ManagersCommissions
from core.util_functions import util_null_to_decimal
from institutions.models import InsTypeRegistries, Institutions
from security.functions import addUserData
from transactions.manager.shopping_cart_manager import ShoppingCartManager
from transactions.models import OrderInstitutionQuotas, OrderInstitutionQuotaDetails, InstitutionQuotesTypeRegister


class ShoppingCartView(PermissionMixin, TemplateView):
    template_name = 'transactions/shopping_cart/view.html'
    permission_required = 'add_orderinstitutionquotas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['quota_sum'] = ShoppingCartManager.get_quota_sum(self.request.session.get('shopping_cart', None))

        institution = Institutions.objects.select_related(
            "type_registration"
        ).get(
            id=context['user'].institution_id
        )

        ins_type_registries_list = institution.get_type_register_enabled_list()

        context['type_registries_list'] = [
            {
                'type_registries': x,
                'institution_id': institution.id,
                'price_discount': x.get_price_with_discount(institution.get_discount_decimal()),
                'quota_balance': ShoppingCartManager.get_quota_balance(x.id, institution.id),
                'has_type_register_assigned': ins_type_registries_list.filter(id=x.id).exists()
            }
            for x in InsTypeRegistries.objects.all().order_by('code')
        ]

        return context

    def post(self, request):
        action = request.POST.get('action')

        if action == 'add_item':

            shopping_cart = request.session.get('shopping_cart')
            type_register_id = int(request.POST.get('typeRegisterId'))
            type_register_id_str = str(type_register_id)
            quotes = int(request.POST.get('quotes'))

            if shopping_cart is None:
                request.session['shopping_cart'] = {
                    type_register_id_str: quotes
                }
            else:
                if request.session['shopping_cart'].get(type_register_id_str):
                    request.session['shopping_cart'][type_register_id_str] = int(
                        request.session['shopping_cart'][type_register_id_str]) + quotes
                else:
                    request.session['shopping_cart'][type_register_id_str] = quotes

        request.session['xd'] = "que rayos esta pasando"
        return JsonResponse({
            'quota_sum': ShoppingCartManager.get_quota_sum(request.session.get('shopping_cart', None))
        })


class ShoppingCartBuyView(PermissionMixin, TemplateView):
    template_name = 'transactions/shopping_cart/buy.html'
    permission_required = 'add_orderinstitutionquotas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)

        context['shopping_cart'] = self.request.session.get('shopping_cart')
        context['subtotal'] = 0
        context['type_registries_list'] = []
        institution = Institutions.objects.select_related(
            "type_registration"
        ).get(
            created_by=context['user'].username
        )

        if context.get('shopping_cart'):

            for k, v in context['shopping_cart'].items():
                ins_type_registries = InsTypeRegistries.objects.get(id=k)
                quotas = v
                price_discount = ins_type_registries.get_price_with_discount(institution.get_discount_decimal())
                price = price_discount * int(quotas)
                context['subtotal'] += price

                context['type_registries_list'].append(
                    {
                        'type_registries': ins_type_registries,
                        'institution_id': institution.id,
                        'price_discount': price_discount,
                        'quota_balance': ShoppingCartManager.get_quota_balance(ins_type_registries.id, institution.id),
                        'quotes': v,
                        'price': price,
                    }
                )

            context['type_registries_list'].sort(key=lambda x: x['type_registries'].code)

        context['show_bottom_pay'] = len(context['type_registries_list']) > 0

        return context

    def post(self, request):
        action = request.POST.get('action')

        if action == 'delete_item':
            type_register_id = int(request.POST.get('typeRegisterId'))
            type_register_id_str = str(type_register_id)
            request.session['shopping_cart'].pop(type_register_id_str)
            request.session['cual'] = None

        elif action == 'pay':
            shopping_cart = request.session.get('shopping_cart')
            institution = Institutions.objects.get(created_by=request.user.username)
            date_buy = datetime.datetime.now()

            if shopping_cart:
                print("mas arriba")
                managers_commissions = ManagersCommissions.objects.get(manager_id=institution.adviser.manager_id, deleted=False)

                commissions_advisers_find = self.commissions_advisers_find(institution)

                order_institution_quotas = OrderInstitutionQuotas.objects.create(
                    institution_id=institution.id,
                    adviser_id=institution.adviser_id,
                    manager_id=institution.adviser.manager_id,
                    date_issue=date_buy,
                    discount_percentage=institution.discount,
                    taxes_percentage=Decimal(0),
                    commissions_advisers_percentage=commissions_advisers_find,
                    commissions_managers_percentage=managers_commissions.value,
                )

                for k, v in shopping_cart.items():
                    ins_type_registries = InsTypeRegistries.objects.get(id=k)
                    quotas = int(v)

                    values_discount = ins_type_registries.get_price_with_discount(institution.get_discount_decimal())
                    OrderInstitutionQuotaDetails.objects.create(
                        order_institution_quota_id=order_institution_quotas.id,
                        type_register_id=ins_type_registries.id,
                        quotas=quotas,
                        values=ins_type_registries.price,
                        values_discount=values_discount,
                        total_item=util_null_to_decimal(quotas * values_discount)
                    )

                    self.create_or_update_institution_quotes_type_register(
                        institution.id,
                        ins_type_registries.id,
                        quotas
                    )

                order_institution_quotas.calculate()

                request.session.pop('shopping_cart')
        return JsonResponse({})

    def commissions_advisers_find(self, institution_instance):
        date_approval = institution_instance.date_approval
        date_buy = datetime.datetime.now().date()

        period_commissions = PeriodCommissions.objects.filter(deleted=False).last()
        advisers_commissions = AdvisersCommissions.objects.get(adviser_id=institution_instance.adviser_id, deleted=False)

        if period_commissions:
            date_approval += datetime.timedelta(days=period_commissions.days_commissions_period_1)

            if date_buy <= date_approval:
                return advisers_commissions.commissions_period_1

            date_approval += datetime.timedelta(days=period_commissions.days_commissions_period_2)

            if date_buy <= date_approval:
                return advisers_commissions.commissions_period_2

            date_approval += datetime.timedelta(days=period_commissions.days_commissions_period_3)

            if date_buy <= date_approval:
                return advisers_commissions.commissions_period_3

        return Decimal(0)

    def create_or_update_institution_quotes_type_register(self, institution_id, ins_type_registries_id, quotas):
        try:
            institution_quotes_type_register = InstitutionQuotesTypeRegister.objects.get(
                institution_id=institution_id,
                type_register_id=ins_type_registries_id,
                deleted=False
            )
        except:
            institution_quotes_type_register = InstitutionQuotesTypeRegister.objects.create(
                institution_id=institution_id,
                type_register_id=ins_type_registries_id
            )

        institution_quotes_type_register.quotas += quotas
        institution_quotes_type_register.quotas_balance += quotas
        institution_quotes_type_register.save()
