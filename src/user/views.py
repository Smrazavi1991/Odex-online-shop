import re
import datetime
import redis

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, RedirectView
from django.views import View
from core.views import BasicViewMixin
from .forms import RegisterUserForm, VerificationForm, SendOTPForm, Loginform
from core.tasks import send_opt_email, send_opt_sms

from .models import User
from order.models import Order


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


class Login(View, BasicViewMixin):
    def get(self, request):
        form = Loginform()
        return render(request, 'user/login.html', {'categories': self.categories, 'form': form})

    def post(self, request):
        form = Loginform(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                return redirect('Home-page')
        return render(request, 'user/login.html', {"categories": self.categories, 'form': form})


class OtpLogin(View, BasicViewMixin):
    def get(self, request):
        form = SendOTPForm()
        return render(request, 'user/login_with_otp_code.html', {'categories': self.categories, 'form': form})

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
                expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiry_minutes)
                expires_string = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
                response.set_cookie("user_email_or_phone", form.cleaned_data['mail_phone'], expires=expires_string)
                return response

        return render(request, 'user/login_with_otp_code.html', {"categories": self.categories, 'form': form})


class Verification(View, BasicViewMixin):
    def get(self, request):
        form = VerificationForm()
        return render(request, "user/verification.html", {"categories": self.categories, "form": form})

    def post(self, request):
        form = VerificationForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']

            r = redis.Redis(host='localhost', port=6379, db=0)
            user_identifier = request.COOKIES.get('user_email_or_phone', None)
            storedcode = r.get(user_identifier).decode()
            if verification_code == storedcode:
                condition1 = Q(email=user_identifier)
                condition2 = Q(phone=user_identifier)
                user = User.objects.filter(condition1 | condition2).first()
                if user:
                    login(request, user)
                    return redirect('Home-page')
        return render(request, 'user/register.html', {"categories": self.categories, 'form': form})


class Profile(RedirectView):
    permanent = True
    pattern_name = "Orders list"


class OrdersList(TemplateView, BasicViewMixin):
    template_name = "user/orders-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.categories
        context['cart'] = self.get_user_cart(self.request, total=False)
        context['more_info'] = self.get_user_cart(self.request, total=True)
        context['orders'] = Order.objects.filter(cart__customer_id=self.request.user.pk)
        return context


class OrderDetail(TemplateView, BasicViewMixin):
    template_name = "user/order-detail.html"


class OrderTracking(TemplateView, BasicViewMixin):
    template_name = "user/order-tracking.html"


class UserInformation(TemplateView, BasicViewMixin):
    template_name = "user/user-information.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserInformation, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.categories
        context['cart'] = self.get_user_cart(self.request, total=False)
        context['more_info'] = self.get_user_cart(self.request, total=True)
        return context


class UserAddress(TemplateView, BasicViewMixin):
    template_name = "user/user_address.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.categories
        context['cart'] = self.get_user_cart(self.request, total=False)
        context['more_info'] = self.get_user_cart(self.request, total=True)
        context['orders'] = Order.objects.filter(cart__customer_id=self.request.user.pk)
        return context


class ChangePassword(TemplateView, BasicViewMixin):
    template_name = "user/change-password.html"


class Logout(View, BasicViewMixin):
    def get(self, request):
        logout(request)
        response = redirect('Home-page')
        response.set_cookie("token", '')
        return response


