import re
import datetime

from django.shortcuts import render, redirect
from django.views import View
from core.views import BasicViewMixin
from .forms import RegisterUserForm, VerificationForm, SendOTPForm
from core.tasks import send_opt_email, send_opt_sms

from .models import User


class Register(View, BasicViewMixin):

    def get(self, request):
        registeration_form = RegisterUserForm()
        return render(request, "user/register.html", {"categories": self.categories, "form": registeration_form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Login')
        return render(request, 'user/register.html', {"categories": self.categories, 'form': form})


class Verification(View, BasicViewMixin):
    def get(self, request):
        form = VerificationForm()
        return render(request, "user/verification.html", {"categories": self.categories, "form": form})


class Login(View, BasicViewMixin):
    def get(self, request):
        form = SendOTPForm()
        return render(request, 'user/login.html', {'categories': self.categories, 'form':form})

    def post(self, request):
        form = SendOTPForm(request.POST)
        if form.is_valid():
            user = None
            if re.match(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', form.cleaned_data['mail_phone']):
                try:
                    user = User.objects.get(email=form.cleaned_data['mail_phone'])
                except User.DoesNotExist:
                    pass
                if user:
                    send_opt_email.delay(form.cleaned_data['mail_phone'], 300)
                    response = redirect('Verification')
                    expiry_minutes = 5

            elif re.match(r'^(09)\d{9}$', form.cleaned_data['mail_phone']):
                try:
                    user = User.objects.get(phone=form.cleaned_data['mail_phone'])
                except User.DoesNotExist:
                    pass
                if user:
                    send_opt_sms.delay(form.cleaned_data['mail_phone'], 60)
                    response = redirect('Verification')
                    expiry_minutes = 1

            if user:
                expires = datetime.datetime.now() + datetime.timedelta(minutes=expiry_minutes)
                expires_string = expires.strftime("%a, %d-%b-%Y %H:%M:%S")
                response.set_cookie("user_email_or_phone", form.cleaned_data['mail_phone'], expires=expires_string)
                return response

        return render(request, 'user/login.html', {"categories": self.categories, 'form': form})


class Profile(View):
    pass