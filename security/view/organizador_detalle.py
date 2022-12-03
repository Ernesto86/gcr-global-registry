from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView

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
        get_params = {k: v[0] for k, v in dict(self.request.GET).items()}
        context.update(get_params)
        try:
            get_params.pop('page')
        except:
            pass
        context['url_params'] = urlencode(get_params)
        return context

    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search', '')

        if search:
            self.filter_date('fecha')
            return StudentRegisters.objects.filter(
                Q(name__icontains=search),
                *self.queries()
            ).order_by(
                '-created_at'
            )
        else:
            typeregister = self.kwargs.get("typeregisterid")
            return StudentRegisters.objects.select_related(
                "institution",
                "student",
                "type_register",
                "certificate",
                "country"
            ).filter(
                type_register_id=typeregister,
                institution__created_by=self.request.user.username
            ).order_by(
                "-date_issue"
            )
