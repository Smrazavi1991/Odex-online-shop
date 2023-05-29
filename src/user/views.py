from random import randint
import re
import datetime
import redis

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
            return redirect('Login')
        return render(request, 'user/register.html', {'form': form})


class Verification(View, BasicViewMixin):
    def get(self, request):
        form = VerificationForm()
        return render(request, "user/verification.html", {"categories": self.categories, "form": form})

    # def post(self, request):
    #     form = VerificationForm(request.POST)
    #     if form.is_valid():
    #         r = redis.Redis(host='localhost', port=6379, db=0)
    #         otp = request.COOKIES.get('user_email_or_phone')
    #         storedotp = r.get(otp).decode()
    #         if form.cleaned_data['verification_code'] == storedotp:
    #             pass
    #
    #
    #             username = request.session.get('username', None)
    #             user = User.objects.get(username=username)
    #             auth_user = authenticate(username=user.username, password=user.password)
    #             if auth_user:
    #                 login(request, auth_user)
    #                 role = identify_user_role()
    #                 payload = {'user_id': auth_user.id, 'user_role': role}
    #                 create_jwt_token(payload)
    #                 return redirect('Home_page')
    #             return JsonResponse({'message': 'Invalid credentials'}, status=401)
    #     print(form.is_valid())
    #     return render(request, 'user/verification.html', {'form': form})


class Login(View, BasicViewMixin):
    def get(self, request):
        form = SendOTPForm()
        return render(request, 'user/login.html', {'categories': self.categories, 'form':form})

    def post(self, request):
        form = SendOTPForm(request.POST)
        if form.is_valid():
            if re.match(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', form.cleaned_data['mail_phone']):
                if User.objects.get(email=form.cleaned_data['mail_phone']):
                    send_opt_email(form.cleaned_data['mail_phone'], 300)
                    response = redirect('Verification')
                    expiry_minutes = 5
                else:
                    raise Exception('invalid email')

            elif re.match(r'^(09)\d{9}$', form.cleaned_data['mail_phone']):
                if User.objects.get(phone=form.cleaned_data['mail_phone']):
                    send_opt_sms(form.cleaned_data['mail_phone'], 60)
                    expiry_minutes = 1
                else:
                    raise Exception('invalid phone')

            else:
                return render(request, 'user/login.html', {'form': form})

            expires = datetime.datetime.now() + datetime.timedelta(minutes=expiry_minutes)
            expires_string = expires.strftime("%a, %d-%b-%Y %H:%M:%S")
            response.set_cookie("user_email_or_phone", form.cleaned_data['mail_phone'], expires=expires_string)
            return response

        return render(request, 'user/login.html', {'form': form})


class Profile(View):
    pass