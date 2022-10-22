from django.views.generic.base import TemplateView

from system.constants import LOGO_SISTEMA, SISTEMA_PAGINA_WEB, NOMBRE_SISTEMA


class MainView(TemplateView):
    template_name = 'security/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['autor'] = ''
        context['sistema_logo'] = LOGO_SISTEMA
        context['sistema_web'] = SISTEMA_PAGINA_WEB
        context['sistema_nombre'] = NOMBRE_SISTEMA
        return context
