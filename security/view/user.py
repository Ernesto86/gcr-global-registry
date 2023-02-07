from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from rest_framework import status

from core.common.form.form_common import FormCommon
from security.functions import addUserData


class UserUpdatePasswordView(FormView):
    template_name = 'security/user/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs = {
            'class': 'form-control',
            'autocomplete': 'off',
            'placeholder': 'Ingrese su contraseña actual',
        }
        form.fields['new_password1'].widget.attrs = {
            'class': 'form-control',
            'autocomplete': 'off',
            'placeholder': 'Ingrese su nueva contraseña',
        }
        form.fields['new_password2'].widget.attrs = {
            'class': 'form-control',
            'autocomplete': 'off',
            'placeholder': 'Repita su contraseña',
        }
        return form

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ""}
        action = request.POST['action']

        if action == 'edit':
            form = self.form_class(user=request.user, data=self.request.POST)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return JsonResponse(data, status=status.HTTP_200_OK)

            data['message'] = 'Error de validacion de formulario.'
            data['errors'] = [FormCommon.get_errors_dict(form)]
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['back_url'] = self.success_url
        context['title_label'] = 'Cambio de contraseña'
        context['action'] = 'edit'
        return context
