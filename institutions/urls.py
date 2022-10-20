from django.urls import path
from institutions.views import InstitutionsListView, InstitutionCreateView, InstitutionUpdateView, InstitutionDelete

urlpatterns = [
    path('', InstitutionsListView.as_view(), name='institution_list'),
    path('create', InstitutionCreateView.as_view(), name='institution_create'),
    path('update/<int:pk>', InstitutionUpdateView.as_view(), name='institution_update'),
    path('delete/<int:pk>', InstitutionDelete.as_view(), name='institution_delete'),
]
