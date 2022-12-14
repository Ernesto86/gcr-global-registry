import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from rest_framework import status as status_verbose
from urllib.parse import urlencode

from advisers.choices import TL_MONTH
from advisers.forms import PaymentAdviserCommissionsForm
from advisers.manager.payment_adviser_commissions_manager import PaymentAdviserCommissionsManager
from advisers.models import PaymentAdviserCommissions, PaymentAdviserCommissionsDetails
from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from security.functions import addUserData
from transactions.models import OrderInstitutionQuotas


class PaymentAdviserCommissionsListView(LoginRequiredMixin, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/payment_adviser_commissions/list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['title_label'] = "Listado de pagos".upper()
        context['create_url'] = reverse_lazy('advisers:payment_adviser_commissions_create')
        context['clear_url'] = reverse_lazy('advisers:payment_adviser_commissions_list')

        get_params = FilterOrmCommon.get_url_params(self.request.GET)
        context.update(get_params)
        context['url_params'] = urlencode(get_params)
        return context

    def get_queryset(self, **kwargs):
        self.query_AND_1, self.query_OR_1 = FilterOrmCommon.get_query_connector_tuple()
        search = self.request.GET.get('search', '')

        if search:
            self.query_OR_1.children.append(("number__icontains", search))

        FilterOrmCommon.get_filter_date_range(self.request.GET, 'date_payment', self.query_AND_1)

        return PaymentAdviserCommissions.objects.filter(
            self.query_AND_1,
            self.query_OR_1,
            deleted=False,
        ).order_by('-created_at')


class PaymentAdviserCommissionsCreateView(CreateView):
    model = PaymentAdviserCommissions
    template_name = 'advisers/payment_adviser_commissions/create.html'
    # template_name = 'advisers/payment_adviser_commissions/create_original.html'
    form_class = PaymentAdviserCommissionsForm
    success_url = reverse_lazy('advisers:payment_adviser_commissions_list')
    permission_required = 'add_institutions'

    def get_next_date_validate(self, year, month, is_first=False):
        year = int(year)
        month = int(month)

        if is_first:
            return {
                'year': year,
                'month': month
            }

        if month == TL_MONTH[12][0]:
            return {
                'year': year + 1,
                'month': TL_MONTH[1][0]
            }

        return {
            'year': year,
            'month': month + 1
        }

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        status = 500

        action = request.POST.get('action', '')
        if action == 'add':
            try:
                status = 200
                print("akaaaaaaaaa")
                type_functionary = int(request.POST.get('type_functionary', ''))
                year = int(request.POST.get('year', ''))
                month = int(request.POST.get('month', ''))
                date_payment = datetime.datetime.now()

                print("adentro")
                data['calculate_payment_commissions'] = PaymentAdviserCommissionsManager.get_calculate_payment_commissions(
                    type_functionary,
                    year,
                    month
                )
                print("afuera")

                PaymentAdviserCommissionsManager.validate_or_raise_name_error(year, month, type_functionary)

                print("no te cachoooooooo")

                try:
                    payment_adviser_commissions = PaymentAdviserCommissions.objects.get(
                        type_functionary=type_functionary,
                        year=year,
                        month=month,
                        pay_period=False
                    )
                except Exception as ex:
                    payment_adviser_commissions = None

                print("no te aaaaaaaa")

                if payment_adviser_commissions:
                    PaymentAdviserCommissionsDetails.objects.filter(
                        payment_adviser_commissions_id=payment_adviser_commissions.id
                    ).delete()
                else:
                    print("debugear")
                    payment_adviser_commissions = PaymentAdviserCommissions.objects.create(
                        type_functionary=type_functionary,
                        date_payment=date_payment,
                        year=year,
                        month=month,
                        # TODO: INCLUIR PROCESO DE PAYPAL PARA PAY_PERYOD TRUE
                        pay_period=True
                    )
                    print("debugear 1111111")

                    update_common = {}

                    if int(type_functionary) == PaymentAdviserCommissions.TYPE_FUNCTIONARY[1][0]:
                        # TODO: INCLUIR PROCESO DE PAYPAL PARA pay_adviser TRUE
                        update_common["pay_adviser"] = True
                    else:
                        # TODO: INCLUIR PROCESO DE PAYPAL PARA pay_adviser TRUE
                        update_common["pay_manager"] = True

                    OrderInstitutionQuotas.objects.filter(
                        deleted=False,
                        date_issue__year=year,
                        date_issue__month=month,
                    ).update(
                        # TODO: INCLUIR PROCESO DE PAYPAL PARA pay_adviser TRUE
                        **update_common
                    )

                PaymentAdviserCommissionsManager.create_details_payment(
                    payment_adviser_commissions.id,
                    data['calculate_payment_commissions']['payment_commissions_details_list']
                )

                payment_adviser_commissions.calculate()

            except Exception as e:
                status = 500
                data['message'] = 'Internal error in code'
                data['errors'].append(str(e))

        elif action == 'calculate':
            try:
                status = 200
                type_functionary = int(request.POST.get('type_functionary', ''))
                year = request.POST.get('year', '')
                month = request.POST.get('month', '')

                data['calculate_payment_commissions'] = PaymentAdviserCommissionsManager.get_calculate_payment_commissions(
                    type_functionary,
                    year,
                    month
                )

            except Exception as e:
                status = 500
                data['message'] = 'Internal error in code'
                data['errors'].append(str(e))

        elif action == 'view_detail':
            type_functionary = int(request.POST.get('type_functionary', ''))
            object_id = int(request.POST.get('object_id', ''))
            year = request.POST.get('year', '')
            month = request.POST.get('month', '')

            data.update(
                PaymentAdviserCommissionsManager.get_detail_adviser_payment(
                    type_functionary,
                    object_id,
                    year,
                    month,
                )
            )

            status = 200
            data['message'] = ''

        elif action == 'get_next_date_payment':
            type_functionary = request.POST.get('type_functionary', None)

            payment_adviser_commissions = PaymentAdviserCommissions.objects.filter(
                type_functionary=type_functionary,
            ).order_by('year', 'month').last()

            if payment_adviser_commissions:
                data.update(
                    self.get_next_date_validate(
                        payment_adviser_commissions.year,
                        payment_adviser_commissions.month,
                    )
                )
                return JsonResponse(data, status=status_verbose.HTTP_200_OK)

            order_institution_quotas = OrderInstitutionQuotas.objects.filter().order_by('date_issue').first()

            if order_institution_quotas is None:
                data['errors'] = ["No existe ninguna compra realizada"]
                return JsonResponse(data, status=status_verbose.HTTP_400_BAD_REQUEST)

            data.update(
                self.get_next_date_validate(
                    order_institution_quotas.date_issue.year,
                    order_institution_quotas.date_issue.month,
                    is_first=True
                )
            )

            return JsonResponse(data, status=status_verbose.HTTP_200_OK)

        return JsonResponse(data, status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = reverse_lazy('advisers:payment_adviser_commissions_list')
        context['form_action'] = 'Crear'
        context['action'] = 'add'
        context['title_label'] = 'Crear pago'
        return context


class PaymentAdviserCommissionsUpdateView(UpdateView):
    model = PaymentAdviserCommissions
    template_name = 'advisers/payment_adviser_commissions/create.html'
    form_class = PaymentAdviserCommissionsForm
    success_url = reverse_lazy('advisers:payment_adviser_commissions_list')
    permission_required = 'add_institutions'

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        status = 500

        action = request.POST.get('action', '')
        if action == 'edit':
            try:
                status = 200
                type_functionary = int(request.POST.get('type_functionary', ''))
                year = int(request.POST.get('year', ''))
                month = int(request.POST.get('month', ''))
                payment_adviser_commissions = self.get_object()
                date_payment = datetime.datetime.now()

                data['calculate_payment_commissions'] = PaymentAdviserCommissionsManager.get_calculate_payment_commissions(
                    type_functionary,
                    year,
                    month
                )

                PaymentAdviserCommissionsManager.validate_or_raise_name_error(year, month, type_functionary)

                payment_adviser_commissions.date_payment = date_payment
                payment_adviser_commissions.save()

                PaymentAdviserCommissionsDetails.objects.filter(
                    payment_adviser_commissions_id=payment_adviser_commissions.id
                ).delete()

                PaymentAdviserCommissionsManager.create_details_payment(
                    payment_adviser_commissions.id,
                    data['calculate_payment_commissions']['payment_commissions_details_list']
                )

                payment_adviser_commissions.calculate()

            except Exception as e:
                status = 500
                data['message'] = 'Internal error in code'
                data['errors'].append(str(e))

        elif action == 'calculate':
            try:
                status = 200
                print("que paso", request.POST.get('type_functionary', ''), "no hay nada")
                type_functionary = int(request.POST.get('type_functionary', ''))
                year = request.POST.get('year', '')
                month = request.POST.get('month', '')
                print("que pasa", year, month)

                data['calculate_payment_commissions'] = PaymentAdviserCommissionsManager.get_calculate_payment_commissions(
                    type_functionary,
                    year,
                    month
                )

            except Exception as e:
                status = 500
                data['message'] = 'Internal error in code'
                data['errors'].append(str(e))

        elif action == 'view_detail':
            type_functionary = int(request.POST.get('type_functionary', ''))
            object_id = int(request.POST.get('object_id', ''))
            year = request.POST.get('year', '')
            month = request.POST.get('month', '')

            data.update(
                PaymentAdviserCommissionsManager.get_detail_adviser_payment(
                    type_functionary,
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
        context['form_action'] = 'Editar'
        context['action'] = self.request.GET.get('action', 'edit')
        return context
