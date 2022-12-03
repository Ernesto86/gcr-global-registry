from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView

from core.common.filter_orm.filter_orm_common import FilterOrmCommon
from core.util_functions import ListViewFilter
from institutions.models import InsTypeRegistries
from security.functions import addUserData
from students.models import StudentRegisters


class OrganizadorRegistroListView(ListViewFilter, LoginRequiredMixin, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'security/organizador_registros/listado.html'
    context_object_name = 'StudentRegisters'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        ins_type_registries = InsTypeRegistries.objects.get(id=self.kwargs.get("typeregisterid"))
        context['title_label'] = f'Registros de {ins_type_registries.name} - {ins_type_registries.detail}'.upper()
        context['clear_url'] = reverse_lazy('organizador_detalle', kwargs={'typeregisterid': ins_type_registries.id})

        get_params = FilterOrmCommon.get_url_params(self.request.GET)
        context.update(get_params)
        context['url_params'] = urlencode(get_params)
        return context

    def get_queryset(self, **kwargs):
        self.query_AND_1, self.query_OR_1 = FilterOrmCommon.get_query_connector_tuple()
        search = self.request.GET.get('search', '')
        type_register_id = self.kwargs.get("typeregisterid")

        self.query_AND_1.children.append(("type_register_id", type_register_id))
        self.query_AND_1.children.append(("institution_id", self.request.user.institution_id))

        if search:
            self.query_OR_1.children.append(("student__last_name__icontains", search))
            self.query_OR_1.children.append(("student__first_name__icontains", search))
            self.query_OR_1.children.append(("student__email__icontains", search))
            self.query_OR_1.children.append(("student__dni__icontains", search))

        FilterOrmCommon.get_filter_date_range(self.request.GET, 'created_at', self.query_AND_1)

        return StudentRegisters.objects.select_related(
            "institution",
            "student",
            "type_register",
            "certificate",
            "country"
        ).filter(
            self.query_AND_1,
            self.query_OR_1
        ).order_by(
            "-date_issue"
        )

        # search = self.request.GET.get('search', '')
        #
        # if search:
        #     print("por akiiiiiiiissssss")
        #     self.filter_date('fecha')
        #     return StudentRegisters.objects.filter(
        #         Q(name__icontains=search),
        #         *self.queries()
        #     ).order_by(
        #         '-created_at'
        #     )
        # else:
        #     print("por akiiiiiiiissssss2222")
        #     typeregister = self.kwargs.get("typeregisterid")
        #     return StudentRegisters.objects.select_related(
        #         "institution",
        #         "student",
        #         "type_register",
        #         "certificate",
        #         "country"
        #     ).filter(
        #         type_register_id=typeregister,
        #         institution__created_by=self.request.user.username
        #     ).order_by(
        #         "-date_issue"
        #     )
