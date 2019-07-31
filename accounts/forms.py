from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import (
    Reader, Blogger
)


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# class ReaderSignUpForm(UserCreationForm):
#     email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
#     hobbies = models.ManyToManyField(Interest)
#     status = models.CharField(max_length=255)
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')