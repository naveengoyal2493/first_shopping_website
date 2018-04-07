from django.contrib.auth.models import User
from django import forms
from .models import *
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=20)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']
