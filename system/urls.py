from django.urls import path

# from . import views
from system.view.parameter.view import SysParameterListView, SysParameterCreateView, SysParameterUpdateView, \
    SysParameterDeleteView

app_name = 'system'

urlpatterns = [
    # path(
    #     "countries/", views.ListSysCountriesAPIView.as_view(), name="countries"
    # ),

    path('sys-parameters', SysParameterListView.as_view(), name='sys_parameter_list'),
    path('sys-parameters/create', SysParameterCreateView.as_view(), name='sys_parameter_create'),
    path('sys-parameters/update/<int:pk>', SysParameterUpdateView.as_view(), name='sys_parameter_update'),
    path('sys-parameters/delete/<int:pk>', SysParameterDeleteView.as_view(), name='sys_parameter_delete'),
]
