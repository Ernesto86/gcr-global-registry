from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView

from advisers.manager.payment_adviser_commissions_manager import PaymentAdviserCommissionsManager
from advisers.models import Advisers, PaymentAdviserCommissions
from advisers.view.dashboard_adviser.Adviser import AdviserDashboard
from core.common.filter_query.filter_query_common import FilterQueryCommon
from institutions.models import Institutions
from security.functions import addUserData


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

            adviser_dashboard = AdviserDashboard(advisers)

            if option_view == 'paid':
                # data.update(
                #     PaymentAdviserCommissionsManager.get_detail_adviser_payment(
                #         PaymentAdviserCommissions.TYPE_FUNCTIONARY[1][0],
                #         advisers.id,
                #         institution_id=institution_id,
                #         pay_adviser=True
                #     )
                # )
                data.update(adviser_dashboard.get_detail_sales_collected_per_range_year())

            elif option_view == 'xcobrar':
                # data.update(
                #     PaymentAdviserCommissionsManager.get_detail_adviser_payment(
                #         PaymentAdviserCommissions.TYPE_FUNCTIONARY[1][0],
                #         advisers.id,
                #         institution_id=institution_id,
                #         pay_adviser=False
                #     )
                # )
                data.update(adviser_dashboard.get_detail_sales_by_collect_per_range_year())

            status = 200
            data['message'] = ''

        elif action == 'commission_paid':
            year_selected = FilterQueryCommon.get_param_validate(request.POST.get('year', None))
            advisers = Advisers.objects.get(user_id=self.request.user.pkid)
            status = 200

            adviser_dashboard = AdviserDashboard(advisers)

            if year_selected:
                data['payment_paid_list'] = adviser_dashboard.get_commission_collected_per_year(year_selected)
            else:
                data['payment_paid_list'] = adviser_dashboard.get_commission_collected_per_range_year()

        elif action == 'commission_x_cobrar':
            year_selected = FilterQueryCommon.get_param_validate(request.POST.get('year', None))
            advisers = Advisers.objects.get(user_id=self.request.user.pkid)
            status = 200

            adviser_dashboard = AdviserDashboard(advisers)

            if year_selected:
                data['payment_paid_list'] = adviser_dashboard.get_commission_by_collect_per_year(year_selected)
            else:
                data['payment_paid_list'] = adviser_dashboard.get_commission_by_collect_per_range_year()

        elif action == 'commission_totals':
            year_selected = FilterQueryCommon.get_param_validate(request.POST.get('year', None))
            advisers = Advisers.objects.get(user_id=self.request.user.pkid)
            status = 200

            adviser_dashboard = AdviserDashboard(advisers)

            if year_selected:
                data['payment_paid_list'] = adviser_dashboard.get_totals_sales_per_year(year_selected)
            else:
                data['payment_paid_list'] = adviser_dashboard.get_totals_sales_per_range_year()

        return JsonResponse(data, status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['advisers'] = advisers = Advisers.objects.get(user_id=self.request.user.pkid)

        adviser_dashboard = AdviserDashboard(advisers)

        context['year_list'] = adviser_dashboard.get_range_last_year()
        context['institutions_active_count'] = adviser_dashboard.get_institutions_active_count()
        context['institutions_disabled_count'] = adviser_dashboard.get_institutions_disabled_count()
        context['value_commission_payment'] = adviser_dashboard.get_commission_collected()
        context['order_subtotal'] = adviser_dashboard.get_totals_sales()
        context['value_commission_x_cobrar'] = adviser_dashboard.get_commission_by_collect()
        context['institutions_list'] = Institutions.objects.filter(adviser_id=advisers.id)

        return context
