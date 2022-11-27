from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from security.functions import addUserData

class HomeView(LoginRequiredMixin,View):
    login_url = '/security/main'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        data = {
            'title': "Home Global Registry"
        }
        addUserData(request, data)
        # return render(request, 'security/index_original.html', data)
        return render(request, 'security/index.html', data)
