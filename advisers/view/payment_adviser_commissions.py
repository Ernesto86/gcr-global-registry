import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from advisers.forms import PaymentAdviserCommissionsForm
from advisers.manager.payment_adviser_commissions_manager import PaymentAdviserCommissionsManager
from advisers.models import PaymentAdviserCommissions, PaymentAdviserCommissionsDetails
from security.functions import addUserData


class PaymentAdviserCommissionsListView(LoginRequiredMixin, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'advisers/payment_adviser_commissions/list.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        return context

    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search', '')
        return PaymentAdviserCommissions.objects.filter(
            number__icontains=search,
            deleted=False,
        ).order_by('-created_at')


class PaymentAdviserCommissionsCreateView(CreateView):
    model = PaymentAdviserCommissions
    template_name = 'advisers/payment_adviser_commissions/create.html'
    form_class = PaymentAdviserCommissionsForm
    success_url = reverse_lazy('advisers:payment_adviser_commissions_list')
    permission_required = 'add_institutions'

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        status = 500

        action = request.POST.get('action', '')
        if action == 'add':
            try:
                status = 200
                type_functionary = int(request.POST.get('type_functionary', ''))
                year = request.POST.get('year', '')
                month = request.POST.get('month', '')
                date_payment = datetime.datetime.now()

                data['calculate_payment_commissions'] = PaymentAdviserCommissionsManager.get_calculate_payment_commissions(
                    type_functionary,
                    year,
                    month
                )

                try:
                    payment_adviser_commissions = PaymentAdviserCommissions.objects.get(
                        type_functionary=type_functionary,
                        year=year,
                        month=month,
                        pay_period=False
                    )
                except Exception as ex:
                    payment_adviser_commissions = None

                if payment_adviser_commissions:
                    PaymentAdviserCommissionsDetails.objects.filter(
                        payment_adviser_commissions_id=payment_adviser_commissions.id
                    ).delete()
                else:
                    payment_adviser_commissions = PaymentAdviserCommissions.objects.create(
                        type_functionary=type_functionary,
                        date_payment=date_payment,
                        year=year,
                        month=month,
                        pay_period=False
                    )

                PaymentAdviserCommissionsManager.create_details_payment(
                    payment_adviser_commissions.id,
                    data['calculate_payment_commissions']['payment_commissions_details_list']
                )

                payment_adviser_commissions.calculate()

            except Exception as e:
                status = 500
                data['code'] = 'failed'
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
                data['code'] = 'failed'
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
        context['form_action'] = 'Crear'
        context['action'] = 'add'
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
                year = request.POST.get('year', '')
                month = request.POST.get('month', '')
                payment_adviser_commissions = self.get_object()
                date_payment = datetime.datetime.now()

                data['calculate_payment_commissions'] = PaymentAdviserCommissionsManager.get_calculate_payment_commissions(
                    type_functionary,
                    year,
                    month
                )

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
                data['code'] = 'failed'
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
                data['code'] = 'failed'
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
