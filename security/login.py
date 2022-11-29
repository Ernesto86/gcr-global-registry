import os
import requests
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy

from core.common.filter_query.filter_query_common import FilterQueryCommon
from security.functions import addUserData
from django.views.generic import RedirectView


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
        context['recaptcha_site_key'] = os.environ.get('RECAPTCHA_SITE_KEY', '')
        return context

    def post(self, request, *args, **kwargs):
        data = {'errors': []}
        status = 200

        recaptcha = FilterQueryCommon.get_param_validate(self.request.POST.get("g-recaptcha-response", None))
        recaptcha_secret_key = os.environ.get('RECAPTCHA_SECRET_KEY', '')

        recaptcha_data = {
            "secret": recaptcha_secret_key,
            "response": recaptcha
        }

        try:
            response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify?secret={}&response={}'.format(
                    recaptcha_secret_key,
                    recaptcha
                ),
                data=json.dumps(recaptcha_data)
            )
        except Exception as e:
            data['errors'] = ["Error de captcha"]
            return JsonResponse(data, status=400)

        if response.status_code != 200:
            data['errors'] = ["Error de captcha"]
            return JsonResponse(data, status=400)

        response_json = response.json()

        if not response_json['success']:
            data['errors'] = ["Error de captcha"]
            return JsonResponse(data, status=400)

        try:
            cuenta = str(request.POST.get('username')).strip()
            password = str(request.POST.get('password')).strip()

            user = authenticate(username=cuenta, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    data['code'] = 'success'
                    data['message'] = 'Login user successful'
                else:
                    status = 400
                    data['message'] = 'Login user session failed'
                    data['errors'].append('Login Fallido!, usuario no esta habilitado')
            else:
                status = 400
                data['message'] = 'Login user session failed'
                data['errors'].append('Login Fallido!, credenciales incorrectas.')

        except Exception as e:
            status = 500
            data['message'] = 'Internal error in code'
            data['errors'].append(str(e))

        return JsonResponse(data, status=status)


class LogoutRedirectView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
