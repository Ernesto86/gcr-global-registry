from urllib.parse import urlencode

from django.db.models import Q
from django.views.generic import ListView

from core.constants import RegistrationStatus
from core.util_functions import ListViewFilter
from institutions.models import Institutions
from security.functions import addUserData
from security.mixins import *
from system.models import SysCountries


class InstitutionsViewListView(PermissionMixin, ListViewFilter, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'institutions/institution/list.html'
    context_object_name = 'institutions'
    permission_required = 'view_institutions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        get_params = {k: v[0] for k, v in dict(self.request.GET).items()}
        context.update(get_params)
        try:
            get_params.pop('page')
        except:
            pass
        context['url_params'] = urlencode(get_params)
        context['status'] = RegistrationStatus.choices
        context['countries'] = SysCountries.objects.filter(deleted=False)
        try:
            context['country_id'] = int(context['country_id']) if context['country_id'] else ''
        except:
            pass
        return context

    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search', '')
        self.query_filter = {
            'registration_status': self.request.GET.get('status_id', ''),
            'country_id': self.request.GET.get('country_id', '')
        }

        return Institutions.objects.filter(
            Q(deleted=False),
            Q(adviser__user_id=self.request.user.pkid),
            Q(code__icontains=search) |
            Q(name__icontains=search),
            *self.queries()
        ).order_by(
            '-created_at',
            'name'
        )
