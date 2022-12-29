from django.urls import path

from advisers.view.adviser import AdviserListView, AdviserCreateView, AdviserUpdateView, AdviserDeleteView
from advisers.view.adviser_profile import AdviserProfileUpdateView
from advisers.view.advisers_commissions import AdvisersCommissionsListView, AdvisersCommissionsCreateView, AdvisersCommissionsUpdateView
from advisers.view.dashboard_admin import DashboardAdminView
from advisers.view.dashboard_advisor import DashboardAdvisorView
from advisers.view.manager import ManagerListView, ManagerCreateView, ManagerUpdateView, ManagerDeleteView
from advisers.view.manager_profile import ManagerProfileUpdateView
from advisers.view.managers_commissions import ManagersCommissionsListView, ManagersCommissionsCreateView, ManagersCommissionsUpdateView
from advisers.view.dashboard_manager import DashboardManagerView
from advisers.view.payment_adviser_commissions import PaymentAdviserCommissionsListView, PaymentAdviserCommissionsCreateView, PaymentAdviserCommissionsUpdateView
from advisers.view.payment_method.view import PaymentMethodDeleteView, PaymentMethodUpdateView, PaymentMethodCreateView, \
    PaymentMethodListView
from advisers.view.period_commissions.view import PeriodCommissionsUpdateView

app_name = 'advisers'

urlpatterns = [
    path('advisers', AdviserListView.as_view(), name='adviser_list'),
    path('advisers/create', AdviserCreateView.as_view(), name='adviser_create'),
    path('advisers/update/<int:pk>', AdviserUpdateView.as_view(), name='adviser_update'),
    path('advisers/delete/<int:pk>', AdviserDeleteView.as_view(), name='adviser_delete'),
    path('adviser-profile/update', AdviserProfileUpdateView.as_view(), name='adviser_profile_update'),

    path('managers', ManagerListView.as_view(), name='manager_list'),
    path('managers/create', ManagerCreateView.as_view(), name='manager_create'),
    path('managers/update/<int:pk>', ManagerUpdateView.as_view(), name='manager_update'),
    path('managers/delete/<int:pk>', ManagerDeleteView.as_view(), name='manager_delete'),
    path('manager-profile/update', ManagerProfileUpdateView.as_view(), name='manager_profile_update'),

    path('dashboard-advisor', DashboardAdvisorView.as_view(), name='dashboard_advisor'),
    path('dashboard-manager', DashboardManagerView.as_view(), name='dashboard_manager'),
    path('dashboard-admin', DashboardAdminView.as_view(), name='dashboard_admin'),
    path('advisers-commissions', AdvisersCommissionsListView.as_view(), name='advisers_commissions_list'),
    path('advisers-commissions/create', AdvisersCommissionsCreateView.as_view(), name='advisers_commissions_create'),
    path('advisers-commissions/update/<int:pk>', AdvisersCommissionsUpdateView.as_view(), name='advisers_commissions_update'),

    path('managers-commissions', ManagersCommissionsListView.as_view(), name='managers_commissions_list'),
    path('managers-commissions/create', ManagersCommissionsCreateView.as_view(), name='managers_commissions_create'),
    path('managers-commissions/update/<int:pk>', ManagersCommissionsUpdateView.as_view(), name='managers_commissions_update'),

    path(
        'advisers-commissions-payment', PaymentAdviserCommissionsListView.as_view(), name='payment_adviser_commissions_list'
    ),
    path(
        'advisers-commissions-payment/create',
        PaymentAdviserCommissionsCreateView.as_view(),
        name='payment_adviser_commissions_create'
    ),
    path(
        'advisers-commissions-payment/update/<int:pk>',
        PaymentAdviserCommissionsUpdateView.as_view(),
        name='payment_adviser_commissions_update'
    ),

    path('payment-method', PaymentMethodListView.as_view(), name='payment_method_list'),
    path('payment-method/create', PaymentMethodCreateView.as_view(), name='payment_method_create'),
    path('payment-method/update/<int:pk>', PaymentMethodUpdateView.as_view(), name='payment_method_update'),
    path('payment-method/delete/<int:pk>', PaymentMethodDeleteView.as_view(), name='payment_method_delete'),

    path('period-commissions/update', PeriodCommissionsUpdateView.as_view(), name='period_commissions_update'),
]
