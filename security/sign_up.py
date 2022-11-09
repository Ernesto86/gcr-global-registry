from django.urls import reverse_lazy
from core.send_email import render_to_email_send
from security.forms import SignUpRegisterForm
from django.views.generic import CreateView
from security.functions import addUserData
from .models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from core.constants import SYSTEM_NAME


class SignUpView(CreateView):
    model = User
    form_class = SignUpRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'security/sign_up.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrarse'
        addUserData(self.request, context)
        return context

    def post(self, request, *args, **kwargs):
        norobot = request.POST.get('norobot', None)
        form = self.get_form()

        if norobot is None:
            messages.error(self.request, "Field norobot is required")
            return render(request, self.template_name, {'form': form})

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
                    #'mensaje': mensaje,
                    'system_name': SYSTEM_NAME,
                },
                receiver=[user.email],
                template='email/user_email_register.html'
            )
            messages.add_message(request, messages.INFO, f"Cuenta creada exitosamente. Revise su correo electronico: {user.email}")
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})
