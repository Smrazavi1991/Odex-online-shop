from random import randint

from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from core.views import BasicViewMixin
from .forms import RegisterUserForm, VerificationForm
from django.http import HttpResponse, JsonResponse

from .models import User
from core.utils import identify_user_role, create_jwt_token


class Register(View, BasicViewMixin):

    def get(self, request):
        registeration_form = RegisterUserForm()
        self.queryset.setdefault('form', registeration_form)
        self.template_name = "user/register.html"
        return super().get(request)

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
        self.queryset.setdefault('form', form)
        self.template_name = "user/verification.html"
        return super().get(request)

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


class Login(View):
    def get(self, request):
        return HttpResponse("hi")


class Profile(View):
    pass
