from urllib.parse import urlencode
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from institutions.forms import InstitutionForm
from institutions.models import Institutions
from security.functions import addUserData
from core.util_functions import ListViewFilter

class InstitutionsListView(ListViewFilter, LoginRequiredMixin, ListView):
    login_url = '/security/login'
    redirect_field_name = 'redirect_to'
    template_name = 'institutions/list.html'
    context_object_name = 'institutions'
    paginate_by = 2

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
        return context


    def get_queryset(self, **kwargs):
        search = self.request.GET.get('search', '')
        self.filter_date('fecha')
        return Institutions.objects.filter(
            Q(name__icontains=search),
            *self.queries()
        ).order_by(
            '-created_at'
        )

class InstitutionCreateView(CreateView):
    model = Institutions
    template_name = 'institutions/create.html'
    form_class = InstitutionForm
    success_url = reverse_lazy('institution_list')
    permission_required = 'add_institutions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = reverse_lazy('institution_list')
        context['form_action'] = 'Crear'
        return context

class InstitutionUpdateView(UpdateView):
    model = Institutions
    template_name = 'institutions/create.html'
    form_class = InstitutionForm
    success_url = reverse_lazy('institution_list')
    permission_required = 'add_institutions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = reverse_lazy('institution_list')
        context['form_action'] = 'Actualizar'
        return context

class InstitutionDelete(View):
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        Institutions.objects.get(pk=id).delete()
        return JsonResponse({}, status=200)
