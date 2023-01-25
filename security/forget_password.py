from uuid import uuid4
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from core.common.filter_query.filter_query_common import FilterQueryCommon
from core.services.recaptcha.recaptcha_service import RecaptchaService
from .models import User
from security.forms import ResetPasswordForm
from security.functions import addUserData
from core.send_email import render_to_email_send
from .models import User
from core.constants import SYSTEM_NAME


class ResetPasswordView(TemplateView):
    success_url = reverse_lazy('login')
    template_name = 'security/forget_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recuperar Password'
        context['recaptcha_site_key'] = RecaptchaService.get_recaptcha_site_key()
        context['form'] = ResetPasswordForm()
        addUserData(self.request, context)
        return context


    def post(self, request, *args, **kwargs):

        form = ResetPasswordForm(self.request.POST)

        recaptcha = FilterQueryCommon.get_param_validate(self.request.POST.get("g-recaptcha-response", None))
        validate_recaptcha = RecaptchaService(recaptcha).validate_facade()
        if not validate_recaptcha[0]:
            messages.add_message(request, messages.ERROR, validate_recaptcha[1])
            return render(request, self.template_name, {'form': form, 'recaptcha_site_key': RecaptchaService.get_recaptcha_site_key()})

        email = self.request.POST.get('email')
        user = User.objects.filter(email=email, is_active = True).first()

        if user is not None:
            user.reset_token = uuid4()
            user.save()

            render_to_email_send(
                subject="Restablacer contraseña de cuenta de usuario en Global Registry",
                body={
                    'user': user,
                    'url_reset_password': f"http://localhost:8001/security/reset-password/{user.id},{user.reset_token}",
                    'system_name': SYSTEM_NAME,
                },
                receiver=[user.email],
                template='email/reset_password.html'
            )
            messages.add_message(request, messages.INFO, f"Se envio exitosamente. Revise su correo electronico:")
            return redirect('password_reset')
        else:
            messages.add_message(request, messages.ERROR, f"Correo ingresado es incorrecto")

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'recaptcha_site_key': RecaptchaService.get_recaptcha_site_key()
            }
        )

# class UsuarioCambiarClave(View):
#     def post(self, request, *args, **kwargs):
#         data = {'resp': False}
#         try:
#             norobot = request.POST.get('norobot', '')
#             if not norobot:
#                 raise Exception("Fallido!, acceso No autorizado.")

#             persona = CatPersona.objects.get(pk=request.POST.get('estudiante_id'))
#             if persona.usuario is not None:
#                 usuario = persona.usuario
#                 if usuario.is_active:
#                     usuario.set_password(str(request.POST.get('password')))
#                     usuario.save()
#                     data['resp']=True
#                     return JsonResponse(data, status=200)

#             data['error'] = "La cuenta de usuario no se encuentra habilitada.."
#         except Exception as e:
#             data['error'] = "No se encontró información cuenta de usuario del estudiante vuelva a intentarlo.."
#         return JsonResponse(data, status=200)

# def solicitar_cambio_clave_form(request,id,ced,token):
#     try:
#         data={}
#         if CatPersona.objects.filter(anulado=False,cedula=ced,token=token).exists():
#             data['persona'] = CatPersona.objects.get(pk=id)
#             return render(request, 'seguridad/solicitud_cambio_clave.html', data)
#     except Exception as e:
#         pass
#     return redirect('/')
