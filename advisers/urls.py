from django.urls import path

from advisers.view.advisers_commissions import AdvisersCommissionsListView, AdvisersCommissionsCreateView, AdvisersCommissionsUpdateView
from advisers.view.dashboard_advisor import DashboardAdvisorView
from advisers.view.dashboard_manager import DashboardManagerView
from advisers.view.payment_adviser_commissions import PaymentAdviserCommissionsListView, PaymentAdviserCommissionsCreateView, PaymentAdviserCommissionsUpdateView

app_name = 'advisers'

urlpatterns = [
    path('dashboard-advisor', DashboardAdvisorView.as_view(), name='dashboard_advisor'),
    path('dashboard-manager', DashboardManagerView.as_view(), name='dashboard_manager'),
    path('advisers-commissions', AdvisersCommissionsListView.as_view(), name='advisers_commissions_list'),
    path('advisers-commissions/create', AdvisersCommissionsCreateView.as_view(), name='advisers_commissions_create'),
    path('advisers-commissions/update/<int:pk>', AdvisersCommissionsUpdateView.as_view(), name='advisers_commissions_update'),
    path('advisers-commissions-payment', PaymentAdviserCommissionsListView.as_view(), name='payment_adviser_commissions_list'),
    path('advisers-commissions-payment/create', PaymentAdviserCommissionsCreateView.as_view(), name='payment_adviser_commissions_create'),
    path('advisers-commissions-payment/update/<int:pk>', PaymentAdviserCommissionsUpdateView.as_view(), name='payment_adviser_commissions_update'),
]
