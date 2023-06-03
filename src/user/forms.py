from django import forms
from .models import *
from django.contrib.auth.hashers import make_password


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'password']
        error_messages = {
            'username': {
                'required': ',وارد کردن نام کاربری الزامی است.',
                'invalid': 'نام کاربری معتبر نمی باشد.',
                'unique': 'این نام کاربری قبلا ثبت شده است.',
            },
            'phone': {
                'required': ',وارد کردن شماره همراه الزامی است.',
                'invalid': 'شماره همراه معتبر نمی باشد.',
                'unique': 'این شماره قبلا ثبت شده است.',
                'min_length': 'لطفا شماره همراه به صورت ۰۹۱۲۳۴۵۶۷۸۹ وارد نمایید.',
                'max_length': 'لطفا شماره همراه به صورت ۰۹۱۲۳۴۵۶۷۸۹ وارد نمایید.',
            },
            'email': {
                'required': ',وارد کردن ایمیل الزامی است.',
                'invalid': 'ایمیل وارد شده معتبر نمی باشد.',
                'unique': 'این ایمیل قبلا ثبت شده است.',
                'invalid_email': 'ایمیل وارد شده معتبر نمی باشد.'
            },
            'password': {
                'required': ',وارد کردن کلمه عبور الزامی است.',
                'invalid': 'کلمه عبور معتبر نمی باشد',
            }}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class Loginform(forms.Form):
    username = forms.CharField(error_messages={
        'required': 'وارد کردن این فیلد الزامی است.',
        'invalid': 'نام کاربری یا رمز عبور معتبر نمی باشد'
    })
    password = forms.CharField(error_messages={
        'required': 'وارد کردن این فیلد الزامی است.',
        'invalid': 'نام کاربری یا رمز عبور معتبر نمی باشد'
    })


class SendOTPForm(forms.Form):
    mail_phone = forms.CharField(error_messages={
        'required': 'وارد کردن این فیلد الزامی است.',
        'invalid': 'شماره همراه یا ایمیل معتبر نمی باشد'
    })


class VerificationForm(forms.Form):
    verification_code = forms.CharField(max_length=6, error_messages={
        'required': ',وارد کردن کد الزامی است.',
        'max_length': 'طول کد وارد شده بیش از حد مجاز(6 کاراکتر) میباشد'
    })

