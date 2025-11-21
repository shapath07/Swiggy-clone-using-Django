from django import forms
from django.contrib.auth.forms import UserCreationForm 
from .models import UserRecord


class SignupForm(UserCreationForm):
    class Meta:
        model = UserRecord
        fields = ['username','password1','password2','email','phone','address']

