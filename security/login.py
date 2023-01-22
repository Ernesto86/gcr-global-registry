import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from rest_framework import status

from core.command.validation_upload_file_institution.validation_upload_file_institution import \
    ValidationUploadFileInstitution
from core.common.filter_query.filter_query_common import FilterQueryCommon
from core.services.recaptcha.recaptcha_service import RecaptchaService
from security.functions import addUserData


class LoginAuthView(LoginView):
    form_class = AuthenticationForm
    template_name = 'security/login.html'

    def get_form(self, form_class=None):
        form = super(LoginAuthView, self).get_form()
        form.fields['username'].widget.attrs = {
            'class': 'form-control form-control-md',
            'placeholder': 'Ingrese su username',
            'autocomplete': 'off',
            'autofocus': True
        }
        form.fields['password'].widget.attrs = {
            'class': 'form-control form-control-md',
            'placeholder': 'Ingrese su password',
            'autocomplete': 'off',
            'value': "admin123**"
        }
        return form

    def get(self, request, *args, **kwargs):
        login_different = reverse_lazy('login')
        if request.user.is_authenticated and login_different != request.path:
            return redirect(reverse_lazy('login_authenticated'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio de Sesión'
        addUserData(self.request, context)
        context['recaptcha_site_key'] = RecaptchaService.get_recaptcha_site_key()
        return context

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        recaptcha = FilterQueryCommon.get_param_validate(self.request.POST.get("g-recaptcha-response", None))

        validate_recaptcha = RecaptchaService(recaptcha).validate_facade()
        if not validate_recaptcha[0]:
            data['errors'] = [validate_recaptcha[1]]
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        try:
            cuenta = str(request.POST.get('username')).strip()
            password = str(request.POST.get('password')).strip()

            user = authenticate(username=cuenta, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    status_final = status.HTTP_200_OK
                    data['code'] = 'success'
                    data['message'] = 'Login user successful'
                else:
                    status_final = status.HTTP_400_BAD_REQUEST
                    data['message'] = 'Login user session failed'
                    data['errors'].append('Login Fallido!, usuario no esta habilitado')
            else:
                status_final = status.HTTP_400_BAD_REQUEST
                data['message'] = 'Login user session failed'
                data['errors'].append('Login Fallido!, credenciales incorrectas.')

        except Exception as e:
            status_final = status.HTTP_500_INTERNAL_SERVER_ERROR
            data['message'] = 'Internal error in code'
            data['errors'].append(str(e))

        return JsonResponse(data, status=status_final)


class LogoutRedirectView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
