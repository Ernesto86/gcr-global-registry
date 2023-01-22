from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from rest_framework import status

from core.common.form.form_common import FormCommon
from core.models import SystemSettings
from security.functions import addUserData
from security.mixins import *
from system.forms import SystemSettingProfileForm


class SystemSettingUpdateView(PermissionMixin, UpdateView):
    model = SystemSettings
    template_name = 'system/system_setting/create.html'
    form_class = SystemSettingProfileForm
    success_url = reverse_lazy('home')
    permission_required = 'change_systemsettings'

    def get_object(self):
        return SystemSettings.objects.all().last()

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ""}
        action = request.POST['action']

        if action == 'edit':
            instance = self.get_object()
            form = self.form_class(self.request.POST, request.FILES, instance=instance)

            if form.is_valid():
                form.save()
                return JsonResponse(data, status=status.HTTP_200_OK)

            data['message'] = 'Error de validacion de formulario.'
            data['errors'] = [FormCommon.get_errors_dict(form)]
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = self.success_url
        context['title_label'] = 'Actualizar configuracion del sistema'
        context['system_settings'] = self.get_object()
        context['action'] = 'edit'
        return context
