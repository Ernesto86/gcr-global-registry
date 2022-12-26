from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from rest_framework import status

from advisers.forms import ManagerProfileForm
from advisers.models import Managers
from core.common.form.form_common import FormCommon
from security.functions import addUserData
from security.mixins import *


class ManagerProfileUpdateView(PermissionMixin, UpdateView):
    model = Managers
    template_name = 'advisers/manager_profile/create.html'
    form_class = ManagerProfileForm
    success_url = reverse_lazy('home')
    permission_required = 'change_managers'

    def get_object(self):
        return Managers.objects.get(user_id=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ""}
        action = request.POST['action']

        if action == 'edit':
            instance = self.get_object()
            form = self.form_class(data=self.request.POST, instance=instance)

            if form.is_valid():
                form.save()
                form.instance.user.first_name = form.instance.first_name
                form.instance.user.last_name = form.instance.last_name
                form.instance.user.save()
                return JsonResponse(data, status=status.HTTP_200_OK)

            data['message'] = 'Error de validacion de formulario.'
            data['errors'] = [FormCommon.get_errors_dict(form)]
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['back_url'] = self.success_url
        context['title_label'] = 'Actualizar perfil'
        context['action'] = 'edit'
        return context
