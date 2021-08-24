from django.db import models
from django.contrib.auth.models import User
from django.forms import fields
from dl5_app.models import UserInfo
from django import forms
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ("username","email","password")
class UserInfoForm(forms.ModelForm):
    class Meta:
        model=UserInfo
        fields=("portfolio_site","profile_pic")        