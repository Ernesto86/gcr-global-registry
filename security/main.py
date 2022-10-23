from django.views.generic.base import TemplateView
from security.functions import addUserData

class MainView(TemplateView):
    template_name = 'security/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        return context
