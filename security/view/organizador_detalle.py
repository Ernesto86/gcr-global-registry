import datetime
from urllib.parse import urlencode

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from institutions.models import InsTypeRegistries

from students.models import StudentRegisters 
from security.functions import addUserData

class ListViewFilter(object):
    query_filter = {}
    def filter_date(self, date_key):
        if 'start_date' in self.request.GET:
            start_date = self.request.GET.get('start_date', '')
            end_date = self.request.GET.get('final', '')
            if start_date and end_date:
                try:
                    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
                    date_range = (
                        datetime.datetime.combine(start_date, datetime.datetime.min.time()),
                        datetime.datetime.combine(end_date, datetime.datetime.max.time())
                    )
                    self.query_filter[f'{date_key}__range'] = date_range
                except:
                    pass

    def queries(self):
        return [Q(**{k: v}) for k, v in self.query_filter.items() if v]

class OrganizadorRegistroListView(ListViewFilter, LoginRequiredMixin, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'security/organizador_registros/listado.html'
    context_object_name = 'StudentRegisters'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nameregister'] = InsTypeRegistries.objects.get(id=self.kwargs.get("typeregisterid"))
        addUserData(self.request, context)
        get_params = {k: v[0] for k, v in dict(self.request.GET).items()}
        context.update(get_params)
        try:
            get_params.pop('page')
        except:
            pass
        context['url_params'] = urlencode(get_params)
        return context


    def get_queryset(self,**kwargs):
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