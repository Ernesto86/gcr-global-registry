from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import status

from core.common.filter_query.filter_query_common import FilterQueryCommon
from core.constants import SYSTEM_NAME
from core.send_email import render_to_email_send
from core.services.recaptcha.recaptcha_service import RecaptchaService
from security.forms import SignUpRegisterForm
from security.functions import addUserData
from .models import User


class SignUpView(CreateView):
    model = User
    form_class = SignUpRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'security/sign_up.html'

    # template_name = 'security/sign_up_original.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrarse'
        context['recaptcha_site_key'] = RecaptchaService.get_recaptcha_site_key()
        addUserData(self.request, context)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        recaptcha = FilterQueryCommon.get_param_validate(self.request.POST.get("g-recaptcha-response", None))

        validate_recaptcha = RecaptchaService(recaptcha).validate_facade()

        if not validate_recaptcha[0]:
            messages.add_message(request, messages.ERROR, validate_recaptcha[1])
            return render(request, self.template_name, {'form': form, 'recaptcha_site_key': RecaptchaService.get_recaptcha_site_key()})


        if form.is_valid():
            form.save()
            try:
                user = form.instance
                user.set_grup_to_user()
            except:
                pass

            render_to_email_send(
                subject="Registro de cuenta de usuario en Global Registry",
                body={
                    'user': user,
                    # 'mensaje': mensaje,
                    'system_name': SYSTEM_NAME,
                },
                receiver=[user.email],
                template='email/user_email_register.html'
            )
            messages.add_message(request, messages.INFO, f"Cuenta creada exitosamente. Revise su correo electronico: {user.email}")
            return redirect(self.success_url)
        else:
            return render(
                request,
                self.template_name,
                {
                    'form': form,
                    'recaptcha_site_key': RecaptchaService.get_recaptcha_site_key()
                }
            )
