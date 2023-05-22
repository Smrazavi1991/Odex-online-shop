from django.shortcuts import render
from django.views import View
from core.views import BasicViewMixin


class RegisterOrLogin(View, BasicViewMixin):
    def get(self, request):
        self.template_name = "user/register-login.html"
        return super().get(request)