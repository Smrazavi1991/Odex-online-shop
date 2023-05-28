from random import randint
import re

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from core.views import BasicViewMixin
from .forms import RegisterUserForm, VerificationForm, SendOTPForm
from django.http import JsonResponse
from core.tasks import send_opt_email, send_opt_sms

from .models import User
from core.utils import identify_user_role, create_jwt_token


class Register(View, BasicViewMixin):

    def get(self, request):
        registeration_form = RegisterUserForm()
        return render(request, "user/register.html", {"categories": self.categories, "form": registeration_form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            #######################################
            # just for example. must change
            Register.otp_code = randint(100000, 999999)
            print(Register.otp_code)
            ##########################################
            request.session['username'] = form.cleaned_data['username']
            return redirect('Verification')
        return render(request, 'user/register.html', {'form': form})


class Verification(View, BasicViewMixin):
    def get(self, request):
        form = VerificationForm()
        return render(request, "user/verification.html", {"categories": self.categories, "form": form})

    def post(self, request):
        form = VerificationForm(request.POST)
        if form.is_valid():
            input_verification = int(form.cleaned_data['verification_code'])
            if input_verification == Register.otp_code:
                username = request.session.get('username', None)
                user = User.objects.get(username=username)
                auth_user = authenticate(username=user.username, password=user.password)
                if auth_user:
                    login(request, auth_user)
                    role = identify_user_role()
                    payload = {'user_id': auth_user.id, 'user_role': role}
                    create_jwt_token(payload)
                    return redirect('Home_page')
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        print(form.is_valid())
        return render(request, 'user/verification.html', {'form': form})


class Login(View, BasicViewMixin):
    def get(self, request):
        form = SendOTPForm()
        return render(request, 'user/login.html', {'categories': self.categories, 'form':form})

    def post(self, request):
        form = SendOTPForm(request.POST)
        if form.is_valid():
            if re.match(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', form.cleaned_data['mail_phone']):
                #########################################
                otp_code = randint(100000, 999999)
                ##########################################
                send_opt_email(otp_code, form.cleaned_data['mail_phone'])
                return redirect('Verification')
            elif re.match(r'^(09)\d{9}$', form.cleaned_data['mail_phone']):
                #########################################
                otp_code = randint(100000, 999999)
                ##########################################
                send_opt_sms(otp_code)
                return redirect('Verification')
        return render(request, 'user/login.html', {'form': form})



class Profile(View):
    pass
