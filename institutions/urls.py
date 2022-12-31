from django.urls import path

from institutions.view.institution.view import InstitutionsViewListView
from institutions.views import *

urlpatterns = [
    path('', InstitutionsListView.as_view(), name='institution_list'),
    path('institutions/view', InstitutionsViewListView.as_view(), name='institution_view_list'),
    path('create', InstitutionCreateView.as_view(), name='institution_create'),
    path('update/<int:pk>', InstitutionUpdateView.as_view(), name='institution_update'),
    path('delete/<int:pk>', InstitutionDelete.as_view(), name='institution_delete'),
    path('configuration', InstitutionconfigurationView.as_view(), name='institution_configuration'),
    path('register-status', InstitutionRegisterStatus.as_view(), name='register_status'),
    path('register-status/<int:pk>', InstitutionViewByPk.as_view(), name='register_status_id'),
]
